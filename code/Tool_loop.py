# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 10:25:47 2024

@author: Caleb Jensen
"""

import pandas as pd
import numpy as np
from Tool_functions import make_prompt
from Tool_functions import step_one_cleaning
from Tool_functions import step_two_cleaning
from Tool_functions import remove_asterisks




ISIC_4_4digit = pd.read_excel("ISIC_4_4digit.xlsx", dtype = {"code": str, "description": str})
ISIC_31_4digit = pd.read_excel("ISIC_31_4digit.xlsx", dtype = {"code": str, "description": str})
corr_table = pd.read_csv("ISIC4_ISIC31.csv", dtype={"ISIC4code": str, "partialISIC4": str, "ISIC31code": str, "partialISIC31": str})

corr_table.fillna("", inplace = True)
ISIC_4_4digit.fillna("", inplace = True)
ISIC_31_4digit.fillna("", inplace = True)

codes = np.array(ISIC_4_4digit["code"])

def tool_loop(codes, mod = 'gemini-pro'):
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
                    prompt = make_prompt("four", four_code, corr_table, ISIC_old = ISIC_31_4digit, ISIC_new = ISIC_4_4digit)
                    df_2 = step_two_cleaning(prompt, four_code, mod)
                    break
                except Exception as e:
                    if i == max_attempts:
                        return(print("it broke"))
            df_big = pd.concat([df_big, df_2])
            df_big = df_big[df_big.notna().all(axis=1)]
            df_big = df_big.reset_index(drop = True)
            if i % 5 == 0:
                time.sleep(5)
            i += 1
        print(four_code)
    return df_big

correspondence_table = tool_loop(codes)
