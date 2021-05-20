#! /bin/bash

python3 -m venv new_env

source new_env/bin/activate

pip3 install -r requirements.txt

python3 cron_setup.py

deactivate