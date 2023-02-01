#!/usr/bin/env bash
# yml->dot->png pipeline

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

# dot -> png
pushd ./out

FMT=svg
RENDERER=":cairo:cairo"
# RENDERER=":svg:core"
ENGINE=neato
dot -K${ENGINE} -T${FMT}${RENDERER} -o${YML}.${FMT} ${YML}.gv


if [ ${?} -ne 0 ];  then
  popd && exit 1
else
  popd
fi
