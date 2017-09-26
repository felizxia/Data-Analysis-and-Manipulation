import re
import pandas as pd
import numpy as np
file=open('access_log.txt','rU')
new= open('invalid_access_log_felizxia.txt','w')
valid=open('valid_access_log_felizxia.txt','a')
def strip(s):
    s=s.replace(".","")
    s=s.lower()
    return s

list=[]
dicts={}
a=[]
counter={}
for line in file:
    match = re.match(r'(^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s(-\s)(\2?|[a-zA-Z]*\s)\[([0-9]{2}/[a-zA-Z]{3}/[0-9]{4}).*]\s\"[GET|POST]+\s(http://|https://)[a-zA-Z]([a-zA-Z0-9\.-]+)(\.[a-zA-Z]+)(.*?\"\s)(200)\s.*?\s\"(.*?)\"\s(.*)',line)
    if match:
        date=match.group(4)
        domain=strip(match.group(7))
        if date not in dicts:
            dicts[date] = {}
            dicts[date][domain] = 1
        else:
            if domain in dicts[date]:
                dicts[date][domain] += 1
            else:
                dicts[date][domain] = 1

file = open("valid_access_log_felizxia.txt", "w+")
for key1 in sorted(dicts):
    file.write(key1)
    for key2 in sorted(dicts[key1]):
        file.write('\t' + key2 + ':' + str(dicts[key1][key2]))
    file.write('\n')
file.close()

