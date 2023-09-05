import datetime
from time import sleep

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone

from core.interfaces.SmartContractInterface import SmartContractInterface
from core.models import Timers, GlobalData, ABSSharedData, ExternalRequests
from fabric.interfaces.FabricSmartContractInterface import FabricSmartContractInterface
from fabric.models import *


class Command(BaseCommand):
    help = "Sync blockchain data and request"

    blockchain_status_to_sync_status = {
        'Pending': GlobalData.PENDING,
        'Accepted': GlobalData.ACCEPTED,
        'Denied': GlobalData.DENIED
    }

    sync_status_to_blockchain_status = {
        GlobalData.PENDING: 'Pending',
        GlobalData.ACCEPTED: 'Accepted',
        GlobalData.DENIED: 'Denied'
    }

    def _get_interface(self):
        if settings.BLOCKCHAIN_LAYER == 'Fabric':
            peers = PeerNode.objects.all()
            orderers = OrdererNode.objects.all()

            if not peers.exists():
                raise Exception("You need at least one peers for the endorsement policies")

            if not orderers.exists():
                raise Exception("You need at least two orderers for the endorsement policies")

            orderer = orderers.first()
            return FabricSmartContractInterface(binary_path=settings.BINARY_PATH,
                                                fabric_cfg_path=settings.CONFIG_PATH,
                                                peer_msp_id=settings.MSP_ID,
                                                peer_msp_config_path=settings.MSP_CONFIG_PATH,
                                                peer_tls_root_cert=settings.TLS_ROOT_CERT,
                                                peer_address=settings.PEER_ADDRESS,
                                                channel=settings.CHANNEL,
                                                chaincode=settings.CHAINCODE,
                                                orderer=[orderer.host, orderer.tls_host_override,
                                                         orderer.path_to_tls_ca_cert],
                                                endorsement_peers=[[peer.host, peer.path_to_tls_ca_cert]
                                                                   for peer in peers.iterator()]
                                                )
        raise Exception("Unknown blockchain layer {}".format(settings.BLOCKCHAIN_LAYER))

    def _get_now(self, timer):
        return timezone.now()

    def _have_to_run(self, timer: Timers) -> bool:
        if timer.last_sync is None:
            return True
        now = self._get_now(timer)
        return now > timer.last_sync + datetime.timedelta(seconds=timer.seconds)

    def _manage_phases(self, interface: SmartContractInterface, timer: Timers, func):
        if self._have_to_run(timer):
            func(interface)
            timer.last_sync = self._get_now(timer)
            timer.save()

    def _manage_global_data(self, interface: SmartContractInterface) -> None:
        # UPLOAD NEW ASSETS
        for data in ABSSharedData.objects.filter(synchronized=False).exclude(created=False):
            interface.update_asset(id=data.identifier, endpoint=settings.ENDPOINT + '/endpoint/' + str(data.pk) + '/',
                                   description=data.description)
            data.synchronized = True
            data.save()

        # CREATE NEW ASSETS
        for data in ABSSharedData.objects.filter(created=False):
            interface.create_asset(id=data.identifier, endpoint=settings.ENDPOINT + '/endpoint/' + str(data.pk) + '/',
                                   description=data.description)
            data.created = True
            data.synchronized = True
            data.save()

        # CREATE OR UPDATE EXISTENT DATA
        results = interface.get_all_assets()
        for r in results:
            GlobalData.objects.update_or_create(identifier=r['ID'],
                                                defaults={"owner": r['Owner'], "description": r['Description'],
                                                          "endpoint": r['Endpoint']})
            if r['Owner'] == settings.OWNER_IDENTITY:
                query = ABSSharedData.objects.filter(identifier=r['ID'])
                if query.exists():
                    for request in r['Requests'].keys():
                        ExternalRequests.objects.get_or_create(requester=request,
                                                               related_data=query.first(),
                                                               defaults={'synchronized': True,
                                                                         'status': ExternalRequests.PENDING})

    def manage_global_data(self, interface: SmartContractInterface) -> None:
        timer = Timers.objects.get(timer_type=Timers.GLOBAL)
        self._manage_phases(interface, timer, self._manage_global_data)

    def _manage_external_request(self, interface: SmartContractInterface) -> None:
        for requester in ExternalRequests.objects.filter(synchronized=False):
            if requester.status == ExternalRequests.ACCEPTED:
                interface.accept_requests(id=requester.related_data.identifier, requester=requester.requester)
                requester.synchronized = True
                requester.save()
            elif requester.status == ExternalRequests.DENIED:
                interface.deny_request(id=requester.related_data.identifier, requester=requester.requester)
                requester.synchronized = True
                requester.save()

    def manage_external_request(self, interface: SmartContractInterface) -> None:
        timer = Timers.objects.get(timer_type=Timers.EXTERNAL_REQUEST)
        self._manage_phases(interface, timer, self._manage_external_request)

    def _manage_petitions(self, interface: SmartContractInterface) -> None:
        own_requests = GlobalData.objects.exclude(sync_status=GlobalData.KNOWN)
        for own_request in own_requests.iterator():
            blockchain_data = interface.read_asset(id=own_request.identifier)
            if blockchain_data:
                if not settings.OWNER_IDENTITY in blockchain_data['Requests']:
                    interface.request_asset(id=own_request.identifier)
                    own_request.sync_status = GlobalData.PENDING

                else:
                    own_request.sync_status = self.blockchain_status_to_sync_status[
                        blockchain_data['Requests'][settings.OWNER_IDENTITY]]
                own_request.save()

    def manage_petitions(self, interface: SmartContractInterface) -> None:
        timer = Timers.objects.get(timer_type=Timers.PETITIONS)
        self._manage_phases(interface, timer, self._manage_petitions)

    def handle(self, *args, **options):
        interface = self._get_interface()
        while True:
            self.manage_global_data(interface)
            self.manage_external_request(interface)
            self.manage_petitions(interface)
            sleep(5)

        # self.stdout.write(self.style.SUCCESS('Data initialized'))
