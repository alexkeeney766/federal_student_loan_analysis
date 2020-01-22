#project
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import statsmodels.formula.api as smf
from statsmodels.graphics.gofplots import ProbPlot
from statsmodels.formula.api import ols
from sklearn import linear_model
linreg = linear_model.LinearRegression()


#import Preliminary data

db0 = pd.read_csv('/Users/Alex/Google Drive (alex.keeney766@gmail.com)/College /Fall 2018/Research Methods/Master1031.csv')
db0.dtypes


#run OLS model
fullmodelp = ols('List_Tuition ~ Rank + Private + CPI + Southern + Lag_APGAF + Lag_AFSLAF + Lag_Applicants', db0).fit()
print(fullmodelp.summary())

model1p = ols('List_Tuition ~ Rank + Private + CPI + Lag_APGAF + Lag_AFSLAF + Lag_Applicants', db0).fit()
print(model1p.summary())


#No Private
model2p = ols('List_Tuition ~ Rank + CPI + Lag_APGAF + Lag_AFSLAF + Lag_Applicants', db0).fit()
print(model2p.summary())

# -------------------------------------------- Larger Model Creation - 123 Schools -----------------------------------------------
# 123 Schools
db1 = pd.read_excel('/Users/Alex/Google Drive (alex.keeney766@gmail.com)/College /Fall 2018/Research Methods/123 Schools DF.xlsx')
db1.dtypes


# make a merge key
def makekey(row):
    return row.institution_name + " " + str(row.year)

db1['key'] = db1.apply(makekey, axis=1)
print(db1.key) 


# Merge in Ranks
rank = pd.read_csv('/Users/Alex/Google Drive (alex.keeney766@gmail.com)/College /Fall 2018/Research Methods/Data/Ranks import 2.csv')
rank = rank.drop(['year2', 'School '], axis=1)
rank.dtypes
db1 = pd.merge(db1, rank, how='left', on='key')
db1[db1['rank'].isnull()]


# adjust for constant 2016 dollars 
cpi = pd.read_excel('/Users/Alex/Google Drive (alex.keeney766@gmail.com)/College /Fall 2018/Research Methods/Data/cpi2008-2016.xlsx')
cpi['CPI_Mult'] = cpi['cpi'].iloc[-1] / cpi['cpi']

db1 = pd.merge(db1, cpi, how='left', on='year')
db1['Constant_Tuition'] = db1.List_Tuition * db1.CPI_Mult
db1['Constant_APGF'] = db1.APGF * db1.CPI_Mult
db1['Constant_AFSLF'] = db1.AFSLF * db1.CPI_Mult
db1.dtypes
db1[['List_Tuition', 'Constant_Tuition']]

db1['Private'] = db1.Sector.replace(('Private not-for-profit, 4-year or above', 'Public, 4-year or above'), (1, 0))

# export current csv
db1.to_excel('/Users/Alex/Google Drive (alex.keeney766@gmail.com)/College /Fall 2018/Research Methods/dataframe.xlsx', sheet_name='Full Database')


# Run Models - Start here -----------------------------------------
db1 = pd.read_excel('/Users/Alex/Google Drive (alex.keeney766@gmail.com)/College /Fall 2018/Research Methods/dataframePerminant.xlsx')

NoSector0 = ols('Constant_Tuition ~ APGF + AFSLF + Applicants + rank', db1).fit()
print(NoSector.summary())

AllPreds = ols('Constant_Tuition ~ APGF + AFSLF + Applicants + rank + Private', db1).fit()
print(AllPreds.summary())

# Suggestions of strong Multicolinearity - try without applicants
NoApps = ols('Constant_Tuition ~ APGF + AFSLF + rank + Private', db1).fit()
print(NoApps.summary())


# 2008 seems to be an outlier in pell grants, or recorded wrong
db2 = db1[db1['year'] != 2008]
db2 = db2[['Constant_Tuition', 'APGF', 'AFSLF', 'rank', 'Private', 'Applicants']]

No08 = ols('Constant_Tuition ~ APGF + AFSLF + Applicants + rank + Private', db2).fit()
print(No08.summary())
#Both Applicants and Student Loans are reported insignificant

No08A = ols('Constant_Tuition ~ APGF + AFSLF + rank + Private', db2).fit()
print(No08A.summary())
#Loans are still insignificant without 08.  

corr_df = db2.corr(method='pearson')
