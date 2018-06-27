# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 19:49:20 2018

@author: Nagasudhir

pandas joing dataframes
https://pandas.pydata.org/pandas-docs/stable/merging.html#joining-on-index
"""
from report_fetch_modules import login_logout as login

from report_fetch_modules import psp_fetch

import pandas as pd

import datetime as dt

import os

# get the directory of the script file
# print(os.path.dirname(os.path.realpath(__file__)))
inputFileFolder = r'C:\Users\Nagasudhir\Documents\Python Projects\python_web_reports_cient\app\ui_modules'
inputFilename = os.path.join(inputFileFolder, 'input_file.xlsx')

# get the analysis Key Values
analysisKeyValuesInputDF = pd.read_excel(inputFilename,sheetname='input')

# read the config params from the input.xlsx file
configDF = pd.read_excel(inputFilename,sheetname='config').set_index('key')
targetOffset=configDF.loc['targetOffset'][0]
fromOffset=configDF.loc['fromOffset'][0]
toOffset=configDF.loc['toOffset'][0]

# login to the site
s  = login.login()

# get the psp stat comparision file
statsDF = psp_fetch.getPSPDFStatsComparision(s,targetOffset, fromOffset, toOffset)

# dump the psp stat comparision file
outFilename = 'psp_dump_'+dt.datetime.now().strftime('%d_%m_%y_%H_%M_%S')+'.xlsx'
writer = pd.ExcelWriter(outFilename)
statsDF.reset_index().to_excel(writer, index=False)
writer.save()

# left join of df using merge
# result = pd.merge(left, right, left_on='key', right_index=True, how='left', sort=False);
leftTable = analysisKeyValuesInputDF.groupby(['entity', 'key']).first()
resultDF = pd.merge(leftTable, statsDF, left_index=True, right_index=True, how='left', sort=False);
# todo create min_violated, max_violated, mean_deviation columns
# todo re-arrange columns

# dump the results file
outFilename = 'results_'+dt.datetime.now().strftime('%d_%m_%y_%H_%M_%S')+'.xlsx'
writer = pd.ExcelWriter(outFilename)
resultDF.reset_index().to_excel(writer, index=False)
writer.save()
