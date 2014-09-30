#!/usr/bin/env python

import sys

# check arguments
if len(sys.argv) != 2:
    sys.stderr.write("usage: python Lep_RD.py <input_file>\n")
    sys.exit()
#allele function
def lep_notation(genotype, current_allele):
    if genotype == current_allele[0]:
        return "A"
    elif genotype == current_allele[1]:
        return "B"
    else:
        return "error"

# open file
with open(sys.argv[1]) as inputfile:

    # read each line of the file
    for line in inputfile:
        if line.startswith("rs#"): 
            header = line.split()
	    IDs = header[4:]
	    print header[0]+"\t"+header[2]+"\t"+"\t".join(header[4:])
        elif line.startswith("alleles"):
            allele = line.strip().split()[1:]
        else:
            columns = line.split()
            locus_name = columns[0]
	    allele = columns[1].strip().split("/")
	    chrom = columns[2]
            position = columns[3]
            genotypes = columns[4:]
            locusgenotype = [] 
            for genotype in genotypes:
            	if genotype in "ACGT":
                    locusgenotype.append(lep_notation(genotype, allele))
                elif genotype in "RYSWKM":
                    locusgenotype.append("H")
                elif genotype == "N":
                    locusgenotype.append("-")
                else:
                    locusgenotype.append("ntc") 
            print locus_name+"\t"+"\t".join(locusgenotype)

 
