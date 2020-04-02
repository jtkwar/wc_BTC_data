# wc_BTC_data
Two python scripts designed scrape the current price of BTC from coindesk.com and to open and visualize the data in real-time

**grab_btc_data.py**
This is the .py script that scrapes the following BTC information from coindesk.com periodically.
- Current Price, USD
- 24 hr open, high, low, net change and percent change

This data is then converted to a ',' delimited string and saved to a .txt file.

**plt_curr_btc_prc.py**
This script opens the saved .txt file and plots the last ten minutes of data as well as providing basic statistics (mean, std, max, and min) on the price over various time frames (1 min, 10 min, 60 min)
