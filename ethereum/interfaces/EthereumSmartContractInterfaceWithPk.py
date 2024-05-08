from typing import Type, Any, Dict, Union, List, Tuple

from web3.contract import AsyncContract, Contract
from web3.contract.contract import ContractFunction

from core.interfaces.SmartContractInterface import SmartContractInterface

import subprocess
import os
import json
from web3 import *

from ethereum.utils import _get_private_key_from_account_path
from exchange_system import settings

SM_CONTRACT_BIN = 'smart_contract/Ethereum/output/Brain.bin'
SM_CONTRACT_ABI = 'smart_contract/Ethereum/output/Brain.abi'


class EthereumSmartContractInterfaceWithPk(SmartContractInterface):

    def __init__(self, provider_url: str, private_key: str, smc_address: str):
        """
        :param provider_url: Url/IP to the Ethereum node provider (rpc or html)
        :param account_path: Wallet file address
        :param keystore_password: Wallet password
        :param smc_address: Ethereum address where the SNC is deployed.
        """
        self.private_key = private_key
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.w3.eth.default_account = Account.from_key(self.private_key).address
        self.Contract = self._get_contract(self.w3, smc_address)

    def _get_contract(self, w3: Web3, smc_address: str) -> Contract:
        """
        Reads the SMART CONTRACT specifications and initializes it on the W3 connection
        """
        with open(SM_CONTRACT_ABI, 'r') as abi_file:
            abi = json.load(abi_file)

        # SET CONTRACT
        contract = w3.eth.contract(address=Web3.to_checksum_address(smc_address), abi=abi)
        return contract

    def _make_transaction_that_alters_the_blockchain(self, func: ContractFunction) -> Any:
        """
        It receives as a parameter the function of the contract to be invoked,
        which modifies the state of the chain, manages all the gas consumed,
        ensures that it is processed properly and returns the information in a tractable format.
        """
        # ESTIMATE REQUIRED GAS
        estimacion_gas = func.estimate_gas()

        # if settings.DEBUG:
        #     print("Estimate required gas: " + str(estimacion_gas))
        # estimacion_gas = int(estimacion_gas * 2)
        #
        # if settings.DEBUG:
        #     print("Estimate required gas after add 200% of margin: " + str(estimacion_gas))

        funcion_txn = func.build_transaction({
            'from': self.w3.eth.default_account,
            'chainId': self.w3.eth.chain_id,
            'gas': estimacion_gas,  # TODO change gass
            'gasPrice': self.w3.eth.gas_price,
            'nonce': self.w3.eth.get_transaction_count(self.w3.eth.default_account),
        })

        signed_txn = self.w3.eth.account.sign_transaction(funcion_txn, private_key=self.private_key)
        try:
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        except ValueError as e:
            tx_receipt = ''  # Transaction already sent
            print("Transaction already sent")
        return tx_receipt

    def _format_values(self, aux_val: Tuple[str, int, str, str, List[Tuple[Any, Any]]]) -> Dict[
        str, Union[str, int, List[Any]]]:
        """
        It receives the raw value of the smart contract structure and adapts it to the format used by the application.
        This is done for compatibility reasons with the other possible chains that can be configured.
        """
        requests = {}
        for account, acceptance in aux_val[4]:
            requests[account] = acceptance

        return {
            'Endpoint': aux_val[0],
            'ID': aux_val[1],
            'Owner': aux_val[2],
            'Description': aux_val[3],
            'Requests': requests
        }

    def _adapt_the_result(self, aux_result: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[
        List[Dict[str, Union[str, int, List[Any]]]], Dict[str, Union[str, int, List[Any]]]]:
        """
        It receives the raw value of the smart contract structure, which can be an individual value or a list,
        and adapts it to the format used by the application.
        """
        if aux_result:
            if isinstance(aux_result, list):
                result = []
                for aux in aux_result:
                    result.append(self._format_values(aux))
                return result
            else:
                return self._format_values(aux_result)
        else:
            return aux_result

    def create_asset(self, identifier: str, endpoint: str, description: str) -> str:
        """
        Announces a new asset by the client calling the function.
        """
        return self._make_transaction_that_alters_the_blockchain(
            self.Contract.functions.createAsset(identifier, endpoint, description))

    def read_asset(self, identifier: str) -> Union[
        list[dict[str, Union[str, int, list[Any]]]], dict[str, Union[str, int, list[Any]]]]:
        """
        Query the metadata of the asset identified with the value "identifier"
        """
        return self._adapt_the_result(self.Contract.functions.getAsset(identifier).call())

    def get_all_assets(self) -> Union[
        list[dict[str, Union[str, int, list[Any]]]], dict[str, Union[str, int, list[Any]]]]:
        """
        Consult the metadata of all available assets
        """
        return self._adapt_the_result(self.Contract.functions.getAllAssets().call())

    def update_asset(self, identifier: str, endpoint: str, description: str) -> str:
        """
        Modify the metadata of an own asset in the chain
        """
        return self._make_transaction_that_alters_the_blockchain(
            self.Contract.functions.UpdateAsset(identifier, endpoint, description))

    def delete_asset(self, identifier: str) -> bool:
        # Ethereum smart contract can not delete assets
        return None

    def request_asset(self, identifier: str) -> bool:
        """
        Solicita la posibilidad de acceso a los datos (no a los metadatos), de un asset identificado como "identifier"
        """
        return self._make_transaction_that_alters_the_blockchain(self.Contract.functions.RequestAsset(identifier))

    def accept_requests(self, identifier: str, requester: str) -> bool:
        """
        Accepts the request for access to the data of the asset identified as "identifier" of the requester "requester"
        """
        return self._make_transaction_that_alters_the_blockchain(
            self.Contract.functions.AcceptRequestAsset(identifier, requester))

    def deny_request(self, identifier: str, requester: str) -> bool:
        """
        Deny the request for access to the data of the asset identified as "identifier" of the requester "requester"
        """
        return self._make_transaction_that_alters_the_blockchain(
            self.Contract.functions.DenyRequestAsset(identifier, requester))
