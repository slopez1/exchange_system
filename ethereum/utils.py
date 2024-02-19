from solcx import compile_source, install_solc
import json
from web3 import *
from web3.middleware import geth_poa_middleware

SM_CONTRACT_ABI = "smart_contract/Ethereum/output/Brain.abi"
SM_CONTRACT_BIN = "smart_contract/Ethereum/output/Brain.bin"


def _get_private_key_from_account_path(account_path: str, keystore_password: str = '') -> str:
    """
    From a file of accounts and the Ethereum unlock password, it returns the associated private key.
    """

    # Load the contents of the keystore file
    with open(account_path) as keyfile:
        encrypted_key = keyfile.read()
        keyfile.close()

    # Decrypt private key
    private_key = Account.decrypt(encrypted_key, keystore_password)

    # Convert private key to hexadecimal string
    private_key_hex = private_key.hex()
    return private_key_hex


def compile_smart_contract():
    """
    This function compiles the contract to smart contract/Ethereum/brain.sol
    with the appropriate flags and the correct solc version for this smart contract.
    """

    # INSTALL REQUIRED SOLC VERSION
    print("[1/3] INSTALLING NEEDED SOLC VERSION")
    print("---------------------------------")
    install_solc('0.8.18')
    print("Done.")
    print("---------------------------------")

    print("[2/3] COMPILING ABI & BIN")
    print("---------------------------------")
    with open('smart_contract/Ethereum/brain.sol', 'r') as file:
        source_code = file.read()
        compiled_sol = compile_source(
            source_code,
            solc_version='0.8.18'
        )
    contract_id, contract_interface = compiled_sol.popitem()
    bytecode = contract_interface['bin']
    abi = contract_interface['abi']
    print("Done.")
    print("---------------------------------")

    print("[3/3] SAVING IT IN smart_contract/Ethereum/output/")
    print("---------------------------------")
    with open('smart_contract/Ethereum/output/Brain.bin', 'w') as bin_file:
        bin_file.write(bytecode)

    with open('smart_contract/Ethereum/output/Brain.abi', 'w') as abi_file:
        json.dump(abi, abi_file)

    print("Done.")
    print("---------------------------------")


def get_account_from_path(account_path: str, keystore_password: str = '') -> Account:
    """
    From an ethereum accounts file, it returns the associated account.
    """
    with open(account_path) as keyfile:
        encrypted_key = keyfile.read()
        keyfile.close()

    # Descifrar la clave privada
    private_key = Account.decrypt(encrypted_key, keystore_password)
    return Account.from_key(private_key)


def deploy_smart_contract(provider_url: str, account_path: str, keystore_password: str) -> str:
    """
    Deploys the compiled smart contract in the compile_smart_contract function to the Ethereum blockchain that the node
    "provider_url" is a part of, as long as the account obtained by account_path and keystore_password is valid and has
    sufficient funds.
    """

    private_key = _get_private_key_from_account_path(account_path, keystore_password)
    account = Account.from_key(private_key)
    w3 = Web3(Web3.HTTPProvider(provider_url))
    w3.eth.defaultAccount = account
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # Información del contrato
    with open(SM_CONTRACT_ABI, 'r') as abi_file:
        abi = json.load(abi_file)

    with open(SM_CONTRACT_BIN, 'r') as bytecode_file:
        bytecode = bytecode_file.read()
    # Crear el contrato en Web3
    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    # DEPLOY: PRINT ESTIMATE GAS
    estimacion_gas = Contract.constructor().estimate_gas()
    print("Estimate required gas: " + str(estimacion_gas))  # 2660670
    estimacion_gas = int(estimacion_gas * 1.2)
    print("Estimate required gas after add 20% of margin: " + str(estimacion_gas))  # 2660670

    # Construir la transacción
    construct_txn = Contract.constructor().build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': estimacion_gas,
        'gasPrice': w3.eth.gas_price
    })

    # Firmar la transacción
    signed = w3.eth.account.sign_transaction(construct_txn, private_key)

    # Enviar la transacción
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)

    # Esperar por el recibo de la transacción
    tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash=tx_hash, timeout=1200)

    # Obtener la dirección del contrato desplegado
    contract_address = tx_receipt.contractAddress

    print(f"Contrato desplegado en la dirección: {contract_address}")
    return contract_address
