# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 10:25:47 2024

@author: Caleb Jensen
"""
from Tool_draft import make_prompt
from Tool_draft import step_one_cleaning
from Tool_draft import step_two_cleaning
from Tool_draft import remove_asterisks
import pandas as pd
import numpy as np

corr_table = pd.read_csv("ISIC4_ISIC31.csv", dtype={"ISIC4code": str, "partialISIC4": str, "ISIC31code": str, "partialISIC31": str})
corr_table = corr_table.fillna("")
ISIC_4 = pd.read_csv("isic4.txt", dtype={'num': str}, delimiter = "|")
ISIC_31 = pd.read_excel("ISIC_31.xlsx", dtype={'code': str, "description": str})
ISIC_31 = ISIC_31.drop(columns = [ISIC_31.columns[0]])
col_names = ["code", "description"]
ISIC_4.columns = col_names
ISIC_31.columns = col_names

ISIC_4_4digit = ISIC_4[ISIC_4['code'].str.len() == 4]
ISIC_31_4digit = ISIC_31[ISIC_31['code'].str.len() == 4]

def tool_loop(codes):
    df_big = pd.DataFrame({'version_4': [], 'version_3.1': [], "Proportion of Jobs": []})
    for four_code in codes:
        if corr_table["ISIC4code"].value_counts()[four_code] == 1:
            code_31 = corr_table[corr_table["ISIC4code"] == four_code]
            v_3 = code_31["ISIC31code"].iloc[0]
            data = {"version_4": [four_code], "version_3.1": [v_3], "Proportion of Jobs": [1]}
            df = pd.DataFrame(data, [len(df_big)])
            df_big = pd.concat([df_big, df])
            df_big = df_big[df_big.notna().all(axis=1)]
            df_big = df_big.reset_index(drop = True)
        else:
            prompt = make_prompt("four", four_code, corr_table, ISIC_old = ISIC_31_4digit, ISIC_new = ISIC_4_4digit)
            df = step_two_cleaning(prompt, four_code)
            df_big = pd.concat([df_big, df])
            df_big = df_big[df_big.notna().all(axis=1)]
            df_big = df_big.reset_index(drop = True)
    return df_big
