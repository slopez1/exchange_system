

from django.core.management.base import BaseCommand

from ethereum.models import Config
from ethereum.utils import compile_smart_contract, deploy_smart_contract

# DEFAULT_VALUES
NODE_URL = 'http://test:8545/'
ACCOUNT_PATH = 'ExampleDockers/Ethereum/files/keystore/UTC--2016-02-29T14-52-41.334222730Z--007ccffb7916f37f7aeef05e8096ecfbe55afc2f'
KEYSTORE_PASSWORD = ''

PATH_TO_BIN = "smart_contract/Ethereum/output/Brain.bin"
PATH_TO_ABI = "smart_contract/Ethereum/output/Brain.abi"


def ask_for_sample_config():
    response = '-'
    while response not in ["Y", "N", ""]:
        response = input("Do you want to activate the sample configuration? (Y/N) default: Y ").strip().upper()
        if response == "N":
            print("Sample configuration will not be activated.")
            return False
        elif response == "Y" or response == "":
            print("You have chosen to activate the sample configuration.")
            return True


def ask_for_SMC_deploy():
    response = '-'
    while response not in ["1", "2", ""]:
        response = input("Do you want to deploy the contract from scratch or do you already have an address?" +
                         " (1 - New Deploy | 2 - I have address) Default: 1").strip()
        if response == "2":
            return False
        elif response == "1" or response == "":
            return True



class Command(BaseCommand):
    help = "Brain guided setup for ethereum. Leave everything configured for Brain to work."

    def handle(self, *args, **options):

        if Config.objects.all().exists():
            user_response = None
            while user_response not in ["Y", "N", ""]:
                user_response = input("There is an ethereum configuration, do you want to delete it? (Y/N), default: N: ")\
                    .strip().upper()
                if user_response not in ["Y", "N", ""]:
                    print("Please enter 'Y' for Yes or 'N' for No.")

            if user_response == "Y":
                Config.objects.all().delete()
                print("Removed old configuration.")
            else:
                print("Process stopped, a configuration already exists.")
                return

        print()
        print()
        welcome_message = """
        +--------------------------------------------------+
        | Welcome to the BRAIN Configurator for Ethereum!  |
        | Here you will set up the minimum values required |
        | for BRAIN to connect to Ethereum. Let's begin:   |
        +--------------------------------------------------+
        """

        print(welcome_message)
        if ask_for_sample_config():
            node_url = NODE_URL
            account_path = ACCOUNT_PATH
            keystore_password = KEYSTORE_PASSWORD

        else: # No activar
            node_url = input("Please enter the URL of the provider node: ").strip()
            account_path = input("Please enter the URL of the Ethereum account file: ").strip()
            keystore_password = input("Please enter the password for the Ethereum account: ").strip()

        compile_smart_contract()

        if ask_for_SMC_deploy():
            smc_address = deploy_smart_contract(node_url, account_path, keystore_password)
        else:
            smc_address = input("Smart contract address: ").strip()

        Config.objects.create(
            node_url=node_url,
            account_path=account_path,
            keystore_password=keystore_password,
            smc_address=smc_address
        )

        print("All done")


