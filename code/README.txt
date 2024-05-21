|GSE-580-Project
├───code
│   ├───.ipynb_checkpoints
│   └───__pycache__
├───India Data
├───input
├───literature
├───meetings
├───output
└───presentations

-All input data files may be found in input, they include 
	- ISIC_4_4digit (all 4 digit ISICS version 4 codes)
	- ISIC_31_4digit (all 4 digit ISICS version 3.1 codes)
	- ISIC4_ISIC31 (correspondence table of ISICS v.4 to ISICS v.3.1
-All code files may be found in code, they include
	- Tool_functions.py (the basic functions that make up the tool) 
	- main_script.py (the script where the functions are used to create a correspondence table 
	- var_scipt.py (the script used to get variance calculations and consider reproducibility)  

Instructions:
 
For simple tool use: 
1) download all files including correspondence table and files containing codes and descriptions from the old and new ISICS versions
2) Ensure all code files are saved in the same directory
3) Run on command line using the following method: 
$ python main_script.py correspondence_table ISIC_old ISIC_new mod <-(optional) out_file_name

For variance tool use:
1) Ensure all files saved in the same location 
2) run on command line as follows: 
$ python var_script.py correspondence_table ISIC_old ISIC_new mod outfile_xl out_file_png
3) this will return 2 files, an excel file showing each code pairing* and its variance and an image of a histogram of these code pairings and variances for visual understanding 

*Only codes where a code in one version maps to multiple codes in another will be included. Otherwise the variance with only a single mapping will bias our mean and median result downward as they will always have 0 variance. 