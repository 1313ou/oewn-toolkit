#!/bin/bash

source .venv/bin/activate
python3 read_definitions.py oewn-2024-sqlite-2.1.1.sqlite
deactivate
