'''
Created on Jun 26, 2018

@author: 19115678
'''

'''
put all amino acid sequence in the file titled @param "set_file_name" into a string
return the string
'''
def retrieve_sequence(set_file_name):
    list = ""
    with open(set_file_name) as f:
        for line in f:
            list += line.split("|")[1][:-1]
    return list

'''
put the secondary structure of amino acids in the file titled @param "set_file_name" into a string
return said string
'''
def retrieve_structure(set_file_name):
    list = ""
    with open(set_file_name) as f:
        for line in f:
            list += line.split("|")[1][:-1]
    return list

'''
precondition: sequence and structure are sorted in the right order (verified in purification verifier)
returns a dictionary of amino acid as keys and tuple of 3 value as value
The 3 values are the times which the amino acid of proteins listed in the @param set that 
has a secondary structure of H,E,C, respectively
'''
def get_frequency_table(sequence,classification):
    sequence = retrieve_sequence(sequence)
    structure = retrieve_structure(classification)
    freq = {"A":(0,0,0),  "R":(0,0,0),  "N":(0,0,0),  "D":(0,0,0),  "C":(0,0,0) , "Q":(0,0,0),  
            "E":(0,0,0),  "G":(0,0,0),  "H":(0,0,0),  "I":(0,0,0),  "L":(0,0,0) , "K":(0,0,0),  
            "M":(0,0,0),  "F":(0,0,0) , "P":(0,0,0) , "S":(0,0,0) , "T":(0,0,0)  ,"W":(0,0,0),
            "Y":(0,0,0) , "V":(0,0,0)}
    if len(sequence) != len(structure):
        print "Sequence and structure length are unmatched."
        return
    for i in range(len(sequence)):
        if sequence[i] not in freq.keys():
            freq[sequence[i]]= (0,0,0)
        h_count, e_count, c_count = freq[sequence[i]]
        if structure[i] == 'H':
            freq[sequence[i]] = (h_count+1,e_count,c_count)
        elif structure[i] == "E":
            freq[sequence[i]] = (h_count,e_count+1,c_count)
        elif structure[i] == "C":
            freq[sequence[i]] = (h_count,e_count,c_count+1)
    return freq

def can_get_tendency_factor(sequence, classification):
    classification_names = []
    with open(classification) as f:
        classification_names = [line.split("|")[0] for line in f]
    
    sequence_names = []
    with open(sequence) as f:
        sequence_names = [line.split("|")[0] for line in f]
   
    if len(classification_names) != len(sequence_names):
        print "Unable to get Tendency Factor."
        return False
    
    for i in range(len(sequence_names)):
        if sequence_names[i] != classification_names[i]:
            print "Unable to get tendency factor. Sequence and Classification unmatched."
            return False
    return True
    
'''
returns a dictionary of amino acid as keys and tuple of 3 numbers as value
The 3 numbers are the tendency factor used for training the SVM
'''
def get_tendency_factor(sequence, classification):
    if can_get_tendency_factor(sequence, classification):
        freq = get_frequency_table(sequence, classification)
        tendency = {}
        keys = freq.keys()
        for i in range(len(keys)):
            tendency[keys[i]] = (0,0,0)
            letter_h, letter_e, letter_c, other_h, other_e, other_c = (0,0,0,0,0,0)
            for key, val in freq.iteritems():
                if key == keys[i]:
                    letter_h, letter_e, letter_c = val              
                else:
                    h_count, e_count, c_count = val
                    other_h+=h_count
                    other_e+=e_count
                    other_c+=c_count
            tendency[keys[i]] = (letter_h/float(other_h),letter_e/float(other_e),letter_c/float(other_c))
        return tendency
    else:
        return None
        