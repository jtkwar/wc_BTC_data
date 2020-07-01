# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 10:21:30 2020

BTC Web-Scraping Program
Coindesk.com

@author: stark
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 17:28:27 2020

@author: stark
"""
# important relevant libraries
# import the relevant libraries for the task
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import style

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
os.chdir('C:\\Users\\stark\\Documents\\Coding\\BTC_historical_data\\')
# load the chrome driver using selenium
chrome_path = 'C:/Users/stark/Documents/Coding/'
#browser     = webdriver.Chrome(chrome_path)
driver = webdriver.Chrome(executable_path=r'C:/Users/stark/Documents/Coding/BTC_historical_data/chromedriver.exe')
# calling coindesk.com
# pull the price of the bitcoin
btc_url = 'https://www.coindesk.com/price/bitcoin'
# initialize an empty dataframe
btc_df = pd.DataFrame(columns=['DateTime', 'Curr_Prc', '24hr_per_chg', '24hr_Low', '24hr_hgh', 
                               '24hr_open', '24hr_net_chg', 'Mkt_Cap', 'Mkt_Sply'])


def grab_btc_data():
    driver.get(btc_url)
    now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    # call BeautifulSoup to extract the data from the html webpage
    soup = BeautifulSoup(driver.page_source, "html5lib")
    # btc_prc : grab data from coindesk.com on BTC
    # - Current Price (USD, string)
    # - Current 24 Change (%, string)
    # - Market Cap (USD, string)
    # - Supply (millions, M, string)
    btc_prc = soup.select('div[class*="coin-info-list price-list"]')
    # btc_act : grab data from coindesk.com on BTC
    # - 24 hour low (USD, string)
    # - 24 hour high (USD, string)
    # - Net Change (USD, string)
    # - 24 Hour open (USD, string)
    btc_act = soup.select('div[class*="coin-info-list activity-list"]')
    
    # NOW GRAB ALL THE SPECIFIC INFORMATION
    curr_prc = btc_prc[0].select('dd[class*="price-large"]')[0].text
    curr_prc = re.sub("(\$|,)", '', curr_prc)
    
    # extracts all the information from the html page
    # strips out $ and , in order to convert string into number
    chg_24hr = btc_prc[0].select('span[class*="percent-value-text"]')[0].text
    info = btc_prc[0].find_all("dd")
    mrkt_cap = info[2].string
    mrkt_cap = re.sub("(\$|,)", '', mrkt_cap)
    mrkt_sup = info[3].string
    mrkt_sup = re.sub("(\$|,)", '', mrkt_sup)
    info = btc_act[0].find_all("dd")
    low_24hr = info[0].string
    low_24hr = re.sub("(\$|,)", '', low_24hr)
    hgh_24hr = info[1].string
    hgh_24hr = re.sub("(\$|,)", '', hgh_24hr)
    hgh_low_chg = info[2].string
    hgh_low_chg = re.sub("(\$|,)", '', hgh_low_chg)
    open_24hr = btc_act[0].select('dd[class*="price-change-medium"]')[0].text
    open_24hr = re.sub("(\$|,)", '', open_24hr)
    # save the output as a string for export to .txt file
    ugh = now + ',' + curr_prc + ',' + chg_24hr + ',' + low_24hr + ',' + hgh_24hr + ',' + open_24hr + ',' + hgh_low_chg + ',' + mrkt_cap + ',' + mrkt_sup
    #temp = {'DateTime': now, 'Curr_Prc': curr_prc, '24hr_per_chg': chg_24hr, '24hr_Low': low_24hr, '24hr_hgh': hgh_24hr, 
            #'24hr_open': open_24hr, '24hr_per_chg': hgh_low_chg, '24hr_net_chg': chg_24hr, 
            #'Mkt_Cap': mrkt_cap, 'Mkt_Sply': mrkt_sup}
    # append to a dataframe for plotting and processing
    #btc_df  = btc_df.append(temp, ignore_index=True)
    #btc_df.to_csv('curr_btc_data.csv')
    #print(ugh)
    return(ugh)
# simple function for rotating what file I am writing to
def RotateFile(count, file_size, file_name):
    indX = 0
    while indX < count:  
        with open(file_name,"a") as fd:  
            ##
            # write the line to the text file
            out = grab_btc_data()
            # print for sanity
            print(out)
            fd.write(out + '\n')
            # clear the .write() buffer
            fd.flush()
            # sleep for 6 seconds
            sleep(6)
            ##  
            if int(os.path.getsize(file_name)) > file_size:
                indX += 1
                fd.close()
                file_name = "output-"+str(datetime.now().strftime("%m-%d-%Y"))+".txt"

# opens a test file to collect the data for now
#with open('output.txt', 'a+') as f:
#f = open('fuck.txt', 'a+')
#    for i in range(10000):
#        # run the web-scraping function
#        out = grab_btc_data()
#        print(out)
#        # write line to .txt file, including a new line
#        f.write(out + '\n')
        # clear the .write() buffer
#        f.flush()
#        # sleep for 6 seconds
#        sleep(6)
#    f.close()

count = 100                          ## 100 files
file_size = 10000000                 ## 10MB in size
file_name = "output.txt"             ## with this name
RotateFile(count, file_size, file_name)
