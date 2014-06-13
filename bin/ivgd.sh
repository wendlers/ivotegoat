#!/bin/bash

BASE=${PWD}
PYTHONPATH=${BASE}/server/src/
DB=${BASE}/server/db/ivotegote.db
DR=${BASE}/client/www
TMP=${BASE}/tmp

mkdir -p ${TMP}

python ${BASE}/server/src/ivg/server.py -B ${DB} -D ${DR} -p ${TMP}/ivgd.pid -l ${TMP}/ivgd.log -d
