# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 17:07:57 2018

@author: Nagasudhir
"""
import requests
import os

loginUrl = 'http://103.7.130.126/POSOCOUI/Account/Login'
logOutUrl = 'http://103.7.130.126/POSOCOUI/Account/DestroySession'

# returns the session of the website after logging in
def login():
    # get the username and password from system variables
    username = os.getenv("reports_web_uname", 'uname')
    password = os.getenv("reports_web_pass", 'pass')
    
    # setup request
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
    
    # do login post request
    loginResult = s.post(url = loginUrl, data=login_data, headers=login_headers)
    if(loginResult.status_code == requests.codes.ok):
        print('login reponse obtained...')
        #logged in! cookies saved for future requests.
        return s
    else:
        print('didnot get a successful response')
    # return None if not logged in
    return None


# logs out of the website, returns True if expected workflow occurs
def logout(s):
    # verify the type of session
    if(type(s) is not requests.sessions.Session):
        return False
    logOutResult = s.get(logOutUrl)
    if(logOutResult.status_code == requests.codes.ok):
        print('logged out of the server')
        return True
    else:
        print('didnot get a successful response')
    return False