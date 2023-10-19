#!/usr/bin/env bash
python3 bpmn_parser.py < ../data/$1.bpmn | tee ../out/$1.json | python3 bpmn_svg.py
