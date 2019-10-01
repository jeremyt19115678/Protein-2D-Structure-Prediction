'''
Created on Jun 22, 2018

@author: 19115678
'''

classification_file_name = "Training_Classification.txt"
sequence_file_name = "Training_Sequence.txt"


'''
return a "shopping list" (dictionary)of all desired 
proteins
'''
def get_desired_proteins():
    #create list of desired proteins
    important_proteins = []
    with open("cullpdb_pc30_res2.0_R0.25_d180607_chains11093.txt") as t:
        important_proteins = [line.split()[0][0:4]+":"+line.split()[0][4:] for line in t]
    important_proteins.pop(0)
    dict = {}
    for i in important_proteins:
        dict[i] = False
    return dict

'''
return a list of all data
'''
def get_all_data():
    contents = []
    with open("ss.txt") as database:
        contents = database.read().split(">")
    return contents

'''
remove all colons and "\n" and return a tuple
(protein name, data type, data)
'''
def transform(entry):
    lines = entry.split("\n") #create one long list of data
    name_and_list = lines[0].split(":") #split into a list of length 3
    name = name_and_list[0]+name_and_list[1]
    data_type = name_and_list[2]
    data = ""
    for i in lines[1:]:
        data += i
    return (name,data_type,data)
    
'''
return the name of the protein including the colon
ex) 101M:A
'''
def name_of(entry):
    if len(entry) > 6:
        return entry[0:6]
    else:
        return ""   

'''
append the entry into different files based on
datatype
'''
def append(entry):
    name,data_type,data = transform(entry)
    if data_type == "sequence":
        seq_file = open(sequence_file_name,"a+")
        seq_file.write(name+"|"+data+"\n")
        seq_file.close()
    elif data_type == "secstr":
        class_file = open(classification_file_name,"a+")
        class_file.write(name+"|"+data+"\n")
        class_file.close()

'''
create the files named filename
'''
def create_file(filename):
    file = open(filename,"w")
    file.close()

'''
create a text file containing proteins not available in the database
'''
def record_missing_proteins(dict):
    create_file("Unavailable_Proteins.txt")
    missing_file = open("Unavailable_Proteins.txt", "a+")
    for key,value in dict.iteritems():
        if value == False:
            missing_file.write(key[0:4]+key[5:]+"\n")
    missing_file.close()

'''
main function called by runner
creates 3 files:
1) Training_Classification.txt containing protein names and their 2D structure
2) Training_Sequence.txt containing protein names and their amino acid sequence
3) Unavailable_Proteins.txt containing names of queried proteins that are not in database

'''
def create_training_data():
    protein_dict = get_desired_proteins()
    database = get_all_data()
    create_file(classification_file_name)
    create_file(sequence_file_name)
    for entry in database:
        if name_of(entry) in protein_dict.keys():
            protein_dict[name_of(entry)] = True
            append(entry)
    record_missing_proteins(protein_dict)
    print "Training Datasets Created. Missing Proteins are recorded in Unavailable_Proteins.txt"