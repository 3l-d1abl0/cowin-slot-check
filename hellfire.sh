#! /bin/bash

cd $1

source new_env/bin/activate

python cowin_api.py

deactivate