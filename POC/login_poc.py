# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 15:12:24 2018

@author: Nagasudhir

# using sessions library - http://docs.python-requests.org/en/latest/user/advanced/#session-objects
# using sessions module for persistent sessions - https://stackoverflow.com/questions/12737740/python-requests-and-persistent-sessions/12737874

# using environment variables for storing passwords and username in python
https://stackoverflow.com/questions/15327776/python-django-avoid-saving-passwords-in-source-code

# In your powershell, type
# https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-powershell-1.0/ff730964(v=technet.10)
[Environment]::SetEnvironmentVariable("reports_web_uname", "uname", "User")
[Environment]::SetEnvironmentVariable("reports_web_pass", "pass", "User")

# In windows command prompt type
SETX reports_web_uname uname /m
SETX reports_web_pass pass /m

# In python code write
username = os.environ.get("reports_web_uname", '')
password = os.environ.get("reports_web_pass", '')
"""
import requests
import json
import os

username = os.getenv("reports_web_uname", 'uname')
password = os.getenv("reports_web_pass", 'pass')

s = requests.session()
login_data = 'User_Name=%s&password=%s&remember=on'%(username, password)

login_headers = {
'Connection': 'keep-alive',
'Content-Length': '43',
'Cache-Control': 'max-age=0',
'Upgrade-Insecure-Requests': '1',
'Content-Type': 'application/x-www-form-urlencoded',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'en-US,en;q=0.9'
        }

loginResult = s.post(url='http://103.7.130.126/POSOCOUI/Account/Login', data=login_data, headers=login_headers)
if(loginResult.status_code == requests.codes.ok):
    print('login reponse obtained...')
    #logged in! cookies saved for future requests.
else:
    print('didnot get a successful response')



# use session object from login
# get PSP data for the date 23.06.2018
psp_api_result = s.get('http://103.7.130.126/POSOCOUI/PSP/GetPSPData?date=23-06-2018')
x = json.loads('{}')
# get the text from response
if(psp_api_result.status_code == requests.codes.ok):
    try:
        psp_api_dict = json.loads(psp_api_result.text)
        print('got an object from server')
    except ValueError:
        print('response returned was not a json object')
    except:
        print('some error occured while parsing response text')
else:
    print('didnot get a successful response')
    



# logout of site
logOutResult = s.get('http://103.7.130.126/POSOCOUI/Account/DestroySession')
if(logOutResult.status_code == requests.codes.ok):
    print('logged out of the server')
else:
    print('didnot get a successful response')


    
# check the validate the structure of a response - https://stackoverflow.com/questions/45812387/how-to-validate-structure-or-schema-of-dictionary-in-python/45812483