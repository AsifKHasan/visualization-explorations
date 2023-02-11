#!/usr/bin/env bash
# yml->dot->image pipeline

# usage
# ./mindmap-from-yml.sh YML [ENGINE] [FMT]

# ENGINE may be one of following. "neato" is the default
#   dot - hierarchical or layered drawings of directed graphs.
#   neato - "spring model" layouts.
#   fdp - Force-Directed Placement.
#   sfdp - Scalable Force-Directed Placement.
#   circo - circular layout.
#   twopi - radial layout.
#   nop - Pretty-print DOT graph file. Equivalent to nop1.
#   nop2 - Pretty-print DOT graph file, assuming positions already known.
#   osage - draws clustered graphs.
#   patchwork - draws map of clustered graph using a squarified treemap layout. 

# FMT may be one of jpg/png/pdf/svg. "svg" is the default


# parameters
YML=$1
ENGINE=$2
FMT=$3

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

# engine 
if [ -z ${ENGINE} ]; then
  ENGINE=neato
fi

echo "prcessing ${YML_NAME}: [FMT=${FMT}] [ENGINE=${ENGINE}]"

pushd ./out
dot -K${ENGINE} -T${FMT}${RENDERER} -o${YML_NAME}.${ENGINE}.${FMT} ${YML_NAME}.gv


if [ ${?} -ne 0 ];  then
  popd && exit 1
else
  popd
fi
