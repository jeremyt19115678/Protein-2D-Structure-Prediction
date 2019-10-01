'''
Created on Jun 25, 2018

@author: 19115678
'''

import numpy as np
from Complicated_Math import amino_acid_order

'''
load a matrix of values from file @param t
return the matrix
'''
def load(t):
    dict= {"Properties_Matrix": "Physicochemical_Properties_Amino_Acids.txt", 
         "Factor_Loading_Matrix": "Given_Factor_Loading_Matrix.txt"}
    with open(dict[t]) as f:
        raw = [line.split() for line in f]
    list = []
    for raw_line in raw:
        line = []
        for item in raw_line:
            line.append(float(item))
        list.append(line)
    return np.array(list)

'''
flip the row and column of a matrix (ex. 5x3 to 3x5)
return said matrix
'''
def flip_matrix(mat):
    flipped_mat = []
    for i in range(len(mat[0])):
        flipped_mat.append([row[i] for row in mat])
    return flipped_mat

'''
for each number in the matrix normalize it based on the method specified in Li et. al's paper
'''
def normalize(mat):
    normalized_mat = []
    for row in mat:
        mini, maxi = (min(row),max(row))
        normalized_row = [(item-mini)/(float(maxi-mini)) for item in row]
        normalized_mat.append(normalized_row)
    return normalized_mat

'''
make a dictionary out of the matrix based on the amino acids
'''
def make_dictionary(mat):
    return {amino_acid_order[i]:tuple(mat[i]) for i in range(len(mat))}

'''
return a dictionary with amino acid as key and tuples of 3 values (3 principal components)
the 3 principal components are calculated based on the data given in the paper.

There are no actual principal component analysis carried out here. 
'''
def get_given_principal_components():
    X = load("Properties_Matrix").tolist()
    Y = load("Factor_Loading_Matrix").tolist()
    pca = np.matmul(X, Y).tolist()
    flipped_pca = flip_matrix(pca)
    normalized_pca = normalize(flipped_pca)
    penultimate = flip_matrix(normalized_pca)
    final = make_dictionary(penultimate)
    return final

