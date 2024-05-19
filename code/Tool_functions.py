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
    if num_codes[four_code] > 10:
        prompt = prompt + " What is your best estimate of the proportion of jobs now coded in " + four_code + " that were in each of the previous codes in version 3.1? The proportions can be less than .05 and many probably are less .05. Can you give me your best guesses in a table with 3 columns, first the three digit code, " + four_code + " then the four didgit codes, then the proportions?"
    else: 
        prompt = prompt + " What is your best estimate of the proportion of jobs now coded in " + four_code + " that were in each of the previous codes in version 3.1? If there is only 1 version 3.1 code, it is automatically 1. Can you give me your best guesses in a table with 3 columns, first the version 4 code, " + four_code + " then the version 3.1 codes, then the proportions?"
    return prompt

## main loop to create codes 
def tool_loop(codes, corr_table, ISIC_old, ISIC_new, mod = 'gemini-pro'):
    import pandas as pd
    import time
    df_big = pd.DataFrame({'version_4': [], 'version_3.1': [], "Proportion of Jobs": []})
    i = 0
    for four_code in codes:
        if corr_table["ISIC4code"].value_counts()[four_code] == 1:
            code_31 = corr_table[corr_table["ISIC4code"] == four_code]
            v_3 = code_31["ISIC31code"].iloc[0]
            data = {"version_4": [four_code], "version_3.1": [v_3], "Proportion of Jobs": [1]}
            df_2 = pd.DataFrame(data, [len(df_big)])
            df_big = pd.concat([df_big, df_2])
            df_big = df_big[df_big.notna().all(axis=1)]
            df_big = df_big.reset_index(drop = True)
        else:
            max_attempts = 10
            for i in range(1+max_attempts):
                try:
                    prompt = make_prompt("four", four_code, corr_table, ISIC_old = ISIC_old, ISIC_new = ISIC_new)
                    df_2 = step_two_cleaning(prompt, four_code, mod)
                    break
                except Exception as e:
                    if i == max_attempts:
                        return(print("it broke"))
            df_big = pd.concat([df_big, df_2])
            df_big = df_big[df_big.notna().all(axis=1)]
            df_big = df_big.reset_index(drop = True)
            if i % 5 == 0:
                time.sleep(3)
            i += 1
        print(four_code)
    return df_big