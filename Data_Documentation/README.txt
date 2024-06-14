									    README
|GSE-580-Project
|----code
|   |----.ipynb_checkpoints
|   |----__pycache__
|   |----config.py				# Has API key (must edit to add your own)
|   |----main_script.py				# Main tool use file, creates probability mapping
|   |----Tool_functions.py			# Holds all functions used in the tool
|   |----var_script.py				# Script to analyze variance in probability predictions
|----India Data
|   |----correspondence_table.Rmd		### 
|   |----India_Data_2009_.Rmd			India data to test the effectiveness of the model predictions. Data is from 2009 and 2011
|   |----India_Data_2011_.Rmd			In 2009 ISICS 3.1 was used, in 2011 4.0 was used, we can test back predictions by comparing the predicted
|   |----Corp_Table.Rmd				Use Corp table to get tables describing backcoded 2011 data to look like 2009
|   |----ISIC_Codes_.txt			values of 2011 to the truth of 2009 under the assumption to 2009 and 2011 economies of India were similar
|----input					###
|   |----ISIC_4_4digit.xlsx			# Holds all 4 digit codes and descriptions for v.4
|   |----ISIC_31_4digit.xlsx			# Holds all 4 digit codes and descriptions for v.3.1
|   |----ISIC4_ISIC31.csv			# Correspondence between v.4 and v.3.1 including details
|   |---- India_State_Boundary.dbf              # Files that contain info to make maps of India. 
|   |---- India_State_Boundary.shx              # From https://github.com/AnujTiwari/India-State-and-Country-Shapefile-Updated-Jan-2020
|   |---- India_State_Boundary.shp
|   |---- ISIC_words.txt                        # basic correspondence table to work off of
|----literature
|----meetings
|----output	
|----presentations

-All input data files may be found in input, they include 
	- ISIC_4_4digit (all 4 digit ISICS version 4 codes)
	- ISIC_31_4digit (all 4 digit ISICS version 3.1 codes)
	- ISIC4_ISIC31 (correspondence table of ISICS v.4 to ISICS v.3.1
        - India_State_Boundary.dbf, .shx, .shp (shape files for India)
-All code files may be found in code, they include
	- Tool_functions.py (the basic functions that make up the tool) 
	- main_script.py (the script where the functions are used to create a correspondence table 
	- var_scipt.py (the script used to get variance calculations and consider reproducibility)  

Instructions:
 
For simple tool use (main.script.py): 
1) download all files including correspondence table and files containing codes and descriptions from the old and new ISICS versions
2) Ensure all code files are saved in the same directory
3) Ensure necessary packages installed, specifically google-generativeai and wandb*
3) Run on command line using the following method: 
$ python main_script.py correspondence_table ISIC_old ISIC_new mod** out_file_name
4) Output correspondence table now saved in excel as out_file_name 
5) Typical runtime for the model is 5-10 minutes depending on the speed of the network calls to the google API

*Other necessary packages are pandas, numpy, and io 
**optional, default is 'gemini-pro', other options are 'gemini-pro-1.0' and 'gemini-pro-1.0-latest'

For variance tool use:
1) Ensure all files saved in the same location 
2) download necessary packages google-generativeai, and wandb***
3) run on command line as follows: 
$ python var_script.py correspondence_table ISIC_old ISIC_new mod**** outfile_xl out_file_png

4) this will return 2 files, an excel file showing each code pairing***** and its variance and an image of a histogram of these code pairings and variances for visual understanding 
5) Be warned, this requires overnight running normally of between 8-10 hours as the model must run 100 times

For India Data:
1) Download the Zip files (IND_2009_EUS_V01_M_V06_A_GLD_ALL and IND_2011_EUS_V01_M_V06_A_GLD_ALL)
2) Download the shapes files for map creation
3) Download ISIC_words.txt
4) Run Data_India_2009.rmd and Data_India_2011.rmd before Corp_Table.rmd
5) Need packages haven, stringr, ggplot2, sf, stringdist
6) Hit run on each code chunk 

***Other necessary packages are pandas, numpy, and io 
****Must specify desired model, options are 'gemini-pro', 'gemini-pro-1.0' and 'gemini-pro-1.0-latest'
*****Only codes where a code in new version maps to multiple codes in older version will be included. Otherwise the variance with only a single mapping will bias our mean and median result downward as they will always have 0 variance. 

------------------------------------------------------------------------------------------------------------------------------------------------------------
Variable Name 		Storage Type		Description
------------------------------------------------------------------------------------------------------------------------------------------------------------
Industrycat_isic	bool (0,1)		ISIC code for individual’s job. If it is in 2009, it is in ISIC 3.1. In 2011, it is in ISIC 4.
urban			bool (0,1)		Binary variable that takes the value 1 if the individual is in a city, and 0 otherwise.
Male			bool (0,1)		Binary variable that takes the value 1 if the individual is male, and 0 otherwise.
literacy		bool (0,1)		binary variable that takes the value 1 if the individual can read and write, and 0 otherwise.
age			int			the age of the individual.
hsize			int			How many members the individual has in their household.
school			bool (0,1)		binary variable that takes the value 1 if the individual is attending school, and 0 otherwise.
marital			int			variable that takes the value 1 if an individual is married, 2 if never married, 3 if living together, 4 if divorced or separated, or 5 if widowed. Of note, for the actual analysis we made a new variable that takes the value 1 if married and 0 otherwise.
vocational		bool (0,1)		binary variable that takes the value 1 if an individual has received vocational training, and 0 otherwise. 
lstatus			int			variable that takes the value 1 if employed, 2 if unemployed, and 3 if not in the labor force. We made a new variable that’s 1 if employed, 0 otherwise. 
subnatid_1		character		variable that has the name of the state or territory the individual is from.
