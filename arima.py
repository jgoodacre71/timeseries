
# coding: utf-8

# In[159]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from datetime import date


# In[160]:

loansData1 = pd.read_csv('../stats/loanStats3b.csv', header=1, low_memory=False)


# In[161]:

loansData1.dropna(inplace=True)
loansData1.head()
loansData1['issue_d'].head()


                # converts string to datetime object in pandas:
                
# In[162]:

loansData1['issue_d_format'] = pd.to_datetime(loansData1['issue_d'])
dfts = loansData1.set_index('issue_d_format') 
year_month_summary = dfts.groupby(lambda x : x.year * 100 + x.month).count()
loan_count_summary = year_month_summary['issue_d']


# In[163]:

loan_count_summary.plot()

#I dont like the way this is graphing and want to see dates on the axis
from dateutil import parser
g= lambda x : str(x)+"01"

loan_count_summary_datetime = pd.to_datetime(map(g,loan_count_summary.index))
loan_count_ts = pd.DataFrame(zip(loan_count_summary_datetime, loan_count_summary.values))
loan_count_timeseries = loan_count_ts.set_index(loan_count_ts[0])
del loan_count_timeseries[0]

#However surely there is a better way of manipulating data in pandas than the above?
loan_count_timeseries.plot()


# In[164]:

#loan count time series is clearly not stationary - so attempt to make it so, perhaps an OLS regression


# In[165]:

loan_count_timeseries.columns = ['Count']


# In[166]:

print loan_count_timeseries[:]


# In[167]:

print loan_count_summary


# In[173]:

df = loan_count_timeseries.reset_index()  
df.columns=['Date','Count']
df

print type(df['Count'])
print type(df['Date'])

df1 = loan_count_summary.reset_index()


# In[174]:

print df1


# In[172]:


res = smf.ols(formula='Count ~ Date', data=df).fit()
print res.params
print res.summary()


# In[176]:

# the above is obviously rubbish but i am unsure as to what i am doing wrong after all the messing with data

res1 = smf.ols(formula='issue_d ~ index', data=df1).fit()
print res1.params
print res1.summary()

# this approach i also dont like as the time series are at equal intervals but if the regression treats as number
# then this is clearly not the case - finding this awkward to manipulate - could do in 1 min in excel


# In[188]:

# so both the regressions i have done arent right, i am struggling to manipulate things in pandas and also formats
# such as dates - the OLS is obviously garbage in garbage out
# the idea would be to take the regression dift off the time series and create a stationary series then do autocorr tests
# so the following will now be flawed given the OLS didnt work - so just working on raw unadjusted data


acf = sm.graphics.tsa.plot_acf(loan_count_summary)
pacf = sm.graphics.tsa.plot_pacf(loan_count_summary)


# In[189]:

acf1 = sm.graphics.tsa.plot_acf(loan_count_timeseries)
pacf1 = sm.graphics.tsa.plot_pacf(loan_count_timeseries)


# In[189]:




# In[189]:




# In[ ]:



