#   Credit for Dow representation goes to Sentdex
#   Initial problems were faced regarding the syntax of pandas
#   Even when a concept seemed clear theoretically, gettings pandas to execute
#   the idea properly was difficult at times

import image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style

# Read election data
original_pres = pd.read_csv("~/Documents/cs504/python/1976-2016-president.csv")
pres = original_pres.copy()

# Clean election csv data
# Candidates that received the popular vote, but did not win the election
popular_losers = ['Clinton, Hillary', 'Gore, Al']

# Remove candidates from list to facilitate data analysis
for loser in popular_losers:
    pres = pres[pres['candidate'] != loser]

# The remaining part of the took a lot of time. First I had a for loop that
# incremented the year by 4 and ran certain operations.
# This didn't result in one clean data set but rather a dataset per year.
# This wasn't ideal and so after reading the documentation and much trial
# and error I finally found an elegant solution to isolate the election
# winners from a dirty dataset.

# Find total candidate votes per year, sum all states candidatevotes
pres = pres.groupby(['year', 'candidate', 'party'])[
                        'candidatevotes'].sum().reset_index()

# Uncomment next line to output csv with candidate votes summed up per year
#pres.to_csv("pres_sum.csv", index=False)

# Isolate only the rows containing to winning candidates
pres = pres.loc[pres.groupby('year')['candidatevotes'].idxmax()]

# Uncomment next line to output csv file containing 'winning' rows
#pres.to_csv("pres_max.csv", index=False)

pres.reset_index()

pres.drop(['candidatevotes'], axis=1, inplace=True)

original_dow = pd.read_csv('~/Documents/cs504/python/dow.csv')
dow = original_dow.copy()
#dow['20ema'] = dow['Value'].ewm(span=20).mean()

dow['Value']
# clean data and represent graph
dow['Date'] = pd.to_datetime(dow['Date'])
#dow['pcnt change'] = dow['Value'].pct_change(freq='1Y')

dow = dow.loc[dow['Date'] > '1975-1-1']
dow = dow.loc[dow['Date'] < '2016-12-31']
dow.set_index('Date', inplace=True)

#   Taking the 90D mean to make a 'per quarter' assessment
#   We can change this value if it helps
dow = dow.resample('3M').mean().reset_index()

# Convert to numpy array for the fill_between function
dates_dow = dow['Date'].values
dates_dow

# Convert 'year' column to datetime format so we can use it in fill_between
pres['year'] = pres['year'].apply(lambda x: pd.to_datetime(str(x), format='%Y'))
dates_pres = pres['year'].values

# Color based on demcrat or republican party in power
#dow.set_index('Date', inplace=True)
plt.plot(dow)

for date in dates_pres:
    party = pres.loc[pres['year'] == date, 'party'].iloc[0]
    if party == 'democrat':
        plt.fill_between(dates_dow, dow['Value'], where=dow.index > date, facecolor='blue')
    if party == 'republican':
        plt.fill_between(dates_dow, dow['Value'], where=dow.index > date, facecolor='red')












#plt.savefig('/home/tdreilloc/dow_per_term.jpg')
