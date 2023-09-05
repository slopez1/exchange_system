import base64

import OpenSSL
from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, utils, ec
from django.conf import settings

from core.models import ExternalRequests
from exchange_system.settings import extract_certificate_identity, get_identity


def _validate_signature(signature: bytes, public_cert: str) -> bool:
    # Eliminar el encabezado y el pie del certificado
    cert_data = public_cert.strip().replace('-----BEGIN CERTIFICATE-----', '') \
        .replace('-----END CERTIFICATE-----', '')

    # Decodificar el certificado desde base64
    decoded_cert = base64.b64decode(cert_data)

    # Cargar el certificado
    cert = x509.load_der_x509_certificate(decoded_cert, default_backend())

    # Extraer la clave pública del certificado
    public_key = cert.public_key()
    try:
        public_key.verify(signature, b'', ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False


def _validate_fabric_access(identifier: str, request) -> bool:
    if "HTTP_X_SIGNATURE" in request.META:
        encoded_cert = request.META['HTTP_X_PUBLIC_CERT']
        decoded_cert = base64.b64decode(encoded_cert)
        public_cert = decoded_cert.decode('utf-8')

        encoded_signature = request.META['HTTP_X_SIGNATURE']
        signature = base64.b64decode(encoded_signature)

        if _validate_signature(signature, public_cert):
            requester = get_identity(public_cert)
            return ExternalRequests.objects.filter(requester=requester,
                                                   related_data__identifier=identifier,
                                                   status=ExternalRequests.ACCEPTED).exists()
    return False


def validate_access(identifier: str, request) -> bool:
    if settings.BLOCKCHAIN_LAYER == 'Fabric':
        return _validate_fabric_access(identifier, request)
    else:
        return True
