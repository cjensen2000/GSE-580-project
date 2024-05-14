# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 10:15:46 2024

@author: Caleb Jensen
"""

from Tool_draft import make_prompt
from Tool_draft import step_one_cleaning
from Tool_draft import step_two_cleaning
from Tool_draft import remove_asterisks
from Tool_loop import tool_loop
import pandas as pd
import numpy as np
import time

## Start by importing the correspondence table and .txt files with with codes and descriptions
corr_table = pd.read_csv("ISIC4_ISIC31.csv", dtype={"ISIC4code": str, "partialISIC4": str, "ISIC31code": str, "partialISIC31": str})
corr_table = corr_table.fillna("")
ISIC_4 = pd.read_csv("isic4.txt", dtype={'num': str}, delimiter = "|")
ISIC_31 = pd.read_excel("ISIC_31.xlsx", dtype={'code': str, "description": str})
ISIC_31 = ISIC_31.drop(columns = [ISIC_31.columns[0]])
col_names = ["code", "description"]
ISIC_4.columns = col_names
ISIC_31.columns = col_names


# Cleaning data and making dfs for each code length 
code_length_4 = ISIC_4['code'].str.len()
code_length_31 = ISIC_31['code'].str.len()

# Filter DataFrames based on code length
ISIC_4_2digit = ISIC_4[code_length_4 == 2]
ISIC_4_3digit = ISIC_4[code_length_4 == 3]
ISIC_4_4digit = ISIC_4[code_length_4 == 4]

ISIC_3_2digit = ISIC_31[code_length_31 == 2]
ISIC_3_3digit = ISIC_31[code_length_31 == 3]
ISIC_3_4digit = ISIC_31[code_length_31 == 4]

# Making 3 digit and 2 digit 4.0 codes columns in the correspondence table 
corr_table['ISIC_4_3d'] = corr_table['ISIC4code'].str[:3]
corr_table['ISIC_4_2d'] = corr_table['ISIC4code'].str[:2]


codes = np.array(ISIC_4_4digit["code"])

codes_list = []
for code in codes :
    if corr_table["ISIC4code"].value_counts()[code] == 1:
        codes_list.append(code)

multi_codes = [code for code in codes if code not in set(codes_list)]
names = []
for i in range(100):
    name = "Proportion of Jobs" + str(i)
    names.append(name)

prop_df = tool_loop(multi_codes)
for i in range(len(names)):
    max_retries = 5
    for j in range(1, max_retries):
        try:
            test = tool_loop(multi_codes)
            break
        except Exception as e:
            if j == max_retries:
                print(f"Reached maximum retries ({max_retries}). Giving up.")
            else: 
                time.sleep(.1)
    prop_df[names[i]] = test['Proportion of Jobs']
    
prop_df["codes"] = prop_df["version_4"] + "-" + prop_df["version_3.1"]
prop_df = prop_df.drop(columns = ["version_4", "version_3.1"])
new_col_names = prop_df["codes"].tolist()
prop_df = prop_df.T
prop_df.columns = new_col_names
prop_df = prop_df.drop("codes", axis = 0)
variance = prop_df.var()
var_df = pd.DataFrame(variance)
var_df.to_excel("variance_df.xlsx")
import matplotlib.pyplot as plt
plt.hist(var_df)
plt.savefig('variance.png', dpi = 300)
