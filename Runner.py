'''
Created on Jun 22, 2018

@author: 19115678
'''
import Training_Data_Extractor as creator
import Training_Data_Purifier as purifier
import Secondary_Structure_Converter_v2 as transformer
import Verifier
import Numerical_Training_Set_Creator as data_quantifier
import Prediction
import SVM

def init():
    creator.create_training_data()
    Verifier.verify_validity("extraction")
    purifier.purify_data()
    Verifier.verify_validity("purification")

def main():
    init()
    for i in range(10):
        data_quantifier.split_categorical_data(0.4)
    transformer.transform_secondary_structure() 
    Verifier.verify_validity("conversion")
    data_quantifier.quantify_data()
    SVM.create_and_store_svm()
    Prediction.predict_and_test()

def length_of(fname):
    list = []
    with open(fname) as f:
        list = [1 for line in f]
    return len(list)

if __name__ == "__main__":
    main()