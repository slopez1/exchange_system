import requests
import OpenSSL.crypto
from django.conf import settings
import base64

from eth_account.messages import encode_defunct
from web3 import Web3

import ethereum
from core.models import GlobalData
from ethereum.utils import _get_private_key_from_account_path


def make_signed_request(url, message=''):
    if settings.BLOCKCHAIN_LAYER == 'Fabric':
        return make_signed_request_fabric(url, message)
    elif settings.BLOCKCHAIN_LAYER == 'Ethereum':
        return make_signed_request_ethereum(url, message)
    else:
        return requests.get(url)

def make_signed_request_ethereum(url, message=''):
    configs = ethereum.models.Config.objects.all()
    if not configs.exists():
        raise Exception("You need to configure brain first, please execute python manage.py raise_ethereum_config")

    config = configs.first()
    private_key = _get_private_key_from_account_path(config.account_path, config.keystore_password)

    w3 = Web3()
    encode_message = encode_defunct(text=message)
    signature = w3.eth.account.sign_message(encode_message, private_key=private_key)

    headers = {
        'X-Signature': signature.signature.hex(),  # Signed message
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("Denied: {}".format(response.status_code))
        return "Denied: {}".format(response.status_code)

def make_signed_request_fabric(url, message=''):
    # Load public and private keys
    with open(settings.OWNER_PRIVATE_CERT, 'r') as key_file:
        key_data = key_file.read()

    private_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, key_data)

    # Sign message
    signature = OpenSSL.crypto.sign(private_key, message, 'sha256')

    # Code sign with base64
    encoded_signature = base64.b64encode(signature).decode('utf-8')

    # Load public cert
    with open(settings.OWNER_CERT, 'r') as cert_file:
        cert_data = cert_file.read()

    # Codificar el certificado público en base64
    encoded_cert = base64.b64encode(cert_data.encode('utf-8')).decode('utf-8')

    headers = {
        'X-Signature': encoded_signature,  # Signed message
        'X-public-cert': encoded_cert  # Added public cert
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return "Denied: {}".format(response.status_code)



def request_blockchain_data(identifier):
    data = GlobalData.objects.get(identifier=identifier)
    return make_signed_request(data.endpoint)
