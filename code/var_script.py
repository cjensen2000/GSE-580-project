# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 10:15:46 2024

@author: Caleb Jensen
"""

from Tool_funtctions import make_prompt
from Tool_funtctions import step_one_cleaning
from Tool_funtctions import step_two_cleaning
from Tool_funtctions import remove_asterisks
from Tool_funtctions import tool_loop
from config import GOOGLE_API_KEY
import pandas as pd
import numpy as np
import time
import sys

# Access input and output file paths from sys.argv
corr_table = sys.argv[1]
ISIC_old = sys.argv[2]
ISIC_new = sys.argv[3]
mod = sys.argv[4]
out_file_xl = sys.argv[5]
out_file_png = sys.argv[6]

## Read in data from input files
ISIC_new = pd.read_excel(ISIC_new, dtype = {"code": str, "description": str})
ISIC_old = pd.read_excel(ISIC_old, dtype = {"code": str, "description": str})
corr_table = pd.read_csv(corr_table, dtype={"ISIC4code": str, "partialISIC4": str, "ISIC31code": str, "partialISIC31": str})

## Ensure no NAs in data read in from excel 
corr_table.fillna("", inplace = True)
ISIC_old.fillna("", inplace = True)
ISIC_new.fillna("", inplace = True)

## Get codes list
codes = np.array(ISIC_new["code"])

## Get a list of codes where the code only appears once 
codes_list = []
for code in codes :
    if corr_table["ISIC4code"].value_counts()[code] == 1:
        codes_list.append(code)

## selecting all but these codes to loop through so variance is not biased down
multi_codes = [code for code in codes if code not in set(codes_list)]
## making a list of names to use in variance loop so that each run of the tool can be assigned to its own column 
names = []
for i in range(100):
    name = "Proportion of Jobs" + str(i)
    names.append(name)

## first run of tool loop to initialize dataframe 
prop_df = tool_loop(multi_codes)
## go though names list, each time add the proportion values we got as a new column
for i in range(len(names)):
    max_retries = 5
    for j in range(1, max_retries):
        try:
            test = tool_loop(multi_codes, corr_table = corr_table, ISIC_old = ISIC_old, ISIC_new = ISIC_new, key = GOOGLE_API_KEY, mod = 'gemini-pro')
            break
        except Exception as e:
            if j == max_retries:
                print(f"Reached maximum retries ({max_retries}). Giving up.", e)
            else: 
                time.sleep(.1)
    prop_df[names[i]] = test['Proportion of Jobs']
    
## Now we manipulate data so that we get columns for each code pair with the 100 different correspondence probability estimates and take the variance of each 
prop_df["codes"] = prop_df["version_4"] + "-" + prop_df["version_3.1"]
prop_df = prop_df.drop(columns = ["version_4", "version_3.1"])
new_col_names = prop_df["codes"].tolist()
prop_df = prop_df.T
prop_df.columns = new_col_names
prop_df = prop_df.drop("codes", axis = 0)
variance = prop_df.var()
var_df = pd.DataFrame(variance)

## Output this variance dataframe to excel 
var_df.to_excel(out_file_xl, index = False)

## Print out a histogram of how the variances are distributed
import matplotlib.pyplot as plt
plt.hist(var_df)
plt.savefig(out_file_png, dpi = 300)
