#!/usr/bin/env bash

# Install conda dependencies
conda install -y -c conda-forge festim matplotlib fenics-dolfinx

# Install app from local directory
python -m pip install /local-app
