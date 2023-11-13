#!/usr/bin/env bash
# yml->dot->bpmn image pipeline

# usage
# ./bpmn-from-yml.sh YML [FMT]

# FMT may be one of jpg/png/pdf/svg. "svg" is the default

# parameters
YML=$1
FMT=$2

# set echo off
PYTHON=python3

# yml-to-bpmn
pushd ./src
# ${PYTHON} yml-to-bpmn.py --config "../conf/config.yml" --yml ${YML}

if [ ${?} -ne 0 ]; then
  popd && exit 1
else
  popd
fi

# dot -> FMT
# get the actual yml name without path prefix
IFS=$'/'; strarr=($YML); unset IFS;
YML_NAME=${strarr[-1]}

# format
if [ -z ${FMT} ]; then
  FMT=svg
  RENDERER=":cairo:cairo"
elif [ ${FMT} == "svg" ]; then
  RENDERER=":cairo:cairo"
else
  RENDERER=""
fi

echo "prcessing ${YML_NAME}: [FMT=${FMT}]"

pushd ./out
# dot -Kdot -T${FMT}${RENDERER} -o${YML_NAME}.${FMT} ${YML_NAME}.gv
dot -Kdot -T${FMT} -o${YML_NAME}.${FMT} ${YML_NAME}.gv

if [ ${?} -ne 0 ];  then
  popd && exit 1
else
  popd
fi
