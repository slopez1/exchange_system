# BRAIN
BRAIN is described as a sophisticated and modular framework that utilizes blockchain technology to provide an innovative and smart solution for fostering collaboration, trust, and competitiveness among entities in a highly interconnected world. BRAIN is designed to address the challenges of secure data exchange and information sharing among entities. It offers features like flexibility, efficiency, security, robustness, and scalability, without the need for intermediaries, to improve productivity and collaboration between entities. BRAIN is intended to serve as a configurable foundation for the development of domain-specific applications, offering a secure and efficient data exchange platform.


## Required software

- Python 3.9.15
- Fabric binaries (Instructions: https://hyperledger-fabric.readthedocs.io/en/release-2.2/install.html)
- Go version 1.20.x (To install Fabric Smart contract)

## Installation

1. Download the repository and access it.
2. Execute the command ``pythonpip install -r requirements.txt.``
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
6. Modify the field /exchange_system/fabric/management/commands/fabric_init_example_data.py, changing the parameters of PeerNode.objects.create and OrdererNode.objects.create to match your use case, and then run ```python python manage.py fabric_init_example_data```
7. Run the commands ```python python manage.py crono``` and ```python python manage.py runserver 0.0.0.0``` in separate terminals.
8. Repeat all the steps with all participant nodes.


# Ethereum
## Requeriments:
1. brew install solidity
2. 