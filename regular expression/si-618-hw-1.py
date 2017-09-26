import re
import math
# import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, read_csv,to_datetime
import numpy as np

dict={}
region_file=open('world_bank_regions.TXT','rU')
# get region:country dictionary
for line in region_file.readlines():
    result= re.findall(r'[^\t\n]+', line)
    region=result[0]
    try:
        country =str(result[2]).strip('""')
        country = str(result[2]).strip('\xe9lemy')
        country = str(result[2]).replace(",","")
        dict[country]=region
    except IndexError:
        country=str(result[1]).strip('""')
        dict[country] = region
region_area=dict.items()

def strip(x):
    x=str(x).replace('"', '')
    x=str(x).replace(',', '')
    return x

def str_function(s):
    s= str('%.5f' % s)
    return s

def math_f(i):
    s= math.log(i)
    return s

def region_match(x):
    for i in region_area:
        if x == i[0]:
            return i[1]

# use pandas to manipulate
file=pd.read_csv('world_bank_indicators.txt',sep="\t")
file.Date=pd.to_datetime(file.Date)
#filter time
t1 = pd.to_datetime('2000-07-01')
t2 = pd.to_datetime('2010-07-01')
date_df = file.loc[(file.Date== t1) | (file.Date == t2)]
# select rows and delete NA values
date2= date_df[['Country Name','Date','Population: Total (count)','Business: Mobile phone subscribers','Health: Mortality, under-5 (per 1,000 live births)','Business: Internet users (per 100 people)','Finance: GDP per capita (current US$)']]
date2.index=date2['Date']
date2=date2.dropna(how='any')
date2=date2.applymap(strip)
date2[['Population: Total (count)','Finance: GDP per capita (current US$)', 'Health: Mortality, under-5 (per 1,000 live births)','Business: Mobile phone subscribers','Finance: GDP per capita (current US$)']]= date2[['Population: Total (count)','Finance: GDP per capita (current US$)', 'Health: Mortality, under-5 (per 1,000 live births)','Business: Mobile phone subscribers','Finance: GDP per capita (current US$)']].applymap(float)
date2['Mobile subscribers per capita (divide total mobile users by total population)']= date2['Business: Mobile phone subscribers']/date2['Population: Total (count)']
date2['Mobile subscribers per capita (divide total mobile users by total population)']=date2['Mobile subscribers per capita (divide total mobile users by total population)'].apply(str_function)
date2['log(GDP per capita)']= date2[['Finance: GDP per capita (current US$)']].applymap(math_f)
date2['log(GDP per capita)']=date2['log(GDP per capita)'].apply(str_function)
date2['log(Health: mortality under 5)']= date2[['Health: Mortality, under-5 (per 1,000 live births)']].applymap(math_f)
date2['log(Health: mortality under 5)']=date2['log(Health: mortality under 5)'].apply(str_function)
date2['Region']= date2['Country Name'].apply(region_match)


# sort by time,  region , increasing GDP per capita
date2.index=pd.to_datetime(date2.index)
date2=date2.sort_index()
date2=date2.sort_values(["Region","Finance: GDP per capita (current US$)"])

data200= date2.loc['2000-07-01',['Mobile subscribers per capita (divide total mobile users by total population)','Business: Internet users (per 100 people)','Region']]
istrue=(data2001.Region=='The Americas') |  (data2001.Region=='Europe')
data2010=date2.loc['2010-07-01',['Mobile subscribers per capita (divide total mobile users by total population)','Business: Internet users (per 100 people)','Region']]
true=(data2010.Region=='The Americas') |  (data2010.Region=='Europe')

data2000[istrue].to_csv("graph1.csv")
data2010[true].to_csv("graph2.csv")














