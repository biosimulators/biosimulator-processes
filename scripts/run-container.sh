#!/bin/bash

version="$1"

if [ "${version}" == "" ]; then
  echo "Please enter the version you would like to run as a runtime arg. Exiting."
  exit 1
fi

docker run -d \
  --platform linux/amd64 \
  -p 8888:8888 \
  --name biosimulator-processes-container \
  ghcr.io/biosimulators/biosimulator-processes:"${version}" \
  sh -c "poetry run jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root"
