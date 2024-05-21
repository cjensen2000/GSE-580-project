					README
|GSE-580-Project
|----code
|   |----.ipynb_checkpoints
|   |----__pycache__
|   |----config.py				# Has API key
|   |----main_script.py				# Main tool use file, creates probability mapping
|   |----Tool_functions.py			# Holds all functions used in the tool
|   |----var_script.py				# Script to analyze variance in probability predictions
|----India Data
|   |----correspondence_table.Rmd		
|   |----India_Data_2009_.Rmd
|   |----India_Data_2011_.Rmd
|   |----ISIC_Codes_.txt
|----input
|   |----ISIC_4_4digit.xlsx			# Holds all 4 digit codes and descriptions for v.4
|   |----ISIC_31_4digit.xlsx			# Holds all 4 digit codes and descriptions for v.3.1
|   |----ISIC4_ISIC31.csv			# Correspondence between v.4 and v.3.1 including details
|----literature
|----meetings
|----output	
|----presentations

-All input data files may be found in input, they include 
	- ISIC_4_4digit (all 4 digit ISICS version 4 codes)
	- ISIC_31_4digit (all 4 digit ISICS version 3.1 codes)
	- ISIC4_ISIC31 (correspondence table of ISICS v.4 to ISICS v.3.1
-All code files may be found in code, they include
	- Tool_functions.py (the basic functions that make up the tool) 
	- main_script.py (the script where the functions are used to create a correspondence table 
	- var_scipt.py (the script used to get variance calculations and consider reproducibility)  

Instructions:
 
For simple tool use (main.script.py): 
1) download all files including correspondence table and files containing codes and descriptions from the old and new ISICS versions
2) Ensure all code files are saved in the same directory
3) Run on command line using the following method: 
$ python main_script.py correspondence_table ISIC_old ISIC_new mod* out_file_name
4) output correspondence table now saved in excel as out_file_name 

*optional, default is 'gemini-pro', other options are 'gemini-pro-1.0' and 'gemini-pro-1.0-latest'

For variance tool use:
1) Ensure all files saved in the same location 
2) run on command line as follows: 
$ python var_script.py correspondence_table ISIC_old ISIC_new mod outfile_xl out_file_png

3) this will return 2 files, an excel file showing each code pairing** and its variance and an image of a histogram of these code pairings and variances for visual understanding 

**Only codes where a code in new version maps to multiple codes in older version will be included. Otherwise the variance with only a single mapping will bias our mean and median result downward as they will always have 0 variance. 