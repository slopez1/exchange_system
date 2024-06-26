"""
Django settings for exchange_system project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import asyncio
import base64
import os
from pathlib import Path
from time import sleep

import OpenSSL.crypto

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


#############################
#          IMPORTANT        #
#############################
BLOCKCHAIN_LAYER_OPTIONS = ['Fabric', 'Ethereum']
BLOCKCHAIN_LAYER = os.getenv("EXCHANGE_SYSTEM_BLOCKCHAIN_LAYER",
                             'Fabric')  # Select blockchain layer Fabric/Ethereum (Ethereum WIP)

if BLOCKCHAIN_LAYER not in BLOCKCHAIN_LAYER_OPTIONS:
    raise EnvironmentError("{} its invalid option please set EXCHANGE_SYSTEM_BLOCKCHAIN_LAYER"
                           " variable with crrect option, options: {}".format(BLOCKCHAIN_LAYER,
                                                                              str(BLOCKCHAIN_LAYER_OPTIONS)))

ENDPOINT = os.getenv("EXCHANGE_SYSTEM_ENDPOINT",
                     'http://localhost:8000')  # The endpoint where this node will publish the data.
############################


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('EXCHANGE_SYSTEM_SECRET_KEY',
                       'django-insecure-w2mz3yen)*0sbjb^#tc#9c)j7%39310=_4(w%3phr1m$ms0stb')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv('EXCHANGE_SYSTEM_DEBUG', 'True') == 'True' else False

ALLOWED_HOSTS = ['*']

def get_identity(cert_data: str) -> str:
    certificate = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_data)
    # Get cert subject
    subject = certificate.get_subject()

    # Extract the subjects components
    common_name = subject.CN
    organizational_unit = subject.OU
    locality = subject.L
    state = subject.ST
    country = subject.C

    # Build cert identity
    identity = f"x509::CN={common_name},OU={organizational_unit},L={locality},ST={state},C={country}::"

    # Get cert issuer
    issuer = certificate.get_issuer()

    # Extract cert issuer
    issuer_common_name = issuer.CN
    issuer_organization = issuer.O
    issuer_locality = issuer.L
    issuer_state = issuer.ST
    issuer_country = issuer.C

    # Add emiter id to the cet id
    identity += f"CN={issuer_common_name},O={issuer_organization},L={issuer_locality},ST={issuer_state},C={issuer_country}"
    return base64.b64encode(identity.encode('utf-8')).decode('utf-8')

def extract_certificate_identity(cert_file: str) -> str:
    # Load certificate
    with open(cert_file, 'r') as file:
        cert_data = file.read()
    return get_identity(cert_data)


if BLOCKCHAIN_LAYER == 'Fabric':
    MANDATORY_ENV_VARS = ["EXCHANGE_SYSTEM_BINARY_PATH",
                          "EXCHANGE_SYSTEM_CONFIG_PATH",
                          "EXCHANGE_SYSTEM_MSP_ID",
                          "EXCHANGE_SYSTEM_MSP_CONFIG_PATH",
                          "EXCHANGE_SYSTEM_TLS_ROOT_CERT",
                          "EXCHANGE_SYSTEM_PEER_ADDRESS",
                          "EXCHANGE_SYSTEM_CHANNEL",
                          "EXCHANGE_SYSTEM_CHAINCODE",
                          "EXCHANGE_SYSTEM_OWNER_CERT",
                          "EXCHANGE_SYSTEM_OWNER_PRIVATE_CERT",
                          "EXCHANGE_SYSTEM_CA_ROOT_CERT",
                          ]

    for var in MANDATORY_ENV_VARS:
        if var not in os.environ:
            raise EnvironmentError("Failed because {} is not set.".format(var))

    BINARY_PATH = os.getenv('EXCHANGE_SYSTEM_BINARY_PATH')  # Path to fabric binaries
    CONFIG_PATH = os.getenv('EXCHANGE_SYSTEM_CONFIG_PATH')  # Path to fabric config folder
    MSP_ID = os.getenv('EXCHANGE_SYSTEM_MSP_ID')  # ID of local msp
    MSP_CONFIG_PATH = os.getenv('EXCHANGE_SYSTEM_MSP_CONFIG_PATH')  # Path to user msp
    TLS_ROOT_CERT = os.getenv('EXCHANGE_SYSTEM_TLS_ROOT_CERT')  # Path to the public key of TLS-CA
    PEER_ADDRESS = os.getenv(
        'EXCHANGE_SYSTEM_PEER_ADDRESS')  # Hostname and port of the current peer witch locate this code.
    CHANNEL = os.getenv('EXCHANGE_SYSTEM_CHANNEL')  # Channel where smart contract was locate
    CHAINCODE = os.getenv('EXCHANGE_SYSTEM_CHAINCODE')  # Channel where smart contract was locate
    OWNER_CERT = os.getenv('EXCHANGE_SYSTEM_OWNER_CERT')  # Path to owner public cert
    OWNER_PRIVATE_CERT = os.getenv('EXCHANGE_SYSTEM_OWNER_PRIVATE_CERT')  # Path to owner public cert
    OWNER_IDENTITY = extract_certificate_identity(OWNER_CERT)
    CA_ROOT_CERT = os.getenv('EXCHANGE_SYSTEM_CA_ROOT_CERT')  # Path to the public key of CA




# Application definition

INSTALLED_APPS = [
    "frontend.apps.FrontendConfig",
    "endpoint.apps.EndpointConfig",
    "ethereum.apps.EthereumConfig",
    "fabric.apps.FabricConfig",
    'rest_framework',
    "core.apps.CoreConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "endpoint.middleware.EndpointCASecurityMiddleware.EndpointCASecurityMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware"

]

ROOT_URLCONF = "exchange_system.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "exchange_system.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

POSTGRES_NAME = os.getenv("POSTGRES_NAME", '')
POSTGRES_USER = os.getenv("POSTGRES_USER", '')
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", '')
POSTGRES_HOST = os.getenv("POSTGRES_HOST", 'db')

if POSTGRES_USER:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_NAME'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': POSTGRES_HOST,
            'PORT': 5432,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

OWNER_IDENTITY = os.getenv('EXCHANGE_SYSTEM_OWNER_IDENTITY', None)


#########################################
# FABRIC EXCHANGE SYSTEM REQUIRED SETUP #
#########################################




BC_GRACE_TIME = os.getenv('EXCHANGE_SYSTEM_BC_GRACE_TIME',
                          15)  # Time that the system tolerates, if it does not detect changes in the blockchain before sending another request


