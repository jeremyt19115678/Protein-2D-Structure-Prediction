'''
Created on Jun 21, 2018

@author: 19115678
'''

import os
from Secondary_Structure_Converter_v2 import all_set_filepath
from __builtin__ import file
from Data_Principal_Component_Analyzer import flip_matrix

'''
return a list of the secondary structure lengths of proteins
retrieved from the database
'''
def get_length(filepath):
    with open(filepath) as t:
        lengths = [len(line.split("|")[1][:-1]) for line in t]
    return lengths

'''
called by Runner
Evaluate whether transformation is valid:
- Valid only if the length of protein secondary structures are the same.
'''
def verify_transformation():
    sets = all_set_filepath()
    for dataset in sets:
        #get original length for training
        original_training_length = get_length(os.path.join(dataset,"SVM_Training_Categorical_Label.txt"))
        original_testing_length = get_length(os.path.join(dataset,"SVM_Testing_Categorical_Label.txt"))
        original_reference_length = get_length(os.path.join(dataset,"SVM_Reference_Categorical_Label.txt"))
        test_translate = []
        train_translate = []
        ref_translate = []
        for i in range(5):
            filename = "SVM_Training_Classification_Transformed_Rule_" + str(i+1) + ".txt"
            path = os.path.join(dataset,filename)
            train_translate.append(path)
            filename = "SVM_Testing_Classification_Transformed_Rule_" + str(i+1) + ".txt"
            path = os.path.join(dataset,filename)
            test_translate.append(path)
            filename = "SVM_Reference_Classification_Transformed_Rule_" + str(i+1) + ".txt"
            path = os.path.join(dataset,filename)
            ref_translate.append(path)
        test_translate_length = []
        train_translate_length = []
        ref_translate_length = []
        for file in test_translate:
            test_translate_length.append(get_length(file))
        for file in train_translate:
            train_translate_length.append(get_length(file))
        for file in ref_translate:
            ref_translate_length.append(get_length(file))
        for i in range(len(original_training_length)):
            lengths = []
            lengths.append(original_training_length[i])
            for j in range(len(train_translate_length)):
                lengths.append(train_translate_length[j][i])
            if len(set(lengths)) != 1:
                print "Transformation failed."
                print dataset
                return
        for i in range(len(original_testing_length)):
            lengths = []
            lengths.append(original_testing_length[i])
            for j in range(len(test_translate_length)):
                lengths.append(test_translate_length[j][i]) 
            if len(set(lengths)) != 1:
                print "Transformation failed."
                print dataset
                return
        for i in range(len(original_reference_length)):
            lengths = []
            lengths.append(original_reference_length[i])
            for j in range(len(ref_translate_length)):
                lengths.append(ref_translate_length[j][i]) 
            if len(set(lengths)) != 1:
                print "Transformation failed."
                print dataset
                return
        print "Transformation successful"