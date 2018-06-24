## Login to site

### URL
http://103.7.130.126/POSOCOUI/Account/Login

### Request headers
```
POST /POSOCOUI/Account/Login HTTP/1.1
Host: 103.7.130.126
Connection: keep-alive
Content-Length: 43
Cache-Control: max-age=0
Origin: http://103.7.130.126
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Referer: http://103.7.130.126/POSOCOUI/Account/Login
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
```

### Form data
```
User_Name=uname&password=pass&remember=on
```

## Logout of site

### URL
http://103.7.130.126/POSOCOUI/Account/DestroySession

### Using sessions in python using the requests module
https://stackoverflow.com/questions/12737740/python-requests-and-persistent-sessions/12737874


## Get all PSP data for a date

### URL

http://103.7.130.126/POSOCOUI/PSP/GetPSPData?date=23-06-2018

### Request Headers
```
GET /POSOCOUI/PSP/GetPSPData?date=23-06-2018 HTTP/1.1
Host: 103.7.130.126
Connection: keep-alive
Accept: application/json, text/javascript, */*; q=0.01
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36
Referer: http://103.7.130.126/POSOCOUI/PSP/PSPReport
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: .ASPXAUTH=BFC462B98FB7F9336358A719A09B49D156BA386932665389EB7645504AC9ED6C59A078AC8573807014B69D00E31D9E90112F71A09B9DE778258BC7DE8CB28AFCF4EDA078BC1A1D144C9D57935624D3ABAA2D7813B1D1A42C0C5C605A999B7BCB; ASP.NET_SessionId=gqq0cwhlr12zykwrveog2mkx
```