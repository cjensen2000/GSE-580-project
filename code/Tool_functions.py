# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 10:16:32 2024

@author: Caleb Jensen
"""

def step_one_cleaning(prompt, mod = 'gemini-pro'):  
    from io import StringIO
    import csv
    import pathlib
    import textwrap
    import google.generativeai as genai
    import numpy as np
    import pandas as pd
    ## Need to change this line to get your own API key if possible
    from config import GOOGLE_API_KEY
    
    
    #setting the model and API key
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(mod)
    
    # Input string prompt to the google model 
    response = model.generate_content(prompt)
    
    # Define the data string
    data_string = response.text
    
    # Create a StringIO object to mimic a file-like object
    data_io = StringIO(data_string)
    
    # Create first df to be cleaned and returned 
    df = pd.read_csv(data_io, delimiter="|")
    
    # Drop empty top row 
    df = df.iloc[1:].reset_index(drop = True)
    
    # Drop empty columns
    names = df.columns
    for name in names: 
        if "unnamed" in name.lower(): 
            df = df.drop(columns = [name])
    return df

def remove_asterisks(text):
    import re
    pattern = r"\*"
    return re.sub(pattern, "", text)

def strip_non_digits(text):
    import re
    return re.sub(r"[^\d.]", "", text)


def step_two_cleaning(prompt, code, mod = 'gemini-pro'):
    import numpy as np
    import pandas as pd
    from collections import Counter
    import time
    status = "broken"
    while status == "broken":
        #max_retries = 10
        #for attempt in range(1, max_retries + 1):
            #try:
        df = step_one_cleaning(prompt, mod)
                #break
            #except Exception as e:
                #if attempt == max_retries:
                    #return print(f"Reached maximum retries ({max_retries}). Giving up.")
                #else: 
                    #time.sleep(.1)
        names = df.columns
        if len(names) == 3 and len(df) != 0 and type(df[names[2]][0]) == str:
            count = Counter(df[names[2]][0])
            if count["."] == 1:
                df[names[2]] = df[names[2]].astype(str)
                props = np.array(df[names[2]])
                for i in range(len(props)): 
                    if df[names[2]][i] == "**1**":
                        df[names[2]][i] = "1.00"
                    elif type(df[names[2]][i]) == str:
                        if 'n/a' in df[names[2]][i].lower() or 'nan' in df[names[2]][i].lower():
                            df[names[2]][i] = "0"
                status = "clean"
        if status == "clean":
            names = df.columns
            names_2 = ["version_4", "version_3.1", "Proportion of Jobs"]
            df.columns = names_2
            # Replace non-numeric characters with an empty string
            pattern = r'\D'  # Matches any non-digit character
            df["version_4"] = df["version_4"].astype(str)
            df["version_4"] = df["version_4"].str.replace(pattern, '') 
            df["version_4"] = df["version_4"].apply(remove_asterisks)
            df["version_4"] = df["version_4"].str.replace(' ', '')
            
            df["version_3.1"] = df["version_3.1"].astype(str)
            df["version_3.1"] = df["version_3.1"].str.replace(pattern, '')
            df["version_3.1"] = df["version_3.1"].apply(remove_asterisks)
            df["version_3.1"] = df["version_3.1"].str.replace(' ', '')
            if type(df["Proportion of Jobs"].iloc[0]) == str:
                df["Proportion of Jobs"] = df["Proportion of Jobs"].apply(remove_asterisks)

        #Checking if full code is present
            if len(df["version_3.1"].iloc[0]) != 4:
                status = "broken"
            if len(df["version_4"].iloc[0]) != 4:
                df["version_4"] = code
  
    # Making proportion column a float between 0 and 1
    if type(df["Proportion of Jobs"][0]) == str:
        pattern = r"[^\d.]"  # Matches any non-digit character
        df["Proportion of Jobs"] = df["Proportion of Jobs"].apply(strip_non_digits)
        df["Proportion of Jobs"] = df["Proportion of Jobs"].str.strip()
        df["Proportion of Jobs"] = df["Proportion of Jobs"].str.replace("%", "")
        df["Proportion of Jobs"] = df["Proportion of Jobs"].str.replace("<", "")
        df["Proportion of Jobs"] = df["Proportion of Jobs"].astype(float)
    if df["Proportion of Jobs"][0] > 1:
        df["Proportion of Jobs"] = df["Proportion of Jobs"]/100 
    
    ## scale the data frame
    df = df.reset_index(drop = True)
    if df["Proportion of Jobs"].sum() > 1:
        total = df["Proportion of Jobs"].sum()
        for i in range(len(df["Proportion of Jobs"])):
            df["Proportion of Jobs"][i] = df["Proportion of Jobs"][i]/total
    return df


## Creating a usable prompt 
def make_prompt(digits, four_code, corr_table, ISIC_old, ISIC_new):
    num_codes = corr_table["ISIC4code"].value_counts()
    prompt = "A " + digits + " digit code " + four_code + " which is (" + str(ISIC_new[ISIC_new["code"] == four_code]["description"].iloc[0]) + ") in ISIC version 4 is comprised of " + str(num_codes[four_code]) + " four digit codes in ISICs version 3.1, "
    codes_31 = corr_table[corr_table["ISIC4code"] == four_code]
    ## Code to handle when there are multiple instances of a code and possibly multiple "details" for that code in the correspondence table
    for code in codes_31["ISIC31code"].unique(): 
        ## start by just adding the code and its standard description from the ISIC code data frame
        prompt = prompt + code + " which is (" + ISIC_old[ISIC_old['code'] == code]['description'].iloc[0] + "), "
        ## now test if the code is unique, that is, it only appears once within the 3 digit code we are considering from version 4
        if codes_31['ISIC31code'].eq(code).sum() == 1:
            ## If it is unique, we test if the detail column of the correspondence table is empty, if it is not we add that extra detail to the prompt
            if codes_31[codes_31["ISIC31code"] == code]["Detail"].iloc[0] != "":
                prompt = prompt + " and includes (" + str(codes_31[codes_31["ISIC31code"] == code]["Detail"].iloc[0]) + ") "
        #elif codes_31['ISIC31code'].eq(code).sum() > 1:
            ## we now test if the code is not unique, if this is the case our code is more complicated, start by making an index list that will track appearances of this code
            #ind = []
            ## Now we will loop through the instances of the code and add the index of each instance if the detail section is not empty, we are collecting all the different details to include 
            #for i in range(codes_31['ISIC31code'].eq(code).sum()):
                #if codes_31[codes_31["ISIC31code"] == code]["Detail"].iloc[i] != "":
                    #ind.append(i)
            ## If the code is repeated but never with a detail the prompt remains unchanged
            #if len(ind) == 0:
                #prompt = prompt
            ## If the code is repeated but only with 1 detail, just include that single detail
            #elif len(ind) == 1:
                #prompt = prompt + "and includes (" + codes_31[codes_31["ISIC31code"] == code]["Detail"].iloc[ind[0]] + ", "
            ## If the code is repeated with multiple details, start with the first detail and drop the first item in the list so it is not repeated, then loop through the list adding all the details
            #else: 
                #prompt = prompt + " and includes (" + codes_31[codes_31["ISIC31code"] == code]["Detail"].iloc[ind[0]]
                #ind = ind[1:]
                #for k in ind
                    #prompt = prompt + ", and (" + codes_31[codes_31["ISIC31code"] == code]["Detail"].iloc[k] + ")"
    if num_codes[four_code] > 10:
        prompt = prompt + " What is your best estimate of the proportion of jobs now coded in " + four_code + " that were in each of the previous codes in version 3.1? The proportions can be less than .05 and many probably are less .05. Can you give me your best guesses in a table with 3 columns, first the three digit code, " + four_code + " then the four didgit codes, then the proportions?"
    else: 
        prompt = prompt + " What is your best estimate of the proportion of jobs now coded in " + four_code + " that were in each of the previous codes in version 3.1? If there is only 1 version 3.1 code, it is automatically 1. Can you give me your best guesses in a table with 3 columns, first the version 4 code, " + four_code + " then the version 3.1 codes, then the proportions?"
    return prompt


#corr_table = pd.read_csv("ISIC4_ISIC31.csv", dtype={"ISIC4code": str, "partialISIC4": str, "ISIC31code": str, "partialISIC31": str})
#corr_table = corr_table.fillna("")
#ISIC_4 = pd.read_csv("isic4.txt", dtype={'num': str}, delimiter = "|")
#ISIC_4.to_excel("ISIC_4.xlsx")
#ISIC_31 = pd.read_excel("ISIC_31.xlsx", dtype={'code': str, "description": str})
#ISIC_31 = ISIC_31.drop(columns = [ISIC_31.columns[0]])
#ISIC_31.to_excel("ISIC_31.xlsx")
#col_names = ["code", "description"]
#ISIC_4.columns = col_names
#ISIC_31.columns = col_names

#ISIC_4_4digit = ISIC_4[ISIC_4['code'].str.len() == 4]
#ISIC_4_4digit.to_excel("ISIC_4_4digit.xlsx")
#ISIC_31_4digit = ISIC_31[ISIC_31['code'].str.len() == 4]
