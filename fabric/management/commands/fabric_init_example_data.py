from django.core.management.base import BaseCommand, CommandError

from fabric.models import *

class Command(BaseCommand):
    help = "Initializes the database with the orderers, peers and data from fabric sample application of version 2.4"

    def handle(self, *args, **options):
        if not PeerNode.objects.all().exists():
            PeerNode.objects.create(host="localhost:7051",
                                    path_to_tls_ca_cert="/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt")
            PeerNode.objects.create(host="localhost:9051",
                                    path_to_tls_ca_cert="/fabric-samples/test-network/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt")

        if not OrdererNode.objects.all().exists():
            OrdererNode.objects.create(host="localhost:7050",
                                       path_to_tls_ca_cert="/fabric-samples/test-network/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem",
                                       tls_host_override="orderer.example.com")

            self.stdout.write(self.style.SUCCESS('Data initialized'))