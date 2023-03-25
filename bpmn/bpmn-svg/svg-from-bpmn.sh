#!/usr/bin/env bash
# bpmn->yml->svg image pipeline

# usage
# ./svg-from-bpmn.sh BPMN

# parameters
BPMN=$1

# set echo off
PYTHON=python3

# bpmn-to-yml
pushd ./bpmn-to-yml/src
# ${PYTHON} yml-from-bpmn.py --config "../conf/config.yml" --bpmn ${BPMN_NAME}

if [ ${?} -ne 0 ]; then
  popd && exit 1
else
  popd
fi

# get the actual yml name without path prefix
IFS=$'/'; strarr=($BPMN); unset IFS;
YML_NAME=${strarr[-1]}


# yml-to-svg
pushd ./yml-to-svg/src
${PYTHON} svg-from-yml.py --config "../conf/config.yml" --yml ${YML_NAME}

if [ ${?} -ne 0 ]; then
  popd && exit 1
else
  popd
fi
