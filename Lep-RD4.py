#!/usr/bin/env python

import sys

# check arguments
if len(sys.argv) != 2:
    sys.stderr.write("usage: python Lep_RD.py <input_file>\n")
    sys.exit()

#allele function
def lep_notation(genotype, current_allele):
    if genotype == current_allele[0]:
        return "1 1"
    elif genotype == current_allele[2]:
        return "2 2"
    else:
        return "error"

#print header
def print_header(locus_names):
    header = "#Group" + "\t" + "IndID" + "\t" + "mom" + "\t" + "dad" + "\t" + "M/F" + "\t" + "B/W" + "\t"
    for locus_name in locus_names:
        header += locus_name + "\t"
    print(header.strip())

#impossible function
def impossible_genotypes(offspring_genotype, mom_genotype, dad_genotype):
    if mom_genotype in "ACTG" and dad_genotype in "ACTG" and mom_genotype == dad_genotype:
	if mom_genotype != offspring_genotype:
	    return True
    elif mom_genotype in "ACTG" and dad_genotype in "RYSWKM":
	if offspring_genotype != mom_genotype and offspring_genotype != dad_genotype:
	    return True
    elif mom_genotype in "RYSWKM" and dad_genotype in "ACTG":
	if offspring_genotype != mom_genotype and offspring_genotype != dad_genotype:
	    return True
    else:
	return False
#get individual info 
def get_ind_info(columns):
    indID = columns[0] #looks like 8_3_2_2F or B8_3_2_2_10M
    indfields = indID.split("_")
    genotypes = columns[1:]
    if indfields[3].startswith("2"):
        group = 2
    elif indfields[3].startswith("1"):
        group = 1
    else:
        group = 5
    return indfields, indID, group, genotypes

# open file
with open(sys.argv[1]) as inputfile:

    # read each line of the file
    for line in inputfile:
        if line.startswith("rs#"): 
            #this is the first line
	    locus_names = line.strip().split()[1:]
            print_header(locus_names)
        elif line.startswith("alleles"):
            #this is the second line
            alleles = line.strip().split()[1:]
        else:
	    isoffspring = True
            columns = line.split()
            indfields, indID, group, genotypes = get_ind_info(columns)
            if indID.startswith("8"):
		isoffspring = False
                father = 0
                mother = 0
		if indID.endswith("F"):
		    mom_genotypes = genotypes
		elif indID.endswith("M"):
		    dad_genotypes = genotypes
		else:
		    print "error"
            else:
                father = "8"+"_"+indfields[1]+"_"+indfields[2]+"_"+indfields[3]+"M"
                mother = "8"+"_"+indfields[1]+"_"+indfields[2]+"_"+indfields[3]+"F"
            if indfields[0].startswith("B"):
                affected = 1
            elif indfields[0].startswith("W"):
                affected = 2
            else:
                affected = 1
            if indID.endswith("M"):
                sex = 2
            else:
                sex = 1
            locusgenotype = [] 
            newline = str(group) + "\t" + str(indID) + "\t" + str(mother) + "\t" + str(father) + "\t" + str(sex) + "\t" + str(affected) + "\t"
            for i, genotype in enumerate(genotypes):
                current_allele = alleles[i]
		if isoffspring:
		    current_mom_allele = mom_genotypes[i]
		    current_dad_allele = dad_genotypes[i]
		    if impossible_genotypes(genotype, current_mom_allele, current_dad_allele): 
			genotype = "N"	
                if genotype in "ACGT":
                    locusgenotype.append(lep_notation(genotype, current_allele))
                elif genotype in "RYSWKM":
                    locusgenotype.append("1 2")
                elif genotype == "N":
                    locusgenotype.append("0 0")
                else:
                    locusgenotype.append("ntc") 
	    for geno in locusgenotype:
	        newline += geno + "\t"
            print(newline.strip())

