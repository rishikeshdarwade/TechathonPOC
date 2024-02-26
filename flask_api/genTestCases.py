# genTestCases.py

import os
#from dotenv import load_dotenv
from genai.credentials import Credentials
from genai.model import Model
from genai.schemas import GenerateParams


def generate_test_cases(context, requirements, acceptance_criteria,isregenerate):
    
    api_url = "https://bam-api.res.ibm.com"
    api_key = "pak-5wpgAvmz71vdcqYCxIVYOgA6HZ6zuqy_ptHnSM3RMlw"
    creds = Credentials(api_key, api_endpoint=api_url)

    params = GenerateParams(
        decoding_method= "greedy",
        temperature=0.7,
        top_p=1,
        top_k= 50,
        typical_p= 1,
        max_new_tokens=2000,
        beam_width= 1,
        stream= "true"
        )
    model = Model("meta-llama/llama-2-70b-chat", params=params, credentials=creds)
    if isregenerate:
        input_sentence=regenerate_input(context)
    else:
        input_sentence = generate_input(context, requirements, acceptance_criteria)
    
    print(input_sentence)
    response = model.generate([input_sentence])
    test_cases = response[0].generated_text
    print(test_cases)
    test_cases_start = test_cases.find("Test Cases:")  # Find the starting point of the test cases
    if test_cases_start != -1:
        modified_text = test_cases[test_cases_start:]  # Extract text from 'Test Cases' onwards
        test_cases = modified_text
        #print(modified_text)
    else:
        test_cases = "Test Cases are not in desired format !. \n" + test_cases

    return test_cases



def generate_input(context, requirements, acceptance_criteria):

    insturction = "[INST] <<SYS>> "+ context +" <</SYS>> \n Requirements: "+ requirements +"\n Acceptance Crtieria : "+ acceptance_criteria +""+ """ \n\n Generate Negative and Positive Test cases for above mentioned requirements. 
    Please maintain the format as below : 
    <<OUTPUT>> 
    Test Cases:
    Test Case 1. <TestCaseName>
    \t Step i. <Step>
    \n
    <</OUTPUT>> 
    [/INST]
    """

    return insturction

def regenerate_input(context):

    insturction = "[INST] <<SYS>> "+ context +""" <</SYS>>  \n\n Not satisfied with the generated test cases. Kindly re-generate more precised test cases.
    Please maintain the format as below :
    <<OUTPUT>>
    Test Cases:
    Test Case 1. <TestCaseName>
         Step i. <Step>
    <</OUTPUT>>
    [/INST] 
    """
    return insturction
