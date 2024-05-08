import time

from django.core.management.base import BaseCommand, CommandError

from exchange_system import settings
from fabric.interfaces.FabricSmartContractInterface import FabricSmartContractInterface
from fabric.models import *

class Command(BaseCommand):
    help = "Test Fabric Speed (Needed command fabric_init_example_data)"

    def handle(self, *args, **options):
        peers = PeerNode.objects.all()
        orderers = OrdererNode.objects.all()

        if not peers.exists():
            raise Exception("You need at least one peers for the endorsement policies")

        if not orderers.exists():
            raise Exception("You need at least two orderers for the endorsement policies")
        self.account = settings.OWNER_IDENTITY
        orderer = orderers.first()
        interface = FabricSmartContractInterface(binary_path=settings.BINARY_PATH,
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

        results = {
            'create_asset': {"time": []},
            'update_asset': {"time": []},
            'request_asset': {"time": []},
            'accept_requests': {"time": []},
            'deny_request': {"time": []},
        }

        def add_to_results(func, tx_receipt, time):
            results[func]["time"].append(time)

            print(f"'func': {func},'Time': {elapsed_time}")

        def print_results(f):
            print(f)
            print("_____________")
            v = "time"
            print(
                f"{v}:\tmax: {max(results[f][v])},  min: {min(results[f][v])}, med={round(sum(results[f][v]) / len(results[f][v]), 2)}")
            print()
            print()

        for i in range(1, 50):
            asset = "Test" + str(i)
            try:
                func = 'create_asset'
                start_time = time.time()
                interface.create_asset(asset, "72.1.2.3/1", asset)
                end_time = time.time()
                elapsed_time = end_time - start_time
                add_to_results(func, "", elapsed_time)
                time.sleep(2)
            except Exception as e:
                print(str(e))

            try:
                func = 'update_asset'
                start_time = time.time()
                interface.update_asset(asset, "72.1.2.3/1", asset)
                end_time = time.time()
                elapsed_time = end_time - start_time
                add_to_results(func, "", elapsed_time)
                time.sleep(2)
            except Exception as e:
                print(str(e))

            try:
                func = 'request_asset'
                start_time = time.time()
                interface.request_asset(asset)
                end_time = time.time()
                elapsed_time = end_time - start_time
                add_to_results(func, "", elapsed_time)
                time.sleep(2)
            except Exception as e:
                print(str(e))

            try:
                func = 'accept_requests'
                start_time = time.time()
                interface.accept_requests(asset, 'eDUwOTo6Q049QWRtaW5Ab3JnMS5leGFtcGxlLmNvbSxPVT1hZG1pbixMPVNhbiBGcmFuY2lzY28sU1Q9Q2FsaWZvcm5pYSxDPVVTOjpDTj1jYS5vcmcxLmV4YW1wbGUuY29tLE89b3JnMS5leGFtcGxlLmNvbSxMPVNhbiBGcmFuY2lzY28sU1Q9Q2FsaWZvcm5pYSxDPVVT')
                end_time = time.time()
                elapsed_time = end_time - start_time
                add_to_results(func, "", elapsed_time)
                time.sleep(2)
            except Exception as e:
                print(str(e))

            try:
                func = 'deny_request'
                start_time = time.time()
                interface.deny_request(asset, 'eDUwOTo6Q049QWRtaW5Ab3JnMS5leGFtcGxlLmNvbSxPVT1hZG1pbixMPVNhbiBGcmFuY2lzY28sU1Q9Q2FsaWZvcm5pYSxDPVVTOjpDTj1jYS5vcmcxLmV4YW1wbGUuY29tLE89b3JnMS5leGFtcGxlLmNvbSxMPVNhbiBGcmFuY2lzY28sU1Q9Q2FsaWZvcm5pYSxDPVVT');
                end_time = time.time()
                elapsed_time = end_time - start_time
                add_to_results(func, "", elapsed_time)
                time.sleep(2)
            except Exception as e:
                print(str(e))

        func = 'create_asset'
        print_results(func)

        func = 'update_asset'
        print_results(func)

        func = 'request_asset'
        print_results(func)

        func = 'accept_requests'
        print_results(func)

        func = 'deny_request'
        print_results(func)