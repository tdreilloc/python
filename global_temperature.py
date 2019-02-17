import image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style

def clean_mole(df):
    df = df.loc[df['year'] > 1879]
    df.set_index('year', inplace=True)
    return df

def clean_temp(df):
    df.drop(['Lowess(5)', 'Lowess(5).1'], axis=1, inplace=True)
    df = df.loc[df['Year'] < 2015]
    return df


def merge_temp_gas(df1, df2):
    df1['mole_fraction_co2'] = df2['data_mean_global'].values
    df1.set_index('Year', inplace=True)
    return df1

def draw_plot():
    # Plot style
    plt.style.use("default")
    # Subplots for future graphs
    fig, ax = plt.subplots(figsize=(10,5))
    # Copy the x-axis to initiate secondary y-axis
    ax2 = ax.twinx()
    # Primary x & y labels
    ax.set_title("Global temperature & C02 concentrations over time")
    ax.set_xlabel("Year")
    ax.set_ylabel('Celsius')
    # Plot mean annual land temperature anomalies
    ax.plot(nasa_original['Land_Annual'], color='g', label="Land temp")
    # Plot mean annual ocean temperature anomalies
    ax.plot(nasa_original['Ocean_Annual'], color='b', label="ocean temp")
    # Put legend on plot
    ax.legend(loc=0)
    # Secondary y-label
    ax2.set_ylabel("Mole Fraction C02", color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    # Plot mole fraction data on copied x-axis to make use of secondary y
    ax2.plot(nasa_original['mole_fraction_co2'], color='r', label="Mole Fraction")
    # Add secondary legend in different position to avoid overlap
    # It IS possible to get them on the same legend, haven't look into the method
    ax2.legend(loc=4)

    # calc the trendline
    z = np.polyfit(nasa_original.index, nasa_original['mole_fraction_co2'], 1)
    p = np.poly1d(z)
    plt.plot(nasa_original.index,p(nasa_original.index),"r--")
    # calc the trendline
    #z = np.polyfit(nasa_original.index, nasa_original['Land_Annual'], 1)
    #p = np.poly1d(z)
    #plt.plot(nasa_original.index,p(nasa_original.index),"r--")
    # calc the trendline
    z = np.polyfit(nasa_original.index, nasa_original['Ocean_Annual'], 1)
    p = np.poly1d(z)
    plt.plot(nasa_original.index,p(nasa_original.index),"r--")

    # Save current plot as png file
    plt.savefig("/home/tdreilloc/Documents/cs504/python/climate/temp_c02_time.png")
    plt.show()



# Read mole fraction c02
mole_fraction_co2 = pd.read_csv('/home/tdreilloc/Documents/cs504/python/climate/mole_fraction_of_carbon_dioxide_in_air_input4MIPs_GHGConcentrations_CMIP_UoM-CMIP-1-1-0_gr3-GMNHSH_0000-2014.csv')
mole_fraction_co2 = clean_mole(mole_fraction_co2)

# Read historical temperature data
nasa_original = pd.read_csv('/home/tdreilloc/Documents/cs504/python/climate/graph.csv')
nasa_original = clean_temp(nasa_original)

# Add mole fraction column to data frame to analyze correlation
temp_gas = merge_temp_gas(nasa_original, mole_fraction_co2)

nasa_original.hist()

temp_gas['Land_Annual'].corr(temp_gas['mole_fraction_co2'])
temp_gas['Ocean_Annual'].corr(temp_gas['mole_fraction_co2'])


draw_plot()



# Create figure and array of subplots for plotting
