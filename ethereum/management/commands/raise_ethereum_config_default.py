import os

from django.core.management.base import BaseCommand

from ethereum.models import Config
from ethereum.utils import compile_smart_contract, deploy_smart_contract

# DEFAULT_VALUES
NODE_URL = 'http://bootstrap:8545'
ACCOUNT_PATH = os.getenv('ACCOUNT_PATH', 'ExampleDockers/Ethereum/files/keystore/UTC--2016-02-29T14-52-41.334222730Z--007ccffb7916f37f7aeef05e8096ecfbe55afc2f')

KEYSTORE_PASSWORD = ''

PATH_TO_BIN = "smart_contract/Ethereum/output/Brain.bin"
PATH_TO_ABI = "smart_contract/Ethereum/output/Brain.abi"

PATH_TO_SM_ADDRESS = 'ExampleDockers/Ethereum/exchange_system/healthcheck/address'

class Command(BaseCommand):
    help = "Set up Brain to work with ethereum. ATTENTION! This is only for docker, use raise_ethereum_config instead'"

    def handle(self, *args, **options):
        node_url = NODE_URL
        account_path = ACCOUNT_PATH
        keystore_password = KEYSTORE_PASSWORD
        compile_smart_contract()
        if os.path.exists(PATH_TO_SM_ADDRESS):
            with open(PATH_TO_SM_ADDRESS, 'r') as file:
                smc_address = file.read()
        else:
            smc_address = deploy_smart_contract(node_url, account_path, keystore_password)
            with open(PATH_TO_SM_ADDRESS, 'w') as f:
                f.write(smc_address)
        Config.objects.create(
            node_url=node_url,
            account_path=account_path,
            keystore_password=keystore_password,
            smc_address=smc_address
        )



