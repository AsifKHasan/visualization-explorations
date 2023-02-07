#!/usr/bin/env bash
# yml->dot->image pipeline

# parameters
YML=$1

# set echo off
PYTHON=python3

# yml-to-mindmap
pushd ./src
${PYTHON} yml-to-mindmap.py --config "../conf/config.yml" --yml ${YML}

if [ ${?} -ne 0 ]; then
  popd && exit 1
else
  popd
fi

# dot -> FMT
:: get the actual yml name without path prefix

pushd ./out

FMT=svg
# FMT=png
RENDERER=":cairo:cairo"
# RENDERER=":svg:core"
ENGINE=neato
dot -K${ENGINE} -T${FMT}${RENDERER} -o${YML}.${FMT} ${YML}.gv


if [ ${?} -ne 0 ];  then
  popd && exit 1
else
  popd
fi
