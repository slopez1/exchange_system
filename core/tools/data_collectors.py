import requests
import OpenSSL.crypto
from django.conf import settings
import base64
from core.models import GlobalData


def make_signed_request(url, message=''):
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
        print("Denied: {}".format(response.status_code))
        return "Denied: {}".format(response.status_code)



def request_blockchain_data(identifier):
    data = GlobalData.objects.get(identifier=identifier)
    return make_signed_request(data.endpoint)
