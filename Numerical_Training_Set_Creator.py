'''
Created on Jun 28, 2018

@author: 19115678
'''

import numpy as np
from Training_Data_Extractor import create_file
from Tendency_Factor_Calculator import get_tendency_factor
from Data_Principal_Component_Analyzer import get_given_principal_components
from Secondary_Structure_Converter_v2 import all_set_filepath
from random import shuffle
import code
import os
from numpy import number

'''
return a dictionary with protein name as key and amino acid sequence as value
'''
def get_all_sequence():
    with open("Training_Sequence.txt") as f:
        return {line.split("|")[0]:line.split("|")[1][:-1] for line in f}

'''
return number of lines in a file
'''
def length_of(fname):
    list = []
    with open(fname) as f:
        list = [1 for line in f]
    return len(list)

'''
return a dictionary with protein name as key and secondary structure as value
'''
def get_all_classification():
    with open("Training_Classification.txt") as f:
        return {line.split("|")[0]:line.split("|")[1][:-1] for line in f}

'''
'''
def get_string(filename):
    with open(filename) as f:
        list = [line.split("|")[1][:-1] for line in f]
    return ''.join(list)

'''
create a directory of 6 files for 3 purposes (training, reference, and testing)
for each purpose there are both feature and label
@param proportion dictates how much of the proteins in the database be used in training and reference
'''
def split_categorical_data(proportion):
    path = os.path.realpath("Training_Set_1")
    while os.path.exists(path):
        path = path[:-1] + str(int(path[-1])+1)
    os.mkdir(path)
    
    sequence = get_all_sequence()
    classification = get_all_classification()
    
    if len(classification.keys()) != len(sequence.keys()):
        print "classification and sequence are of different length"
        return
    if proportion*len(classification) < 1 and proportion*len(classification) > 0:
        print "proportion too small"
        return
    elif proportion >= 1 or proportion <= 0:
        print "proportion must be within (0,1)"
        return
    
    create_file(os.path.join(path,"SVM_Training_Categorical_Feature.txt"))
    create_file(os.path.join(path,"SVM_Training_Categorical_Label.txt"))
    create_file(os.path.join(path,"SVM_Testing_Categorical_Feature.txt"))
    create_file(os.path.join(path,"SVM_Testing_Categorical_Label.txt"))
    create_file(os.path.join(path,"SVM_Reference_Categorical_Feature.txt"))
    create_file(os.path.join(path,"SVM_Reference_Categorical_Label.txt"))
    
    keylist = classification.keys()
    shuffle(keylist)
    training_length = proportion*len(classification)
    for i in range(len(keylist)):
        if i < training_length:
            file = open(os.path.join(path,"SVM_Training_Categorical_Feature.txt"),"a+") 
            file.write(keylist[i]+"|"+sequence[keylist[i]]+"\n")
            file.close()
            file = open(os.path.join(path,"SVM_Training_Categorical_Label.txt"),"a+")
            file.write(keylist[i]+"|"+classification[keylist[i]] + "\n")
            file.close()
        elif i < 2*training_length:
            file = open(os.path.join(path,"SVM_Reference_Categorical_Feature.txt"),"a+")
            file.write(keylist[i]+"|"+sequence[keylist[i]]+"\n")
            file.close()
            file = open(os.path.join(path,"SVM_Reference_Categorical_Label.txt"),"a+")
            file.write(keylist[i]+"|"+classification[keylist[i]] + "\n")
            file.close()
        else:
            file = open(os.path.join(path,"SVM_Testing_Categorical_Feature.txt"),"a+") 
            file.write(keylist[i]+"|"+sequence[keylist[i]]+"\n")
            file.close()
            file = open(os.path.join(path,"SVM_Testing_Categorical_Label.txt"),"a+")
            file.write(keylist[i]+"|"+classification[keylist[i]] + "\n")
            file.close()
    if length_of(os.path.join(path,"SVM_Training_Categorical_Feature.txt")) + length_of(os.path.join(path,"SVM_Testing_Categorical_Feature.txt")) + length_of(os.path.join(path,"SVM_Reference_Categorical_Feature.txt"))== len(keylist):
        print "successful separation"
        
'''
Quantify the training data by amino acid.
Six numbers are used to represent one single amino acid
'''
def quantify_data():
    sets = all_set_filepath()
    classification_to_number = {"H":0, "E": 1, "C":2}
    pc = get_given_principal_components()
    for dataset in sets:
        train_classification_file = []
        train_sequence_file = os.path.join(dataset,"SVM_Training_Categorical_Feature.txt")
        train_sequence = get_string(train_sequence_file)
        for i in range(5):
            filename = "SVM_Training_Classification_Transformed_Rule_" + str(i+1) + ".txt"
            train_classification_file.append(os.path.join(dataset,filename))
        for file in train_classification_file:
            print file
            number = file[-5]
            tf = get_tendency_factor(train_sequence_file, file)
            classification = get_string(file)
            filename = os.path.join(dataset,"SVM_Training_Feature_" + number + ".txt")
            create_file(filename)
            filename = os.path.join(dataset,"SVM_Training_Label_" + number + ".txt")
            create_file(filename)
            list = []
            for i in range(len(classification)):
                code = tf[train_sequence[i]] + pc[train_sequence[i]]
                a,b,c,d,e,f = code
                code = (a,b,c,d,e,f,classification_to_number[classification[i]])
                list.append(code)
            for a,b,c,d,e,f,g in list:
                file = open(os.path.join(dataset,"SVM_Training_Feature_" + number + ".txt"), "a+")
                file.write(str(round(a,2))+","+str(round(b,2))+","+str(round(c,2))+","+str(round(d,2))+","+str(round(e,2))+","+str(round(f,2))+"\n")
                file.close()
                file = open(os.path.join(dataset,"SVM_Training_Label_" + number + ".txt"), "a+")
                file.write(str(g) + "\n")
                file.close()