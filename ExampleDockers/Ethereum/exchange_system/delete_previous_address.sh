#!/bin/bash

DIRECTORY="ExampleDockers/Ethereum/exchange_system/healthcheck"

# Called by the first initialization container, checks that an address file from a previous execution does not exist, if it exists it deletes it

if [ -f "$DIRECTORY/address" ]; then
  echo "Deleting 'address' file..."
  rm "$DIRECTORY/address"
else
  echo "'address' file does not exist."
fi
