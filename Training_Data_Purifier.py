'''
Created on Jun 26, 2018

@author: 19115678
'''

import os
from Training_Data_Extractor import create_file

'''
return a dictionary of amino acid sequence for proteins in training set
'''
def get_all_sequence():
    sequence = []
    with open("Training_Sequence.txt") as f:
        sequence = [line.split("|") for line in f]
    dict = {name:sequence[:-1] for (name,sequence) in sequence}
    return dict

'''
record key (a string of a protein's name) into "Unavailable_Proteins.txt"
'''
def write_unavailable(key):
    file = open("Unavailable_Proteins.txt", "a+")
    file.write(key+"\n")
    file.close()

'''
return a "purified" version of the @param "dict"
'''
def remove_unavailable(dict):
    new = {}
    for key,value in dict.iteritems():
        if 'X' not in value and 'B' not in value and 'O' not in value and 'U' not in value:
            new[key] = value
        else:
            write_unavailable(key)
    return new

'''
write a new file "new_sequence.txt" based on dictionary @param dict
the dict is sorted before it's written into the file
the file contains the amino acid sequence and the name of proteins
'''
def write_file(dict):
    filename = "new_sequence.txt"
    keylist = dict.keys()
    keylist.sort()
    file = open(filename,"a+")
    for key in keylist:
        file.write (key+"|"+dict[key]+"\n")
    file.close()

'''
write a new file "new_secondary_structure.txt" containing secondary structure of proteins specified
in @param list
'''
def update_secondary_structure(list):
    filename = "new_secondary_structure.txt"
    classification = []
    with open("Training_Classification.txt") as f:
        classification = [line.split("|") for line in f]
    dict = {name:sequence[:-1] for (name,sequence) in classification if name in list}
    #write into file
    keylist = dict.keys()
    keylist.sort()
    file = open(filename,"a+")
    for key in keylist:
        file.write (key+"|"+dict[key]+"\n")
    file.close()

'''
called by the runner
creates temporary file "new_sequence.txt" and "new_secondary_structure.txt"
deletes their predecessor "Training_Sequence.txt" and "Training_Classification.txt"
renames temporary file to their predecessors
''' 
def purify_data():
    create_file("new_sequence.txt")
    create_file("new_secondary_structure.txt")
    sequence = get_all_sequence()
    new_seq = remove_unavailable(sequence)
    write_file(new_seq)
    update_secondary_structure(new_seq.keys())
    os.remove("Training_Sequence.txt")
    os.remove("Training_Classification.txt")
    os.rename("new_sequence.txt", "Training_Sequence.txt")
    os.rename("new_secondary_structure.txt", "Training_Classification.txt")