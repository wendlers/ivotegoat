#!/bin/bash

BASE=${PWD}
PYTHONPATH=${BASE}/server/src/

python ${BASE}/server/src/ivg/client.py $@ 
