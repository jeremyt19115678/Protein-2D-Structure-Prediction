'''
Created on Jul 5, 2018

@author: 19115678
'''

from Secondary_Structure_Converter_v2 import all_set_filepath
from Training_Data_Extractor import create_file
from Tendency_Factor_Calculator import get_tendency_factor
from Data_Principal_Component_Analyzer import get_given_principal_components
from sklearn.externals import joblib
from math import sqrt
from time import gmtime, strftime

import os
import Complicated_Math
import numpy as np

def similar_amino_acid(protein_sequence_3d,refs,window_size,threshold):
    if window_size % 2 == 0:
        sidelength = window_size/2
    else:
        sidelength = (window_size-1)/2
    for name,ref in refs.iteritems():
        for j in range(len(ref)):
            if j-sidelength < 0 or j + sidelength >= len(ref):
                continue
            ref_sequence = ref[j-sidelength:j+sidelength+1]
            ref_sequence_3d = Complicated_Math.get_coordinate((1,2,7),ref_sequence)
            if Complicated_Math.get_similarity(ref_sequence_3d[sidelength], protein_sequence_3d[sidelength]) >= threshold:
                return (name, j)
    return None
                
def similarity_prediction(setpath,window_size, threshold):
    
    file = open("Overall_Results.txt","a+")
    file.write("Trial " + setpath[-1] + ":\n")
    file.close()
    if window_size % 2 == 0:
        sidelength = window_size/2
    else:
        sidelength = (window_size-1)/2
    for m in range(5):
        with open(os.path.join(setpath,"SVM_Reference_Categorical_Feature.txt")) as f:
            list = [line.split("|")[0] for line in f]
        filename = "SVM_Reference_Classification_Transformed_Rule_"+str(m+1)+".txt"
        with open(os.path.join(setpath, filename)) as f:
            list2 = [line.split("|")[0] for line in f]
        if list != list2:
            return
        
        with open(os.path.join(setpath,"SVM_Reference_Categorical_Feature.txt")) as f:
            refs = {line.split("|")[0] : line.split("|")[1][:-1] for line in f}
        with open(os.path.join(setpath,"SVM_Testing_Categorical_Feature.txt")) as f:
            test = {line.split("|")[0] : line.split("|")[1][:-1] for line in f}
        filename = "SVM_Reference_Classification_Transformed_Rule_" + str(m+1) +".txt"
        with open(os.path.join(setpath,filename)) as f:
            ref_structure = {line.split("|")[0] : line.split("|")[1][:-1] for line in f}
        
        unpredictable_amino_acids = 0
        total_amino_acids = 0
        bad_proteins = {}
        predicted_proteins = {}
        test_length = 0
        for protein in test.itervalues():
            test_length += len(protein)
        print test_length
        for name, protein in test.iteritems():
            prediction = ""
            for i in range(len(protein)):
                total_amino_acids += 1
                if i-sidelength < 0 or i + sidelength >= len(protein):
                    prediction+=" "
                    unpredictable_amino_acids += 1
                    continue
                protein_sequence = protein[i-sidelength:i+sidelength+1]
                protein_sequence_3d = Complicated_Math.get_coordinate((1,2,7),protein_sequence)
                similar = similar_amino_acid(protein_sequence_3d, refs, window_size, threshold)
                if similar == None:
                    prediction += " "
                    unpredictable_amino_acids+= 1
                    continue
                else:
                    sim_name, index = similar
                    prediction += ref_structure[sim_name][index]  
            if len(prediction) != len(protein):
                print "Protein", name, "predicted secondary structure length is problematic."
                bad_proteins[name] = prediction
                continue
            predicted_proteins[name] = prediction   
            print str(total_amino_acids), "/" , str(test_length)
        
        file = open("Overall_Results.txt","a+")
        file.write("When using translation method " + str(m+1) + ", " + str(round(unpredictable_amino_acids/float(total_amino_acids),1))+"% of Proteins cannot be predicted via similarity analysis.\n")
        file.close()
        
        filename = "Prediction_Based_On_Similarity_" + str(m+1) + ".txt"
        create_file(os.path.join(setpath,filename))
        file = open(os.path.join(setpath,filename),"a+")
        for name,item in predicted_proteins.iteritems():
            file.write(name + "|" + item + "\n")
        file.close()
        
        filename = "Prediction_Pure_SVM_" + str(m+1) + ".txt"
        create_file(os.path.join(setpath,filename))
        file = open(os.path.join(setpath,filename),"a+")
        for name, item in predicted_proteins.iteritems():
            file.write(name+"|")
            for i in item:
                file.write(" ")
            file.write("\n")
        file.close()
    #loop through the test file proteins
    #for each test proteins loop through reference set to look for similar
    #if similar take reference amino acid's secondary structure
    #if no similar/ sliding table too small put blank
    #create a file for each translation method 

