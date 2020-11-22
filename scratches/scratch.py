import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from datetime import datetime
import seaborn as sb

#Timestamp for today
today_in_milliseconds = int(round(time.time() * 1000))

# Dax
dax = "https://query1.finance.yahoo.com/v7/finance/download/%5EGDAXI?period1=1577836800&period2="+str(today_in_milliseconds)+"&interval=1d&events=history"

#DowJonesIndex
dowjones = "https://query1.finance.yahoo.com/v7/finance/download/^DJI?period1=1577836800&period2="+str(today_in_milliseconds)+"&interval=1d&events=history"

#JohnHopkins update
#https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series
#time_series_covid19_confirmed_global.csv
covid_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
#time_series_covid19_deaths_global.csv
covid_death = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
#time_series_covid19_recovered_global.csv
covid_recovered = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

#gather data
df_dax = pd.read_csv(dax)
df_dow = pd.read_csv(dowjones)
df_covid_confirmed = pd.read_csv(covid_confirmed)
df_covid_death = pd.read_csv(covid_death)
df_covid_recovered = pd.read_csv(covid_recovered)

df_total = df_dax.join(df_dow, rsuffix='_DOW', lsuffix='_DAX')

#append columns
df_total = df_total.assign(covid_confirmed=None)
df_total = df_total.assign(covid_death=None)
df_total = df_total.assign(covid_recovered=None)

#merge data

for i in df_total['Date_DAX'].index:
    strDate = datetime.strptime(df_total.iat[i,0],'%Y-%m-%d').date()
    strDate = strDate.strftime('%-m/%-d/%y')
    if strDate in df_covid_confirmed:
        df_total.at[i,'covid_confirmed'] = df_covid_confirmed[strDate].sum()
        df_total.at[i, 'covid_death'] = df_covid_death[strDate].sum()
        df_total.at[i, 'covid_recovered'] = df_covid_recovered[strDate].sum()

df_total['covid_confirmed'] = df_total['covid_confirmed'].astype(float)
df_total['covid_death'] = df_total['covid_death'].astype(float)
df_total['covid_recovered'] = df_total['covid_recovered'].astype(float)

#df_total.to_csv(r'~/Desktop/File Name.csv', index = False)

#statistics

#pearsoncorr = df_total.drop(columns=['Open_DAX','Open_DOW','High_DAX','High_DOW','Low_DAX','Low_DOW','Adj Close_DAX','Adj Close_DOW','Volume_DAX','Volume_DOW'])

pearsoncorr = df_total.dropna()
pearsoncorr = pearsoncorr.corr(method='pearson')

#Corr plot
sb.heatmap(pearsoncorr,
            xticklabels=pearsoncorr.columns,
            yticklabels=pearsoncorr.index,
            cmap='RdBu_r',
            annot=True,
            linewidth=0.5)

#Plot

fig,ax1 = plt.subplots()

color ="tab:red"
#ax1.set_xlabel('time (s)')
#ax1.set_ylabel('stock market (DJI + DAX)',color=color)
#ax1.plot(df_total['Date_DAX'],df_total['Close_DAX'],label='DAX',color='coral')
#ax1.plot(df_total['Date_DAX'],df_total['Close_DOW'],label='DJI',color='crimson')
#ax1.tick_params(axis='y', labelcolor=color)

every_nth = 15
for n, label in enumerate(ax1.xaxis.get_ticklabels()):
    if n % every_nth != 0:
        label.set_visible(False)

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('Covid-19', color=color)
ax2.plot(df_total['Date_DAX'],df_total['covid_confirmed'],label='Covid Confirmed',color='C9')
ax2.plot(df_total['Date_DAX'],df_total['covid_death'],label='Covid Death',color='C7')
ax2.plot(df_total['Date_DAX'],df_total['covid_recovered'],label='Covid Recovered',color='C0')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.show()
