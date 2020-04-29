#!/bin/sh

python3 parse.py --output data/output.csv
python3 parse.py --transpose --output data/output-transposed.csv 