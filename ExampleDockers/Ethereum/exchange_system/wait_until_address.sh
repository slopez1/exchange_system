#!/bin/bash

DIRECTORY="ExampleDockers/Ethereum/exchange_system/healthcheck"

# Checks if the initial container has already acquired the smart contract in the test network

while [ ! -f "$DIRECTORY/address" ]; do
  echo "Waiting for 'address' file..."
  sleep 1
done

echo "'address' file found."
