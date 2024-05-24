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
from Tool_functions import tool_loop
from config import GOOGLE_API_KEY
import sys


# Access input and output file paths from sys.argv
corr_table = sys.argv[1]
ISIC_old = sys.argv[2]
ISIC_new = sys.argv[3]


ISIC_new = pd.read_excel(ISIC_new, dtype = {"code": str, "description": str})
ISIC_old = pd.read_excel(ISIC_old, dtype = {"code": str, "description": str})
corr_table = pd.read_csv(corr_table, dtype={"ISIC4code": str, "partialISIC4": str, "ISIC31code": str, "partialISIC31": str})

corr_table.fillna("", inplace = True)
ISIC_old.fillna("", inplace = True)
ISIC_new.fillna("", inplace = True)

codes = np.array(ISIC_new["code"])
if len(sys.argv) > 5:
    mod = sys.argv[4]
    out_file = sys.argv[5]
    correspondence_table = tool_loop(codes, corr_table=corr_table, ISIC_old=ISIC_old, ISIC_new=ISIC_new, key = GOOGLE_API_KEY, mod = mod)

else: 
    out_file = sys.argv[4]
    correspondence_table = tool_loop(codes, corr_table=corr_table, ISIC_old=ISIC_old, ISIC_new=ISIC_new, key = GOOGLE_API_KEY, mod = 'gemini-pro')

correspondence_table.to_excel(out_file, index= False)

correspondence_table = tool_loop(codes, corr_table=corr_table, ISIC_old=ISIC_old, ISIC_new=ISIC_new, key = GOOGLE_API_KEY, mod = 'gemini-pro')
