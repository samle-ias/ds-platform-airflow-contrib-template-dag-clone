#!/bin/bash

set -ex

echo "Workspace is: ${WORKSPACE}"
echo "Workspace contents: $(ls $WORKSPACE)"

echo "Running flake8..."
flake8 .
