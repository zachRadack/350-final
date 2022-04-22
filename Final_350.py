import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math as mt
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from os.path import exists

import plotly.express as px
import plotly.offline as pyo
pyo.init_notebook_mode()


url = "https://www.usinflationcalculator.com/inflation/coffee-prices-by-year-and-adjust-for-inflation/"
r = requests.get(url)
soup_text = BeautifulSoup(r.content).prettify()
with open('kaggle.html', 'wb') as fp:
    fp.write(bytes(soup_text, encoding='utf-8'))

print(fp)
browser = webdriver.Chrome()
browser.get(url)

enter_common = browser.find_element_by_xpath("//*[@id='post-21032']/div/table")

htmltable = enter_common.text
tableData = htmltable.split()[19:]

#print()
BigTableData = []
for i in range(0,len(tableData),4):
    BigTableData.append(tableData[i:i+4])
#print(BigTableData)


df1 = pd.DataFrame(data= BigTableData, columns=["Years","Prices","CPI","CPI_coffee_price" ])
df1["CPI_coffee_price"] = df1["CPI_coffee_price"].replace({'\$':''}, regex=True).astype(float)
df1 = df1[:][:-6]
#print(df1)


#https://www.kaggle.com/datasets/marshallproject/crime-rates
fname1 = "homocide.csv"
df2 = pd.read_csv(fname1)
df2.columns = [c.replace(' ', '_') for c in df2.columns]
#print(df2)
df2_years = df2["report_year"].drop_duplicates(keep='first')



#
#print(df2_condensed)
#print("==============")
statslist1 = []

cur_year = df2_years[0]

cur_year_killspercapita = 0
cur_year_rapespercapita = 0
df2['homicides_percapita'] = df2['homicides_percapita'].fillna(0)
df2['rapes_percapita'] = df2['rapes_percapita'].fillna(0)

for i, j in df2.iterrows():
    if cur_year == j[0]:
        cur_year_killspercapita+= j[11]
        cur_year_rapespercapita+=j[12]
    else:
        statslist1.append([cur_year,cur_year_killspercapita,cur_year_rapespercapita])
        cur_year_killspercapita = 0
        cur_year_rapespercapita = 0
        cur_year = j[0]

df2_condensed = pd.DataFrame(data=statslist1,columns=["report_year",'homicides_per_capita',"rapes_per_capita"])        
df2_condensed = df2_condensed[5:]



DF_Comparison =  pd.DataFrame(data=df2_condensed["homicides_per_capita"])
i = df1["CPI_coffee_price"]
DF_Comparison =DF_Comparison.join(i)
print(DF_Comparison)

fig1 = px.scatter(df1, x = 0,y = 3, trendline="ols", title="Coffee prices inflation accounted")
fig1.show()


fig2 = px.scatter(df2_condensed, x = "report_year",y = "homicides_per_capita", trendline="ols", title="murders per year")
fig2.show()
fig3 = px.scatter(df2_condensed, x = "report_year",y = "rapes_per_capita", trendline="ols", title="rapes per year")
fig3.show()
