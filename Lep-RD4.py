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
    ind = columns[0] #looks like 8_3_2_2F or B8_3_2_2_10M
    individual = {}
    individual["ID"] = ind
    ind_info = ind.strip().split("_")
    if ind_info[3].startswith("1"):
        individual["group"] = 1
    elif ind_info[3].startswith("2"):
        individual["group"] = 2
    else:
        individual["group"] = 5
    if ind[0].startswith("8"):
        individual["mother"] = 0
        individual["father"] = 0
    else:
        individual["mother"] = "8" + "_" + ind_info[1] + "_" + ind_info[2] + "_" + ind_info[3] + "F"
        individual["father"] = "8" + "_" + ind_info[1] + "_" + ind_info[2] + "_" + ind_info[3] + "M"
    if ind_info[-1].endswith("F"):
        individual["sex"] = 1
    else:
        individual["sex"] = 2
    if ind_info[0].startswith("W"):
        individual["affected"] = 2
    else:
        individual["affected"] = 1
    if individual["mother"] == 0 and individual["father"] == 0:
        individual["isoffspring"] = False
    else:
        individual["isoffspring"] = True
    return individual 

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
            columns = line.split()
            genotypes = columns[1:]
            individual_info = get_ind_info(columns)
            group = individual_info['group']
            ID = individual_info['ID']
            mother = individual_info['mother']
            if individual_info['isoffspring'] == False and individual_info['sex'] == 1:
                mom_genotypes = genotypes
            elif individual_info['isoffspring'] == False and individual_info['sex'] == 2:
                dad_genotypes = genotypes
            father = individual_info['father']
            sex = individual_info['sex']
            affected = individual_info['affected']
            isoffspring = individual_info['isoffspring']
            locusgenotype = []
            newline = str(group) + "\t" + str(ID) + "\t" + str(mother) + "\t" + str(father) + "\t" + str(sex) + "\t" + str(affected) + "\t"
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

