#!/usr/bin/env bash
# yml->svg pipeline

# parameters
YML=$1

# set echo off
PYTHON=python3

# yml-to-svg
pushd ./src
${PYTHON} yml-to-svg.py --config "../conf/config.yml" --yml ${YML}

if [ ${?} -ne 0 ]; then
  popd && exit 1
else
  popd
fi
