'''
Created on Jul 2, 2018

@author: 19115678
'''
import numpy as np
from sklearn.preprocessing.label import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from sklearn.externals import joblib
from Secondary_Structure_Converter_v2 import all_set_filepath
from sklearn import svm
import os
'''
09.19.2018 11:54 PM GMT +8 edit:
minor debug use
'''
import sys
'''
end update
'''

def load_data(filename):
    with open(filename) as f:
        return [[float(i) for i in line.split(",")] for line in f]
    
def train_SVM(train_input_path, train_output_path):
    #get data
    train_input = np.array(load_data(train_input_path))
    train_output = np.array(load_data(train_output_path))
    classifier = OneVsRestClassifier(svm.SVC(kernel = "rbf"))
    classifier.fit(train_input, train_output)
    return classifier
    
def save_SVM(classifier,path,set_num, trans_num):
    #generate filename
    filename = "SVM_Set_"+set_num+"_"+trans_num+".pkl"
    joblib.dump(classifier, filename)

def create_and_store_svm():
    sets = all_set_filepath()
    for dataset in sets:
        '''
	09.20.2018 12:05 AM GMT +8 flag:
	bug found: set_number only takes in the last number
	if set number exceeds single-digit issues occur
	'''
	#set_number = dataset[-1]
	'''
	09.20.2018 12:05 AM GMT +8 bugfix:
	'''
	set_number = ''.join([char for char in dataset if char.isdigit()])
	'''
	end bugfix
	'''
        input_paths = []
        output_paths = []
	
        for i in range(5):
            filename = "SVM_Training_Feature_" + str(i+1) + ".txt"
            input_paths.append(os.path.join(dataset,filename))
            filename = "SVM_Training_Label_" + str(i+1) + ".txt"
            output_paths.append(os.path.join(dataset, filename))

        for i in range(len(input_paths)):
            print input_paths[i]
            svm = train_SVM(input_paths[i],output_paths[i])
            save_SVM(svm,dataset,set_number,str(i+1))
