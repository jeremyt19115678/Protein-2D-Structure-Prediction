'''
Created on Jun 21, 2018

@author: 19115678
'''

'''
return the number of missing proteins
'''
def missing_protein_num():
    with open("Unavailable_Proteins.txt") as f:
        missing_proteins = f.read().split("\n")
        missing_proteins.pop(-1)
    return len(missing_proteins)

'''
main function called by runner
Evaluate a rudimentary test for Data viability
Conditions include:
- Protein Structures and Sequence have the same amount of data
- Amount of missing proteins is noted
- Protein structure and sequence do not have repeating data entries
'''
def verify_training_data():
    missing_num = missing_protein_num()
    
    classification = []
    with open("Training_Sequence.txt") as f:
        classification = [line.split("|")[0] for line in f]
        
    sequence = []
    with open("Training_Classification.txt") as f:
        sequence = [line.split("|")[0] for line in f]
        
    important_proteins = []
    with open("cullpdb_pc30_res2.0_R0.25_d180607_chains11093.txt") as t:
        important_proteins = [line.split()[0][0:4]+":"+line.split()[0][4:] for line in t]
    important_proteins.pop(0)
    
    checklist = [len(classification) == len(sequence), len(important_proteins)-missing_num == len(sequence), 
                 len(set(classification)) == len(classification), len(set(sequence)) == len(sequence)]
    
    error_message = {0:"Training input and output are of different length.\nTraining_Sequence.txt has " + str(len(sequence)) + 
                      " entries. Training_Classification.txt has " + str(len(classification)) + " entries.",
                      1:"Training data entries number " + str(len(sequence)) + ", but it should be " + str(len(important_proteins)-missing_num)+".",
                      2:"Training_Classification.txt contains repeating entries.",3:"Training_Sequence.txt contains repeating entries"}
    for i in range(len(checklist)):
        if checklist[i] == False:
            print "Data failed to pass verification."
            print error_message[i]
            return
    print "Data verified as functional."