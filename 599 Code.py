# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 15:00:22 2021

@author: Colton
"""


import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import csv
import matplotlib.pyplot as plt
import datetime

ail_data1=pd.read_csv('C:/Users/Colton/Documents/Econ 611 MSA data/AIL and Pool Price (2010-2020).csv')
ail_data2=pd.read_csv('C:/Users/Colton/Documents/Econ 611 MSA data/AIL and Pool Price (2017-2020).csv')
temp_data=pd.read_csv('C:/Users/Colton/Documents/Econ 611 MSA data/Wide Format_Weighted Temp 2010-2021.csv')
oilfutures_data=pd.read_csv(r'C:\Users\Colton\Documents\Econ 611 MSA data\EIA NYMEX Futures (Crude Oil).csv',header=2)
oilprices_data=pd.read_csv(r'C:\Users\Colton\Documents\Econ 611 MSA data\EIA Oil Prices.csv',header=2)

#Cleaning the Data
oilfutures_data=oilfutures_data.rename(columns={"Cushing, OK Crude Oil Future Contract 1 (Dollars per Barrel)":"future 1","Cushing, OK Crude Oil Future Contract 2 (Dollars per Barrel)":"future 2","Cushing, OK Crude Oil Future Contract 3 (Dollars per Barrel)":"future 3","Cushing, OK Crude Oil Future Contract 4 (Dollars per Barrel)":"future 4"})
oilfutures_data=oilfutures_data.drop('Unnamed: 5',axis=1)
oilfutures_data['BEGIN_DATE_GMT']=pd.to_datetime(oilfutures_data["Date"])
oilfutures_data=oilfutures_data[~(oilfutures_data['BEGIN_DATE_GMT']<='2010-01-01')]
oilfutures_data['BEGIN_DATE_GMT']=pd.to_datetime(oilfutures_data['BEGIN_DATE_GMT']).dt.date
del oilfutures_data['Date']


oilprices_data=oilprices_data.rename(columns={"Cushing, OK WTI Spot Price FOB (Dollars per Barrel)":"WTI spot"})
oilprices_data['BEGIN_DATE_GMT']=pd.to_datetime(oilprices_data["Date"])
oilprices_data=oilprices_data[~(oilprices_data['BEGIN_DATE_GMT']<='2010-01-01')]
oilprices_data['BEGIN_DATE_GMT']=pd.to_datetime(oilprices_data['BEGIN_DATE_GMT']).dt.date
del oilprices_data['Date']

ail_frames=[ail_data1,ail_data2]
ail_data=pd.concat(ail_frames)
ail_data['BEGIN_DATE_GMT']=pd.to_datetime(ail_data['BEGIN_DATE'])
ail_data['hour']=ail_data['BEGIN_DATE_GMT'].dt.hour
del ail_data['BEGIN_DATE']
del ail_data['DATE']

temp_datacln=temp_data[['BEGIN_DATE_GMT','Avg temp','Weighted Avg Temp']]
temp_datacln['BEGIN_DATE_GMT']=pd.to_datetime(temp_datacln['BEGIN_DATE_GMT'])

#Merging the data -> Need to find Normalized Demand then merge back into the dataset

merged_data=ail_data.merge(temp_datacln,how="right",on=['BEGIN_DATE_GMT'])
merged_data['BEGIN_DATE_GMT']=pd.to_datetime(merged_data['BEGIN_DATE_GMT']).dt.date
merged_data=merged_data.merge(oilfutures_data,how="outer",on=['BEGIN_DATE_GMT'])
merged_data=merged_data.merge(oilprices_data,how="outer",on=['BEGIN_DATE_GMT'])

#Plots
ail_data['AIL_DEMAND']=ail_data['AIL_DEMAND'].str.replace(',','')
ail_data['AIL_DEMAND']=ail_data['AIL_DEMAND'].astype(int)
ail_data.plot('BEGIN_DATE_GMT','AIL_DEMAND')
plt.show(ail_data.plot)

temp_datacln['Avg temp']=temp_datacln['Avg temp'].astype(float)
temp_datacln['Weighted Avg Temp']=temp_datacln['Weighted Avg Temp'].astype(float)
temp_datacln.plot('BEGIN_DATE_GMT','Weighted Avg Temp')
plt.show(temp_datacln.plot)

#temp_datacln.plot('BEGIN_DATE_GMT','Avg temp')
#plt.show(temp_datacln.plot)

oilprices_data['WTI spot']=oilprices_data['WTI spot'].astype(float)
oilprices_data.plot('BEGIN_DATE_GMT','WTI spot')
plt.show(oilprices_data.plot)

oilfutures_data['future 1']=oilfutures_data['future 1'].astype(float)
oilfutures_data['future 2']=oilfutures_data['future 2'].astype(float)
oilfutures_data['future 3']=oilfutures_data['future 3'].astype(float)
oilfutures_data['future 4']=oilfutures_data['future 4'].astype(float)
oilfutures_data.set_index('BEGIN_DATE_GMT').plot()
plt.show(oilfutures_data.plot)

#Normalization Process

#Weather Related Energy
#Drop date proir to Dec 31 2020
merged_data['POOL_PRICE']=merged_data['POOL_PRICE'].str.replace('$','')
merged_data['POOL_PRICE']=merged_data['POOL_PRICE'].astype(float)
merged_data['AIL_DEMAND']=merged_data['AIL_DEMAND'].str.replace(',','')
merged_data=merged_data[~(merged_data['BEGIN_DATE_GMT']>='2020-12-31')]

