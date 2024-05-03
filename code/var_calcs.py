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

var_df = pd.DataFrame({'version_4': [], 'version_3.1': []})
test_codes = ['3312', '2811', '2731', '2670']
j = 0
for code in test_codes:
    j +=1
    prompt = make_prompt("four", code)
    df = step_two_cleaning(prompt, code)
    names = ["Proportion of Jobs1","Proportion of Jobs2","Proportion of Jobs3","Proportion of Jobs4","Proportion of Jobs5","Proportion of Jobs6","Proportion of Jobs7","Proportion of Jobs8", "Proportion of Jobs9"]
    ranks = ["rank1", "rank2", "rank3", "rank4", "rank5", "rank6", "rank7", "rank8", "rank9", "rank10"]
    print(j)
    for i in range(len(names)):
        prompt = make_prompt("four", code)
        test = step_two_cleaning(prompt, code)
        df[names[i]] = test["Proportion of Jobs"]
        df[ranks[i]] = test["Proportion of Jobs"].rank(ascending = False).astype(int)
    var_df = pd.concat([var_df, df])


df_2 = pd.DataFrame()
var_df = var_df.reset_index(drop = True)


prop_df = var_df.filter(like="Proportion")
prop_df["codes"] = var_df["version_4"] + "-" + var_df["version_3.1"]
prop_df_2 = prop_df.T

new_col_names = prop_df["codes"].tolist()
prop_df_2.columns = new_col_names
prop_df_2 = prop_df_2.drop("codes", axis = 0)

variance = prop_df_2.var()
print(np.mean(variance))
print(np.max(variance))
print(np.min(variance))

prop_df = tool_loop(multi_codes)
names = ["Proportion of Jobs2","Proportion of Jobs3","Proportion of Jobs4","Proportion of Jobs5","Proportion of Jobs6","Proportion of Jobs7","Proportion of Jobs8", "Proportion of Jobs9"]
for i in range(len(names)):
    test = tool_loop(multi_codes)
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
np.mean(variance)
np.max(variance)
variance[variance == np.max(variance)]
prop_df["8549-8090"]

variance = variance[variance < .05]
np.mean(variance)
np.max(variance)
np.min(variance)
variance[variance == np.max(variance)]
test[test["version_4"]=="2811"]
prop_df['8620-8512']


codes = np.array(ISIC_4_4digit["code"])

codes_list = []
for code in codes :
    if corr_table["ISIC4code"].value_counts()[code] == 1:
        codes_list.append(code)
corr_table
trial = tool_loop(codes_list)
np.min(trial["Proportion of Jobs"])   

multi_codes = [code for code in codes if code not in set(codes_list)]
trial_multi = tool_loop(multi_codes)
