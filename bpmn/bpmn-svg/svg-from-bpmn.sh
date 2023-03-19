#!/usr/bin/env bash
# bpmn->yml->svg image pipeline

# usage
# ./svg-from-bpmn.sh YML

# parameters
YML=$1

# set echo off
PYTHON=python3

# yml-to-bpmn
pushd ./src
${PYTHON} yml-to-bpmn.py --config "../conf/config.yml" --yml ${YML}

if [ ${?} -ne 0 ]; then
  popd && exit 1
else
  popd
fi
