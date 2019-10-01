# uncompyle6 version 3.4.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.4 (tags/v3.7.4:e09359112e, Jul  8 2019, 19:29:22) [MSC v.1916 32 bit (Intel)]
# Embedded file name: /home/jeremyt/Post_Internship_Work/Secondary_Structure_Converter_v2.py
# Compiled at: 2018-07-05 02:20:29
"""
Created on Jun 21, 2018

@author: 19115678
"""
import os

def create_file(filename):
    file = open(filename, 'w')
    file.close()


def transform_rule(rule_number):
    dict = {}
    if rule_number == 1:
        dict = {'H': 'H', 'G': 'H', 'I': 'H', 'E': 'E', 'B': 'C', 'T': 'C', 'S': 'C', ' ': 'C'}
    elif rule_number == 2:
        dict = {'H': 'H', 'G': 'H', 'I': 'C', 'E': 'E', 'B': 'E', 'T': 'C', 'S': 'C', ' ': 'C'}
    elif rule_number == 3:
        dict = {'H': 'H', 'G': 'H', 'I': 'C', 'E': 'E', 'B': 'C', 'T': 'C', 'S': 'C', ' ': 'C'}
    elif rule_number == 4:
        dict = {'H': 'H', 'G': 'C', 'I': 'C', 'E': 'E', 'B': 'E', 'T': 'C', 'S': 'C', ' ': 'C'}
    elif rule_number == 5:
        dict = {'H': 'H', 'G': 'C', 'I': 'C', 'E': 'E', 'B': 'C', 'T': 'C', 'S': 'C', ' ': 'C'}
    return dict


def transform(dict, descriptor):
    newList = ''
    for i in descriptor:
        newList += dict[i]

    return newList


def write_file(file, name, descriptor):
    rule = int(file[(-5)])
    descriptor = transform(transform_rule(rule), descriptor)
    f = open(file, 'a+')
    f.write(name + '|' + descriptor + '\n')
    f.close()


def all_set_filepath():
    sets = []
    path = os.path.realpath('Training_Set_1')
    while os.path.exists(path):
        sets.append(path)
        path = path[:-1] + str(int(path[(-1)]) + 1)

    return sets


def transform_secondary_structure():
    sets = all_set_filepath()
    for set in sets:
        test_translate = []
        train_translate = []
        ref_translate = []
        for i in range(5):
            filename = 'SVM_Training_Classification_Transformed_Rule_' + str(i + 1) + '.txt'
            path = os.path.join(set, filename)
            create_file(path)
            train_translate.append(path)
            filename = 'SVM_Testing_Classification_Transformed_Rule_' + str(i + 1) + '.txt'
            path = os.path.join(set, filename)
            create_file(path)
            test_translate.append(path)
            filename = 'SVM_Reference_Classification_Transformed_Rule_' + str(i + 1) + '.txt'
            path = os.path.join(set, filename)
            create_file(path)
            ref_translate.append(path)

        with open(os.path.join(set, 'SVM_Training_Categorical_Label.txt')) as (data):
            for line in data:
                name, structure_descriptor = line.split('|')[0], line.split('|')[1][:-1]
                for file in train_translate:
                    write_file(file, name, structure_descriptor)

        with open(os.path.join(set, 'SVM_Testing_Categorical_Label.txt')) as (data):
            for line in data:
                name, structure_descriptor = line.split('|')[0], line.split('|')[1][:-1]
                for file in test_translate:
                    write_file(file, name, structure_descriptor)

        with open(os.path.join(set, 'SVM_Reference_Categorical_Label.txt')) as (data):
            for line in data:
                name, structure_descriptor = line.split('|')[0], line.split('|')[1][:-1]
                for file in ref_translate:
                    write_file(file, name, structure_descriptor)