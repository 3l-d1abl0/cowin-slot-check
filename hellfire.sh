#! /bin/bash

cd $1

source new_env/bin/activate

python3 cowin_api.py

deactivate