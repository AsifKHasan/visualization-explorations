#!/usr/bin/env bash
# yml->dot->bpmn image pipeline

# usage
# ./bpmn-from-yml.sh YML [DIR]

# DIR may be LR or TB. "LR" is the default

# parameters
YML=$1
DIR=$2

# set echo off
PYTHON=python3

# DIR
if [ -z ${DIR} ]; then
  DIR="LR"
elif [ "${DIR}" != "LR" ] && [ "${DIR}" != "TB" ]; then
  DIR="LR"
fi

# yml-to-bpmn
pushd ./src
${PYTHON} yml-to-bpmn.py --config "../conf/config.yml" --yml ${YML} --dir ${DIR}

if [ ${?} -ne 0 ]; then
  popd && exit 1
else
  popd
fi

# dot -> SVG
# get the actual yml name without path prefix
IFS=$'/'; strarr=($YML); unset IFS;
YML_NAME=${strarr[-1]}

echo "prcessing ${YML_NAME}: [DIR=${DIR}]"

pushd ./out
dot -Kdot -Tsvg -o${YML_NAME}.svg ${YML_NAME}.gv

if [ ${?} -ne 0 ];  then
  popd && exit 1
else
  popd
fi

# post process SVG
echo "post processing ${YML_NAME}.svg: [DIR=${DIR}]"

pushd ./src
${PYTHON} svg-post-process.py --config "../conf/config.yml" --svg ${YML_NAME}.svg --dir ${DIR}

if [ ${?} -ne 0 ]; then
  popd && exit 1
else
  popd
fi
