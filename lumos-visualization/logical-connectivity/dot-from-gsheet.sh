#!/usr/bin/env bash
# gsheet->json->dot->png pipeline

# parameters
DOCUMENT=$1
WORKSHEET=$2

# set echo off
PYTHON=python3

# json-from-gsheet
pushd ./gsheet-to-json/src
# ${PYTHON} json-from-gsheet.py --config "../conf/config.yml" --gsheet ${DOCUMENT} --worksheet ${WORKSHEET}

if [ ${?} -ne 0 ]; then
  popd && exit 1
else
  popd
fi

# dot-from-json
pushd ./json-to-dot/src
${PYTHON} dot-from-json.py --config "../conf/config.yml" --json ${WORKSHEET}

if [ ${?} -ne 0 ]; then
  popd && exit 1
else
  popd
fi

# dot -> png
pushd ./out

FMT=png
ENGINE=dot
dot -K${ENGINE} -T${FMT} -o${WORKSHEET}.${FMT} ${WORKSHEET}.gv


if [ ${?} -ne 0 ];  then
  popd && exit 1
else
  popd
fi
