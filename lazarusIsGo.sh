#! /bin/bash

python -m venv new_env

pip install -r requirements.txt

source new_env/bin/activate

python cron_setup.py

deactivate