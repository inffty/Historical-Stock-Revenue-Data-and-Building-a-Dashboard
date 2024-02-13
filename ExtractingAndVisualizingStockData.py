# Create a list
from datetime import datetime
import math
import html5lib
import matplotlib.pyplot as plt
import os
import openpyxl
import xlrd
import warnings
warnings.filterwarnings('ignore',category=DeprecationWarning)
import pandas as pd
import numpy as np
import time
import sys
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
import requests
import os
from PIL import Image
from IPython.display import IFrame
from randomuser import RandomUser
import json
import html5lib
import bs4
from bs4 import BeautifulSoup
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()





# Question 4: Use Webscraping to Extract GME Revenue Data
#Use the requests library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html. Save the text of the response as a variable named html_data.
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data=requests.get(url).text
# Parse the html data using beautiful_soup.
soup = BeautifulSoup(html_data, 'html5lib')
# Using BeautifulSoup or the read_html function extract the table with GameStop Revenue and store it into a dataframe named gme_revenue. The dataframe should have columns Date and Revenue. Make sure the comma and dollar sign is removed from the Revenue column using a method similar to what you did in Question 2.
gme_revenue=pd.DataFrame(columns=["Date","Revenue"])
for row in soup.find("tbody").find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    Revenue=col[1].text
    gme_revenue.loc[len(gme_revenue)]={"Date": date, "Revenue": Revenue}

gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace('$',"")
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',',"")
#Execute the following lines to remove an null or empty strings in the Revenue column.
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
#Display the last five rows of the gme_revenue dataframe using the tail function. Take a screenshot of the results.
print(gme_revenue.head())



# Question 3: Use yfinance to Extract Stock Data
# Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is GameStop and its ticker symbol is GME.
Ticker= yf.Ticker("GME")
#Using the ticker object and the function history extract stock information and save it in a dataframe named gme_data. Set the period parameter to max so we get information for the maximum amount of time.
gme_data = Ticker.history(period="max")
# Reset the index using the reset_index(inplace=True) function on the gme_data DataFrame and display the first five rows of the gme_data dataframe using the head function. Take a screenshot of the results and code from the beginning of Question 3 to the results below
gme_data.reset_index(inplace=True)
pd.set_option('display.max_columns', 8) # option to show all columns
print(gme_data.head())





make_graph(gme_data, gme_revenue, 'GameStop')
"""

# Question 2: Use Webscraping to Extract Tesla Revenue Data
#Use the requests library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm Save the text of the response as a variable named html_data.
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data=requests.get(url).text
# Parse the html data using beautiful_soup.
soup = BeautifulSoup(html_data, 'html5lib')
# Using BeautifulSoup or the read_html function extract the table with Tesla Revenue and store it into a dataframe named tesla_revenue. The dataframe should have columns Date and Revenue
tesla_revenue=pd.DataFrame(columns=["Date","Revenue"])
for row in soup.find("tbody").find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    Revenue=col[1].text
    tesla_revenue.loc[len(tesla_revenue)]={"Date": date, "Revenue": Revenue}
#Execute the following line to remove the comma and dollar sign from the Revenue column.
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',',"")
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace('$',"")
#Execute the following lines to remove an null or empty strings in the Revenue column.
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
#Display the last 5 row of the tesla_revenue dataframe using the tail function. Take a screenshot of the results.
print(tesla_revenue.tail())




# Question 1: Use yfinance to Extract Stock Data
#Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a
# ticker object. The stock is Tesla and its ticker symbol is TSLA

Ticker= yf.Ticker("TSLA")

#Using the ticker object and the function history extract stock information and save it in a dataframe
# named tesla_data. Set the period parameter to max so we get information for the maximum amount of time.

tesla_data = Ticker.history(period="max")
#Reset the index using the reset_index(inplace=True) function on the tesla_data DataFrame and display the first five rows of the tesla_data dataframe using the head function. Take a screenshot of the results and code from the beginning of Question 1 to the results below.

tesla_data.reset_index(inplace=True)
print(tesla_data.head())



make_graph(tesla_data, tesla_revenue, 'GameStop')

"""





"""
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/amazon_data_webpage.html"

with open ("Amazon.html","w",encoding="utf-8") as f:
    data=requests.get(url).text
    f.write(data)

soup = BeautifulSoup(data, 'html5lib')
print(soup.find("title"))
amazon_data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Volume"])


for row in soup.find("tbody").find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    Open = col[1].text
    high = col[2].text
    low = col[3].text
    close = col[4].text
    adj_close = col[5].text
    volume = col[6].text
    amazon_data.loc[len(amazon_data)]={"Date":date, "Open":Open, "High":high, "Low":low, "Close":close, "Adj Close":adj_close, "Volume":volume}
    print(date,Open,high,low,close,adj_close,volume)


print("this is new to me", amazon_data.head())
print(amazon_data.iloc[-3:])
"""
"""

data = requests.get(url).text

soup = BeautifulSoup(data, 'html5lib')


read_html_pandas_data = pd.read_html(url)
read_html_pandas_data = pd.read_html(str(soup))
netflix_dataframe = read_html_pandas_data[0]
print(netflix_dataframe.head())
"""
"""


arr = a = b = c = np.array([4, 2])


print(c.mean(),c.max(),c.min(),c.std())
x=np.linspace(0,2*np.pi,200)
y=np.sin(x)

plt.plot(x,y)
plt.show()
"""
