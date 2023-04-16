import requests
import pandas as pd
import csv
import os

l=[["VACCINE","STATE","APPLICANTS","VACCINATED","YEAR"]]
def scrape(s):
    start = 2008
    end = 2009
    name = '25122015'
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'hmis.mohfw.gov.in',
    'Referer': 'https://hmis.nhp.gov.in/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    while (end!=2021):
        if start==2014: name='29012016' 
        elif start==2015: name='12052017' 
        elif start==2016: name='15032019' 
        elif start==2018: name='27032020' 
        elif start==2019: name='06112020'
        url = f"https://hmis.mohfw.gov.in/downloadfiles?filepath=/Standard%20Reports/11~G.%20RCH%20Reports%20-%20Indicator%20Wise/2~Immunisation/{start}-{end}/MonthUpToDecember/{s}_{name}.xls"
        print(url)
        r = requests.get(url, headers = headers, verify=False)
        binary = r.content
        with open(f'{s}_{start}-{end}.xls','wb') as f:
            f.write(binary)
        start+=1
        end+=1

def modify(s):
    start = 2008
    end = 2009
    while (end!=2021):
        f_name=f"{s}_{start}-{end}.xls"
        try:
            d = pd.read_html(f_name)
        except:
            start+=1
            end+=1
            os.remove(f_name)
            continue
        for df in d:
            print(df.keys()[0])
            total=0
            for row in df.iterrows():
                total+=1
            count=0
            for row in df.iterrows():
                count+=1
                if (count==total-1 or count==total): continue
                if (row[1][1]=='.'): row[1][1]=0
                if (row[1][2]=='.'): row[1][2]=0
                if (row[1][3]=='.'): row[1][3]=0
                t=[s,row[1][1],row[1][2],row[1][3],start]
                l.append(t)
        os.remove(f_name)
        start+=1
        end+=1

vaccines=["BCG","DPT","DT","Measles","Polio","Children more than 10 years given TT10","Children more than 16 years given TT16","Vitamin A Dose-1","Vitamin A Dose-5","Vitamin A Dose-9"]
for k in vaccines:
    scrape(k)
    modify(k)

fin=[["VACCINE","STATE","APPLICANTS","VACCINATED","YEAR"]]
for a in vaccines:
    for b in range(1,37):
        state=l[b][1]
        for c in l:
            if (c[1]==state and c[0]==a):
                fin+=[c]

with open("compiled_report.csv","w",newline="") as f:
    writer = csv.writer(f)
    writer.writerows(fin)