def svm_prediction(setpath):
    number = setpath[-1]
    pc = get_given_principal_components()
    test_sequence_file = os.path.join(setpath,"SVM_Testing_Categorical_Feature.txt")
    
    with open(test_sequence_file) as f:
        test_proteins = {line.split("|")[0] : line.split("|")[1][:-1] for line in f}
        
    for m in range(5):
        filename = "SVM_Set_"+number+"_"+str(m+1)+".pkl"
        print filename
        classifier = joblib.load(filename)
        print classifier
        test_classification_file = os.path.join(setpath,"SVM_Testing_Classification_Transformed_Rule_" + str(m+1) + ".txt")
        tf = get_tendency_factor(test_sequence_file,test_classification_file)
    
        
        filename = "Prediction_Based_On_Similarity_" + str(m+1) + ".txt"
        print filename
        print "started", strftime("%Y-%m-%d %H:%M:%S", gmtime())
        with open(os.path.join(setpath, filename)) as f:
            predictions = {line.split("|")[0] : line.split("|")[1][:-1] for line in f}
        print len(predictions)
        create_file(os.path.join(setpath,"temp.txt"))
        for name, item in predictions.iteritems():
            for i in range(len(item)):
                pass
                if item[i] == " ":
                    code = tf[test_proteins[name][i]] + pc[test_proteins[name][i]]
                    a,b,c,d,e,f = code
                    code = (round(a,2),round(b,2),round(c,2),round(d,2),round(e,2),round(f,2))
                    nparray = np.array(list(code))
                    reshaped_array = nparray.reshape(1,-1)
                    svm_output = int(classifier.predict(reshaped_array).tolist()[0])
                    svm_output_to_categorical= {0:"H", 1:"E", 2:"C"}
                    item = item[:i] + svm_output_to_categorical[svm_output] + item[i+1:]
                    predictions[name] = item
        file = open(os.path.join(setpath,"temp.txt"),"a+")
        for name, item in predictions.iteritems():
            file.write(name + "|" + item + "\n")
        file.close()
        os.remove(os.path.join(setpath,filename))
        os.rename(os.path.join(setpath,"temp.txt"), os.path.join(setpath,filename))
        print "completed", strftime("%Y-%m-%d %H:%M:%S", gmtime())

def get_accuracy_state(setpath):
    setnumber = setpath[-1]
    file = open("Overall_Results.txt","a+")
    file.write("Set " + setnumber + ":\n")
    file.write()
    file.close()
    for m in range(5):
        filename = os.path.join(setpath,"SVM_Testing_Classification_Transformed_Rule_"+str(m+1)+".txt")
        with open(filename) as f:
            correct_output = {line.split("|")[0] : line.split("|")[1][:-1] for line in f}
        filename = os.path.join(setpath,"Prediction_Based_On_Similarity_" + str(m+1) + ".txt")
        with open(filename) as f:
            svm_and_similarity_output = {line.split("|")[0] : line.split("|")[1][:-1] for line in f}
        
        total_state = [0,0,0]
        similarity_right_predict = [0,0,0]
        categorical_to_number = {"H":0, "E": 1, "C":2}
        number_to_categorical = {0: "H", 1: "E",2:"C"}
        
        for name, item in svm_and_similarity_output.iteritems():
            for i in range(len(item)):
                if item[i] == correct_output[name][i]:
                    similarity_right_predict[categorical_to_number[item[i]]] += 1
                
                total_state[categorical_to_number[item[i]]] += 1
        
        print similarity_right_predict, total_state
        similarity_overall_accuracy = sum(similarity_right_predict)/float(sum(total_state))
        similarity_right_predict = [float(similarity_right_predict[i])/total_state[i] for i in range(len(similarity_right_predict))]
        
        file = open("Overall_Results.txt","a+")
        file.write("Set " + setnumber + ":\n")
        output = "Translate " + str(m+1) + ": "
        for i in range(len(similarity_right_predict)):
            output += "Q" + number_to_categorical[i] + " = " + str(round(similarity_right_predict[i],2)) + ", "
        file.write(output[:-2])
        file.close()

def predict_and_test(): #better named results
    create_file("Overall_Results.txt")
    sets = all_set_filepath()
    for i in range(len(sets)):
        similarity_prediction(sets[i], 15, 0.9)
    for dataset in sets:
        svm_prediction(dataset)
        get_accuracy_state(dataset)
