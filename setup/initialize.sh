#!/usr/bin/env bash

# Install app from local directory
"${TRAME_VENV}/bin/python" -m pip install -e /local-app || exit 1
