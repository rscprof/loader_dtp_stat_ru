"""Loading stats from stat.gibdd.ru for future analysis"""

import sys
import calendar
import datetime
import json
import zipfile
import io
import os
import requests

if len(sys.argv)!=3:
    print("Loading stats from stat.gibdd.ru",file = sys.stderr)
    print("Run: python3 loader.py <year> <region>", file = sys.stderr)
    print("Hint: for Moscow region is 45", file = sys.stderr)
    sys.exit(1)

YEAR = int(sys.argv[1])
REGION = sys.argv[2]

for month in range(1,13):
    _,last_day = calendar.monthrange(YEAR,month)
    date_st = datetime.date (YEAR, month, 1)
    date_end = datetime.date (YEAR,month,last_day)
    date_st_str = date_st.strftime('%d.%m.%Y')
    date_end_str = date_end.strftime('%d.%m.%Y')
    URL = 'http://stat.gibdd.ru/export/getCardsXML'
    data = {'date_st' : date_st_str, 'date_end' : date_end_str ,
            'ParReg' : '877',
            'order' : { 'type' : 1, 
                        'fieldName' : 'dat' 
                       },
            'reg' : [REGION],
            'ind' : '1',
            'exportType' : 1
            }
    headers = {
            'Content-type' : 'application/json; charset=UTF-8'
            }
    data = { 'data' : json.dumps(data) }
    print("Loading data for " + date_st.strftime("%m.%Y"),flush = True)
    
    r = requests.post(URL,data = json.dumps(data),headers = headers,timeout = 10)
    if r.status_code!=200:
        print("Status for "+URL+" with data = "+json.dumps(data)+" is "+str(r.status_code),
              file = sys.stderr)
        sys.exit(1)
    response = r.json()
    number_file = response['data']
    if number_file=="":
        print("No data for request with data = "+json.dumps(data),file = sys.stderr)
    else:
        URL = 'http://stat.gibdd.ru/getFileById?data='+number_file
        r = requests.get(URL,timeout = 10)
        if r.status_code!=200:
            print("Status for "+URL+" is "+str(r.status_code),
                  file = sys.stderr)
            sys.exit(1)
        zip_file = r.content
        with zipfile.ZipFile(io.BytesIO(zip_file)) as zipfile_object:
            zipfile_object.extract('Карточки ДТП.xml')
        os.rename('Карточки ДТП.xml',date_st.strftime('%Y_%m.xml'))
