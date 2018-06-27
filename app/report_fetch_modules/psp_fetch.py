# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 11:35:24 2018

@author: Nagasudhir

adding rows to multiindexed df
"""

import json
import requests
import pandas as pd
import datetime as dt
import numpy as np

pspUrl = 'http://103.7.130.126/POSOCOUI/PSP/GetPSPData?date=%s'

def getPSPDFStatsComparision(s, targetOffset, fromOffset, toOffset):
    comparePspDF = getPSPDFStats(s, fromOffset, toOffset)
    targetPspDF = getPSPDFSince(s, targetOffset, targetOffset)
    comparePspDF = comparePspDF.groupby(['entity', 'key']).first()
    targetPspDF = targetPspDF.groupby(['entity', 'key']).first()
    df = pd.concat([targetPspDF, comparePspDF], axis=1)
    return df
    

def getPSPDFStats(s, fromOffset, toOffset):
    pspDF = getPSPDFSince(s, fromOffset, toOffset)
    pspDF['value'] = pd.to_numeric(pspDF['value'], errors='coerce')
    aggDF = pspDF.groupby(['entity', 'key'], as_index=False).agg([np.nansum, np.nanmean, np.max, np.min])
    aggDF.columns = ['sum', 'mean', 'max', 'min']
    aggDF = aggDF.reset_index()
    return aggDF
    
def getPSPDFSince(s, fromOffset, toOffset):
    pspDF = getBlankPSPDF()
    if(not type(s) is requests.sessions.Session):
        print('didnot get valid session as a function input')
        return pspDF
    if(not((type(fromOffset) is int) and (type(fromOffset) is int))):
        print('didnot get integers as a date offset inputs')
        return pspDF
    if(fromOffset>toOffset):
        print('from offset should be less than to offset')
        return pspDF
    dateObjs = []
    for offset in range(fromOffset, toOffset+1):
        todayDate = dt.datetime.now()
        dateObjs.append(todayDate - dt.timedelta(offset))
    return getPspDFForDates(s, dateObjs)

def getPspDFForDates(s, dateObjs):
    pspDF = getBlankPSPDF()
    if(not type(s) is requests.sessions.Session):
        print('didnot get valid session as a function input')
        return pspDF
    if(not type(dateObjs) is list):
        print("invalid dateObjects array given for the function")
        return pspDF
    if(len(dateObjs)<1):
        print("atleast one date is required")
        return pspDF
    pspDF = getPspDF(s, dateObjs[0])
    for dateObj in dateObjs[1:]:
        pspDF = pspDF.append(getPspDF(s, dateObj), ignore_index=True)
    return pspDF

def getPspDF(s, dateObj):
    pspDF = getBlankPSPDF()
    if(not type(s) is requests.sessions.Session):
        print('didnot get valid session as a function input')
        return pspDF
    return convertPSPObjtoKeyValDF(getPspObj(s, dateObj))

def getPspObj(s, dateObj):    
    if(not type(s) is requests.sessions.Session):
        print('didnot get valid session as a function input')
        return None
    # check if date is passed into the function
    if(not type(dateObj) is dt.datetime):
        print('didnot get a valid as date object as input')
        return None    
    # parse the date string for url parameter
    try:
        dateStr = dt.datetime.strftime(dateObj, "%d-%m-%Y")
    except:
        print('didnot obtain a parsable date for the psp object fetch url param')
    
    psp_api_result = s.get(pspUrl%(dateStr))
    # get the text from response
    if(psp_api_result.status_code == requests.codes.ok):
        try:
            psp_api_dict = json.loads(psp_api_result.text)
            print('got an object from server')
            return psp_api_dict
        except ValueError:
            print('response returned was not a json object')
        except:
            print('some error occured while parsing response text')
    else:
        print('didnot get a successful response')
    return None

def getBlankPSPDF():
    pspDF = pd.DataFrame(columns=['time', 'entity' ,'key', 'value'])
    pspDF['time'] = pd.to_datetime(pspDF['time'])
    return pspDF

def convertPSPObjtoKeyValDF(pspObj):
    pspDF = getBlankPSPDF()
    # pspDF.set_index('Time',inplace=True)
    if(not type(pspObj) is dict):
        print('didnot get a valid as psp object')
        return pspDF
    for pspTableName in pspObj.keys():
        pspTableRows = pspObj[pspTableName]
        pspDF = pspDF.append(getTableRowsDF(pspTableName, pspTableRows), ignore_index=True)
    return pspDF

def getTableRowsDF(pspTableName, pspTableRows):
    tableDF = getBlankPSPDF()
    # tableDF.set_index('Time',inplace=True)
    if(pspTableName=='pspstateloaddetails'):
        entityKeyStr = 'STATE_NAME'
        dateKeyStr = 'DATE_KEY'
        keyMappings = {
                'ACTUAL_DRAWAL': 'ACTUAL_DRAWAL',
                'AVAILABILITY': 'AVAILABILITY',
                'CONSUMPTION': 'CONSUMPTION',
                'DRAWAL_SCHDULE': 'DRAWAL_SCHDULE',
                'HYDRO': 'HYDRO',
                'OTHERS': 'OTHERS',
                'REQUIREMENT': 'REQUIREMENT',
                'SHORTAGE': 'SHORTAGE',
                'SOLAR': 'SOLAR',
                'THERMAL': 'THERMAL',
                'TOTAL': 'TOTAL',
                'UI': 'UI',
                'WIND': 'WIND'
        }
    elif(pspTableName=='pspregionalavailibilitydemand'):
        entityKeyStr = 'STATE_NAME'
        dateKeyStr = 'DATE_KEY'
        keyMappings = {
                'DAY_ENERGY_DEMAND_MET': 'DAY_ENERGY_DEMAND_MET',
                'DAY_ENERGY_SHORTAGE': 'DAY_ENERGY_SHORTAGE',
                'OFF_PEAK_DEMAND_MET': 'OFF_PEAK_DEMAND_MET',
                'OFF_PEAK_FREQ': 'OFF_PEAK_FREQ',
                'OFF_PEAK_REQUIREMENT': 'OFF_PEAK_REQUIREMENT',
                'OFF_PEAK_SHORTAGE': 'OFF_PEAK_SHORTAGE',
                'PEAK_DEMAND_MET': 'PEAK_DEMAND_MET',
                'PEAK_FREQ': 'PEAK_FREQ',
                'PEAK_REQUIREMENT': 'PEAK_REQUIREMENT',
                'PEAK_SHORTAGE': 'PEAK_SHORTAGE'
        }
    elif(pspTableName=='pspinterregionalexchanges'):
        entityKeyStr = 'LINE_NAME'
        dateKeyStr = 'DATE_KEY'
        keyMappings = {
                'EXPORT_MW': 'EXPORT_MW',
                'EXPORT_MU': 'EXPORT_MU',
                'IMPORT_MW': 'IMPORT_MW',
                'IMPORT_MU': 'IMPORT_MU',
                'NET': 'NET',
                'OFF_PEAK_MW': 'OFF_PEAK_MW',
                'PEAK_MW': 'PEAK_MW'
        }
    elif(pspTableName=='pspinterregionalscheduleactual'):
        entityKeyStr = 'LINE_NAME'
        dateKeyStr = 'DATE_KEY'
        keyMappings = {
                'BILT_SCHEDULE': 'BILT_SCHEDULE',
                'ISGS_SCHEDULE': 'ISGS_SCHEDULE',
                'NET_IR_UI': 'NET_IR_UI',
                'PX_SCHEDULE': 'PX_SCHEDULE',
                'TOTAL_IR_ACTUAL': 'TOTAL_IR_ACTUAL',
                'TOTAL_IR_SCHEDULE': 'TOTAL_IR_SCHEDULE'
        }
    elif(pspTableName=='pspregionalentitiesgeneration'):
        entityKeyStr = 'CONSTITUENT_NAME'
        dateKeyStr = 'DATE_KEY'
        keyMappings = {
                'AVG_MW': 'AVG_MW',
                'DAY_ENERGY_SCHDULE': 'DAY_ENERGY_SCHDULE',
                'DAY_ENERGY_ACTUAL': 'DAY_ENERGY_ACTUAL',
                'DAY_PEAK_HRS': 'DAY_PEAK_HRS',
                'DAY_PEAK_MW': 'DAY_PEAK_MW',
                'OFF_PEAK_MW': 'OFF_PEAK_MW',
                'PEAK_MW': 'PEAK_MW'
        }
    elif(pspTableName=='pspstateentitiesgeneration'):
        entityKeyStr = 'CONSTITUENT_NAME'
        dateKeyStr = 'DATE_KEY'
        keyMappings = {
                'AVG_MW': 'AVG_MW',
                'DAY_ENERGY': 'DAY_ENERGY',
                'DAY_PEAK_HRS': 'DAY_PEAK_HRS',
                'DAY_PEAK_MW': 'DAY_PEAK_MW',
                'OFF_PEAK_MW': 'OFF_PEAK_MW',
                'PEAK_MW': 'PEAK_MW'
        }
    elif(pspTableName in ['pspVoltageProfile_400kv', 'pspVoltageProfile_765kv']):
        entityKeyStr = 'STATION_NAME'
        dateKeyStr = 'DATE_KEY'
        keyMappings = {
                'MAX_TIME': 'MAX_TIME',
                'MIN_TIME': 'MIN_TIME',
                'max_voltage': 'max_voltage',
                'min_voltage': 'min_voltage',
                'volt1_value': 'volt1_value',
                'volt2_value': 'volt2_value',
                'volt3_value': 'volt3_value',
                'volt4_value': 'volt4_value'
        }
    elif(pspTableName == 'pspstatedemandrequirement'):
        entityKeyStr = 'STATE_NAME'
        dateKeyStr = 'DATE_KEY'
        keyMappings = {
                'DEMAND_MET_MAX_REQUIREMENT': 'DEMAND_MET_MAX_REQUIREMENT',
                'MAX_DEMAND': 'MAX_DEMAND',
                'MAX_DEMAND_REQUIREMENT': 'MAX_DEMAND_REQUIREMENT',
                'MAX_DEMAND_SHORTAGE': 'MAX_DEMAND_SHORTAGE',
                'MAX_DEMAND_TIME': 'MAX_DEMAND_TIME',
                'MAX_REQUIREMENT': 'MAX_REQUIREMENT',
                'MAX_REQUIREMENT_SHORTAGE': 'MAX_REQUIREMENT_SHORTAGE',
                'MAX_REQUIREMENT_TIME': 'MAX_REQUIREMENT_TIME'
        }
    elif(pspTableName == 'pspSTOADetails1'):
        entityKeyStr = 'STATE_NAME'
        dateKeyStr = 'DATE_KEY'
        keyMappings = {
                'DE_BILT': 'DE_BILT',
                'DE_ISGS': 'DE_ISGS',
                'DE_PX': 'DE_PX',
                'DE_TOTAL': 'DE_TOTAL',
                'OP_BILATERAL': 'OP_BILATERAL',
                'OP_IEX': 'OP_IEX',
                'OP_PXIL': 'OP_PXIL',
                'PEAK_BILATERAL': 'PEAK_BILATERAL',
                'PEAK_IEX': 'PEAK_IEX',
                'PEAK_PXIL': 'PEAK_PXIL'
        }
    elif(pspTableName == 'pspSTOADetails2'):
        entityKeyStr = 'STATE_NAME'
        dateKeyStr = 'DATE_KEY'
        keyMappings = {
                'BILATERAL_MAX': 'BILATERAL_MAX',
                'BILATERAL_MIN': 'BILATERAL_MIN',
                'IEX_MAX': 'IEX_MAX',
                'IEX_MIN': 'IEX_MIN',
                'ISGS_MAX': 'ISGS_MAX',
                'ISGS_MIN': 'ISGS_MIN',
                'PXIL_MAX': 'PXIL_MAX',
                'PXIL_MIN': 'PXIL_MIN'
        }
    else:
        return tableDF
    
    if(not type(pspTableRows) is list):
        return tableDF
    
    for row in pspTableRows:
        if(not type(row) is dict):
            print('psp table row is not a dict')
            continue
        # find entity from row
        if(pspTableName=='pspregionalavailibilitydemand'):
            entity = 'WR'
        elif(pspTableName=='pspinterregionalscheduleactual'):
            entity = row.get('FROM_REGION_NAME')+'-'+row.get('TO_REGION_NAME')
        else:
            entity = row.get(entityKeyStr)
        
        # find date from row
        dateStr = str(row.get(dateKeyStr))
        if(entity == None or dateStr == None):
            print('didnot get entity or date column for the psp table row')
            continue
        try:
            dateObj = dt.datetime.strptime(dateStr, "%Y%m%d")
        except:
            print('didnot obtain a parsable date for the psp table row')
        
        # get all the key values from row
        for keyStr in keyMappings:
            tableDF = tableDF.append(dict(time=dateObj, entity=entity, key=keyMappings[keyStr], value=row.get(keyStr)), ignore_index=True)
            
    return tableDF