'''
Created on Jun 27, 2018

@author: 19115678
'''
from timeit import itertools
from math import sqrt

amino_acid_order = "ACDEFGHIKLMNPQRSTVWY"

def get_attributes_combinations():
    list = [i for i in range(8)]
    i = itertools.combinations(list,3)
    combinations = [item for item in i]
    return combinations

def get_similarity(vector_a, vector_b):
    x_a, y_a, z_a = vector_a
    x_b, y_b, z_b = vector_b
    return (x_a*x_b+y_a*y_b+z_a*z_b)/sqrt(x_a**2+y_a**2+z_a**2)/sqrt(x_b**2+y_b**2+z_b**2)

def transform(list):
    avg_x, avg_y, avg_z = (sum([x for (x,y,z) in list])/len([x for (x,y,z) in list]),sum([y for (x,y,z) in list])/len([y for (x,y,z) in list]),sum([z for (x,y,z) in list])/len([z for (x,y,z) in list]))
    return [(x-avg_x,y-avg_y,z-avg_z) for (x,y,z) in list]

def equation_2_3(list):
    ans = []
    for i in range(len(list)):
        x,y,z = list[i]
        for j in range(i):
            pre_x,pre_y,pre_z = list[j]
            x += pre_x
            y += pre_y
            z += pre_z
        ans.append((x,y,z))
    return ans

def get_coordinate(combination, protein):
    if combination == 'principal_components':
        pass
    else:
        attribute_a, attribute_b, attribute_c = combination
        with open("Physicochemical_Properties_Amino_Acids.txt") as f:
            attributes = [(float(line.split()[attribute_a]),float(line.split()[attribute_b]), float(line.split()[attribute_c])) for line in f]
        normalized_attributes = transform(attributes)
        numerical_input = [normalized_attributes[amino_acid_order.index(i)] for i in protein if i in amino_acid_order]
        final_input = equation_2_3(numerical_input)
        return final_input
    