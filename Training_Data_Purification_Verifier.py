'''
Created on Jun 27, 2018

@author: 19115678
'''

from Training_Data_Extraction_Verifier import missing_protein_num

'''
Evaluate the postcondition of purifying the data:
- All missing proteins are recorded in "Unavailable_Proteins.txt"
- The protein sequence and classification are in the same order
- The protein sequence and classification files are of same length
'''
def verify_purification():
    classification_names = []
    with open("Training_Classification.txt") as f:
        classification_names = [line.split("|")[0] for line in f]
    
    sequence_names = []
    with open("Training_Sequence.txt") as f:
        sequence_names = [line.split("|")[0] for line in f]
    
    important_proteins = []
    with open("cullpdb_pc30_res2.0_R0.25_d180607_chains11093.txt") as t:
        important_proteins = [line.split()[0] for line in t]
    important_proteins.pop(0)
   
    if len(classification_names) != len(sequence_names) or len(important_proteins) - missing_protein_num() != len(classification_names):
        print "Purification failed."
        return
    
    for i in range(len(sequence_names)):
        if sequence_names[i] != classification_names[i]:
            print "Purification failed. Protein", sequence_names[i], "sequence is matched with secondary structure of protein", classification_names[i]+"."
            return
    
    print "Purification successful."