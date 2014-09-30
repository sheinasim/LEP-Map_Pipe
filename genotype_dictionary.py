#!/usr/bin/env python

import sys

# check arguments
if len(sys.argv) != 3:
    sys.stderr.write("usage: python full_dictionary.py <OM_file> <genotype_file>\n")
    sys.exit()

# open file
map = {}

with open(sys.argv[1]) as map_file:
    #turn map file into key
    for line in map_file:
        columns = line.strip().split("\t")
        if len(columns) < 2:
            continue
        map[columns[0]] = columns[1]

name = {}

with open(sys.argv[2]) as name_file:
    #turn name file into key
    for line in name_file:
        columns = line.strip().split("\t")
        if len(columns) < 281:
            continue
        name[columns[0]] = [column for column in columns[1:]]

if not map:
    print("Error reading map file")
    exit()

if not name:
    print("Error reading name file")
    exit()

joined = {}
for locus in map:
    print(locus+'\t'+map[locus]+'\t'+'\t'.join(name[locus]))

