'''
Created on Jun 26, 2018

@author: 19115678
'''

import Training_Data_Extraction_Verifier as data_verifier
import Secondary_Structure_Conversion_Verifier_v2 as conversion_verifier
import Training_Data_Purification_Verifier as purification_verifier

'''
@param operation specifies the postcondition that is being verified

called by the runner
'''
def verify_validity(operation):
    if operation == "extraction":
        data_verifier.verify_training_data()
    elif operation == "conversion":
        conversion_verifier.verify_transformation()
    elif operation == 'purification':
        purification_verifier.verify_purification()