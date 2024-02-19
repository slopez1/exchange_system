# BRAIN

BRAIN is described as a sophisticated and modular framework that utilizes blockchain technology to provide an innovative
and smart solution for fostering collaboration, trust, and competitiveness among entities in a highly interconnected
world. BRAIN is designed to address the challenges of secure data exchange and information sharing among entities. It
offers features like flexibility, efficiency, security, robustness, and scalability, without the need for
intermediaries, to improve productivity and collaboration between entities. BRAIN is intended to serve as a configurable
foundation for the development of domain-specific applications, offering a secure and efficient data exchange platform.

# FABRIC
## Required software

- Python 3.9.15
- Fabric binaries (Instructions: https://hyperledger-fabric.readthedocs.io/en/release-2.2/install.html)
- Go version 1.20.x (To install Fabric Smart contract)

## Installation

1. Download the repository and access it.
2. Execute the command ``pip install -r requirements.txt.``
3. Install the smart contract located in your blockchain at `exchange_system/smart_contract/fabric`.
4. Fill in the following environment variables

Fill in the following environment variables:

```bash
   export DJANGO_SETTINGS_MODULE=exchange_system.settings
   export EXCHANGE_SYSTEM_BLOCKCHAIN_LAYER='Fabric'
   export EXCHANGE_SYSTEM_BINARY_PATH=Path to Fabric binaries
   export EXCHANGE_SYSTEM_CA_ROOT_CERT=Path to the public certificate of the certificate authority
   export EXCHANGE_SYSTEM_CHAINCODE=Namespace under which the smart contract is registered
   export EXCHANGE_SYSTEM_CHANNEL=Name of the channel on which the smart contract operates
   export EXCHANGE_SYSTEM_CONFIG_PATH=Path to the Fabric client configuration file
   export EXCHANGE_SYSTEM_MSP_CONFIG_PATH=Path to the Fabric client\'s MSP
   export EXCHANGE_SYSTEM_MSP_ID=MSP Identifier
   export EXCHANGE_SYSTEM_OWNER_CERT=Public certificate of the Fabric client
   export EXCHANGE_SYSTEM_OWNER_PRIVATE_CERT=Private certificate of the Fabric client
   export EXCHANGE_SYSTEM_PEER_ADDRESS=Network address of a peer belonging to the node\'s channel
   export EXCHANGE_SYSTEM_TLS_ROOT_CERT=Path to the public certificate of the TLS entity```
```

Example using the Docker images provided in the Fabric binaries:

```bash
   export DJANGO_SETTINGS_MODULE=exchange_system.settings
   export EXCHANGE_SYSTEM_BLOCKCHAIN_LAYER='Fabric'
   export EXCHANGE_SYSTEM_BINARY_PATH=/fabric-samples/bin
   export EXCHANGE_SYSTEM_CA_ROOT_CERT=/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem
   export EXCHANGE_SYSTEM_CHAINCODE=basic
   export EXCHANGE_SYSTEM_CHANNEL=mychannel
   export EXCHANGE_SYSTEM_CONFIG_PATH=/fabric-samples/config
   export EXCHANGE_SYSTEM_MSP_CONFIG_PATH=/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
   export EXCHANGE_SYSTEM_MSP_ID=Org1MSP
   export EXCHANGE_SYSTEM_OWNER_CERT=/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/signcerts/Admin@org1.example.com-cert.pem
   export EXCHANGE_SYSTEM_OWNER_PRIVATE_CERT=/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/priv_sk
   export EXCHANGE_SYSTEM_PEER_ADDRESS=localhost:7051
   export EXCHANGE_SYSTEM_TLS_ROOT_CERT=/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
```

5. Run ```python python manage.py migrate```
6. Modify the field /exchange_system/fabric/management/commands/fabric_init_example_data.py, changing the parameters of
   PeerNode.objects.create and OrdererNode.objects.create to match your use case, and then
   run ```python python manage.py fabric_init_example_data```
7. Run the commands ```python python manage.py crono``` and ```python python manage.py runserver 0.0.0.0``` in separate
   terminals.
8. Repeat all the steps with all participant nodes.

# Ethereum

## Required software

- Python 3.9.15
- Solidity 0.8.18

## Installation

1. Download the repository and access it.
2. Execute the command ``pip install -r requirements.txt.``
3. Fill in the following environment variables

```bash
   export DJANGO_SETTINGS_MODULE=exchange_system.settings
   export EXCHANGE_SYSTEM_BLOCKCHAIN_LAYER='Ethereum'
   export EXCHANGE_SYSTEM_ENDPOINT=Public address of the node where you will expose the endpoint and other nodes will be able to consult the information you share
```

4. Run ```python python manage.py migrate```
5. Run ```python python manage.py raise_ethereum_config``` and follow the steps as per your use case.
6. Run the commands ```python python manage.py crono``` and ```python python manage.py runserver 0.0.0.0``` in separate
   terminals.
7. Repeat all the steps with all participant nodes.

## Ethereum docker example

If your sole intention is to test the software on an Ethereum network, you can execute the docker-compose found
at `ExampleDockers/Ethereum/docker-compose.yml`. This will instantiate an Ethereum network consisting of 2 nodes and
deploy 2 BRAIN clients along with their respective threads listening on ports 8000 and 8001:

**Note:** This requires Docker and docker-compose to be installed on your machine.

To execute the `docker-compose up -d` command in a terminal, navigate to the `exchange_system/ExampleDockers/Ethereum`
directory and run the command. Here are the steps:

1. Open a terminal.

2. Change directory to `exchange_system/ExampleDockers/Ethereum`. You can do this using the `cd` command followed by the
   path to the directory. For example:

```bash 
   cd exchange_system/ExampleDockers/Ethereum 
```

Once you are in the correct directory, execute the docker-compose up -d command. This command will start the containers
defined in the docker-compose.yml file in detached mode (in the background). Here's the command:

```bash 
   docker-compose up -d
```

Make sure you have Docker and docker-compose installed on your machine before executing this command.

