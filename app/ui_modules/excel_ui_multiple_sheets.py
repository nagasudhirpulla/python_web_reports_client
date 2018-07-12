# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 19:49:20 2018

@author: Nagasudhir

pandas joing dataframes
https://pandas.pydata.org/pandas-docs/stable/merging.html#joining-on-index
https://www.dataquest.io/blog/excel-and-pandas/
"""
import sys
# making the parent directory as the main path for imports
sys.path.append("..")

from report_fetch_modules import login_logout as login

from report_fetch_modules import psp_fetch

import pandas as pd

import datetime as dt

import os

import numpy as np

inputFileFolder = r'C:\Users\Nagasudhir\Documents\Python Projects\python_web_reports_cient\app\ui_modules'

# get the directory of the script file
# print(os.path.dirname(os.path.realpath(__file__)))
if('__file__' in globals()):
    inputFileFolder = os.path.dirname(os.path.realpath(__file__))

inputFilename = os.path.join(inputFileFolder, 'input_file.xlsx')

# get the analysis Key Values
analysisKeyValuesInputDF = pd.read_excel(inputFilename,sheetname='input')

# read the array of input dfs for analysis
analysisKeyValuesInputDFArray = []
inputSheetNames = []
xlsx = pd.ExcelFile(inputFilename)
for sheetName in xlsx.sheet_names:
    if(sheetName.startswith("input")):
        # sheet name starts with input, hence push to inout dfs array
        analysisKeyValuesInputDFArray.append(pd.read_excel(inputFilename,sheet_name=sheetName))
        inputSheetNames.append(sheetName)

# read the config params from the input.xlsx file
configDF = pd.read_excel(inputFilename,sheetname='config').set_index('key')
targetOffset=configDF.loc['targetOffset'][0]
fromOffset=configDF.loc['fromOffset'][0]
toOffset=configDF.loc['toOffset'][0]

# login to the site
s  = login.login()

# get the psp stat comparision file
statsDF = psp_fetch.getPSPDFStatsComparision(s,targetOffset, fromOffset, toOffset)

# logout of the site
loggedOut = login.logout(s)

# dump the psp stat comparision file
outFilename = os.path.join(inputFileFolder, 'psp_dump_' + dt.datetime.now().strftime('%d_%m_%y_%H_%M_%S')+'.xlsx')
writer = pd.ExcelWriter(outFilename)
statsDF.reset_index().to_excel(writer, index=False)
writer.save()

# create the results file
outFilename = os.path.join(inputFileFolder, 'results_' + dt.datetime.now().strftime('%d_%m_%y_%H_%M_%S')+'.xlsx')
writer = pd.ExcelWriter(outFilename)
    
for counter, analysisKeyValuesInputDF in enumerate(analysisKeyValuesInputDFArray):
    # left join of df using merge
    # result = pd.merge(left, right, left_on='key', right_index=True, how='left', sort=False);
    leftTable = analysisKeyValuesInputDF.groupby(['entity', 'key']).first()
    resultDF = pd.merge(leftTable, statsDF, left_index=True, right_index=True, how='left', sort=False);
    
    # create min_violated, max_violated, violated, is_Blank, mean_deviation_percentage columns
    val_col = pd.to_numeric(resultDF['value'], errors='coerce')
    resultDF['min_violated'] = np.where((pd.notnull(val_col))&(val_col<resultDF['min_cap']), 1, 0)
    resultDF['max_violated'] = np.where((pd.notnull(val_col))&(val_col>resultDF['max_cap']), 1, 0)
    resultDF['violated'] = resultDF['min_violated'] | resultDF['max_violated']
    resultDF['is_Blank'] = np.where((~pd.notnull(val_col)), 1, 0)
    resultDF['prev_band_violated'] = np.where((pd.notnull(val_col))&(val_col<resultDF['min']), 1, 0) | np.where((pd.notnull(val_col))&(val_col>resultDF['max']), 1, 0)
    resultDF['mean_deviation_perc'] = np.where(resultDF['is_Blank'] == 0, 100*(val_col-resultDF['mean'])/resultDF['mean'], None)
    
    # re-arrange columns
    resultDF = resultDF[['value', 'min_cap', 'max_cap', 'mean', 'mean_deviation_perc', 'violated', 'prev_band_violated', 'min', 'max', 'is_Blank', 'min_violated', 'max_violated', 'time']]
    
    resultDF.reset_index().to_excel(writer, sheet_name=inputSheetNames[counter], index=False)

writer.save()