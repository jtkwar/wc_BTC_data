# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 10:27:47 2020

Program to plot the Current BTC Price vs. Time
Live Plot

Opens the current .txt file
Extracts the information into a dataframe
Plots the BTC Price vs. Time

@author: stark
"""

# important relevant libraries
# import the relevant libraries for the task
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.gridspec as gridspec

# ability to scrap the webpage and access chrome automatically
from bs4 import BeautifulSoup
from selenium import webdriver

import re
import requests
import scipy
from PyAstronomy import pyasl
from datetime import date, timedelta, datetime
import time
from time import sleep
import schedule

import smtplib
os.chdir('C:\\Users\\stark\\Documents\\Coding\\')

# some plot initializations
plt.ion()
plt.style.use('ggplot')
# column names for tables in the over-figure
columns = ['Open', 'Low (USD)', 'High (USD)', 'Net Change (USD)', 'Percent Change']
cinqmin_cols = ['~10 min Mean', '~10 min Stdev', '~10 min Max', '~10 min Min']
min_cols = ['~1 min Mean', '~1 min Stdev', '~1 min Max', '~1 min Min']
hora_cols = ['~60 min Mean', '~60 min Stdev', '~60 min Max', '~60 min Min']
# define the over-figure and the number of subplots
#fig, axs =plt.subplots(4,1) 




fig = plt.figure(figsize=(20,20))
gs = gridspec.GridSpec(nrows=4, ncols=2, height_ratios=[1, 0.1, 0.2, 0.2], figure=fig)
axs0 = fig.add_subplot(gs[0,:])
axs1 = fig.add_subplot(gs[2,0])
axs2 = fig.add_subplot(gs[2,1])
axs3 = fig.add_subplot(gs[3,0])
axs4 = fig.add_subplot(gs[3,1])
# animation function
def animate(i):
    # read in the csv as a dataframe
    data = pd.read_csv('output.txt', sep=",", header=None)
    # define the names to the columns of the loaded dataframe
    data.columns = ['DateTime', 'Curr_Prc', '24hr_per_chg', '24hr_low', '24hr_hgh', 
                    '24hr_open', '24hr_net_chg', 'Mkt_Cap', 'Mkt_Sply']
    # drop all null lines in the dataframe
    data.dropna(inplace=True)
    # set the type of some of the columns for the data frame, conversion to ints to allow for plotting
    data.astype({'Curr_Prc': 'int32', '24hr_per_chg': 'int32', '24hr_low': 'int32', '24hr_hgh': 'int32', 
               '24hr_open': 'int32', '24hr_per_chg': 'int32', '24hr_net_chg': 'int32'}).dtypes
    
    # clear the plot and tables at each iteration
    axs0.clear()
    axs1.clear()
    axs2.clear()
    axs3.clear()
    axs4.clear()
    
    # plot the current BTC price versus time
    axs0.plot(data['DateTime'][-100:], data['Curr_Prc'][-100:], 'ko-', linewidth=2, markersize=6, label='Current Price, USD')
    plt.setp(axs0.xaxis.get_majorticklabels(), rotation=45)
    # plot the ~10 min average of current BTC price
    axs0.axhline(np.mean(data['Curr_Prc'][-100:]), label = '~10 min Mean')
    # plot axes titles and legends
    axs0.set_title('Current BTC Price (USD) vs. Time')
    axs0.set_xlabel('Time')
    axs0.set_ylabel('BTC Price, USD')
    axs0.legend()
    axs0.set_aspect('equal')
    
    # Table for calculating the ~10 min mean, std, min and max
    cell_text1 = [[str(round(np.mean(data['Curr_Prc'][-10:]), 2)), 
                   str(round(np.std(data['Curr_Prc'][-10:]), 2)),
                   str(max(data['Curr_Prc'][-10:])),
                   str(min(data['Curr_Prc'][-10:]))]]
    # eliminate the axes for a clean table
    axs1.axis('tight')
    axs1.axis('off')
    # implement table
    axs1.table(cellText=cell_text1,colLabels=min_cols, cellLoc='center',loc='center')
    axs1.set_title('~1 min BTC Price Summary')
    
    # Table for calculating the ~10 min mean, std, min and max
    cell_text2 = [[str(round(np.mean(data['Curr_Prc'][-100:]), 2)), 
                   str(round(np.std(data['Curr_Prc'][-100:]), 2)),
                   str(max(data['Curr_Prc'][-100:])),
                   str(min(data['Curr_Prc'][-100:]))]]
    # eliminate the axes for a clean table
    axs2.axis('tight')
    axs2.axis('off')
    # implement table
    axs2.table(cellText=cell_text2,colLabels=cinqmin_cols, cellLoc='center',loc='center')
    axs2.set_title('~10 min BTC Price Summary')
    
    # Table for calculating the ~60 min mean, std, min and max
    cell_text3 = [[str(round(np.mean(data['Curr_Prc'][-1000:]), 2)), 
                   str(round(np.std(data['Curr_Prc'][-1000:]), 2)),
                   str(max(data['Curr_Prc'][-1000:])),
                   str(min(data['Curr_Prc'][-1000:]))]]
    # eliminate the axes for a clean table
    axs3.axis('tight')
    axs3.axis('off')
    # implement table
    axs3.table(cellText=cell_text3,colLabels=hora_cols, cellLoc='center',loc='center')
    axs3.set_title('~60 min BTC Price Summary')
    
    posneg = "g"
    if data['24hr_net_chg'].iloc[-1] < 0:
        posneg = "r"
    # Table for printing the 24 hour information from coindesk.com
    # the latest information from coindesk.com
    colors = [["w","w","w",posneg,posneg]]
    cell_text4 = [[str(data['24hr_open'].iloc[-1]), str(data['24hr_low'].iloc[-1]), 
                 str(data['24hr_hgh'].iloc[-1]), str(data['24hr_net_chg'].iloc[-1]), 
                 str(data['24hr_per_chg'].iloc[-1])]]
    # implement table
    axs4.table(cellText=cell_text4,colLabels=columns, cellLoc='center',
       loc='center', cellColours=colors)
    # table title
    axs4.set_title('24 Hr BTC Data')
    # eliminate the axes for a clean table
    axs4.axis('tight')
    axs4.axis('off')
    #plt.subplots_adjust(bottom=0.30)
    #plt.tight_layout()

    
ani = animation.FuncAnimation(fig, animate, interval=5000)
plt.show()