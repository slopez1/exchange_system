import base64

import OpenSSL.crypto
from django.conf import settings
from django.http import HttpResponseForbidden
from eth_account.messages import encode_defunct
from web3 import Web3


class CASecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def _manage_fabric(self, request):
        # Get cliente certificate from request
        client_cert_data = request.META.get('HTTP_X_PUBLIC_CERT')
        if client_cert_data:
            decoded_cert = base64.b64decode(client_cert_data)
            client_cert_data = decoded_cert.decode('utf-8')
            try:
                # Load client cert
                client_certificate = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, client_cert_data)

                # Load CA cert
                with open(settings.CA_ROOT_CERT, 'r') as ca_cert_file:
                    ca_cert_data = ca_cert_file.read()
                    ca_certificate = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, ca_cert_data)

                # Validate if client cert was emitted from the correct CA
                store = OpenSSL.crypto.X509Store()
                store.add_cert(ca_certificate)

                store_ctx = OpenSSL.crypto.X509StoreContext(store, client_certificate)
                store_ctx.verify_certificate()
                # All is okey
                return self.get_response(request)
            except OpenSSL.crypto.X509StoreContextError:
                # Access denied. Certificate not valid. (403)
                return HttpResponseForbidden("Access denied. Certificate not valid.")
        else:
            # Certificate not provided (403)
            return HttpResponseForbidden("Access denied. Certificate not provided.")

    def _manage_ethereum(self, request):
        if 'X-Signature' in request.headers:
            try:
                signature_encoded = request.headers['X-Signature']
                signature = bytes.fromhex(signature_encoded[2:])
                w3 = Web3()
                coded_message = encode_defunct(text="")
                recovered_account = w3.eth.account.recover_message(coded_message, signature=signature)
                # All is okey, the account exists
                return self.get_response(request)
            except Exception as e:
                print("Error on Ethereum middleware: " + str(e))
                return HttpResponseForbidden("Access denied. Signature not valid.")
        else:
            return HttpResponseForbidden("Access denied. Certificate not provided.")

    def _need_to_apply_this_middleware(self, request):
        # Override on chills to customize this url affected for the middleware
        return True

    def __call__(self, request):
        if self._need_to_apply_this_middleware(request):
            if settings.BLOCKCHAIN_LAYER == 'Fabric':
                return self._manage_fabric(request)
            elif settings.BLOCKCHAIN_LAYER == 'Ethereum':
                return self._manage_ethereum(request)
            else:
                return self.get_response(request)
        else:
            return self.get_response(request)
