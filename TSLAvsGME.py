import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
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


#Tesla:

url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data  = requests.get(url).text
soup = BeautifulSoup(html_data, 'html5lib')
tables = soup.find_all('table')
for table in tables:
    if 'Tesla Quarterly Revenue' in str(table):
        tesla_revenue = pd.read_html(str(table),flavor='bs4')[0]
tesla_revenue = tesla_revenue.rename(columns={'Tesla Quarterly Revenue(Millions of US $)': 'Date', 'Tesla Quarterly Revenue(Millions of US $).1': 'Revenue'})
#tesla_revenue = tesla_revenue.set_index('Date')
tesla_revenue
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"") # Removes the $ sign
tesla_revenue.dropna(inplace=True) # removes NA
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""] # Removes empty strings
tesla_revenue.tail(5)


# GameStop

msft = yf.Ticker("GME") # Gamestop
gme_data = msft.history(period="max") # convert the history contained in the Ticker object into a dataframe
gme_data.reset_index(inplace=True)
gme_data.head(5)
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data  = requests.get(url).text
soup = BeautifulSoup(html_data, 'html5lib')
tables = soup.find_all('table')
for table in tables:
    if 'GameStop Quarterly Revenue' in str(table):
        gme_revenue = pd.read_html(str(table),flavor='bs4')[0]
gme_revenue = gme_revenue.rename(columns={'GameStop Quarterly Revenue(Millions of US $)': 'Date', 'GameStop Quarterly Revenue(Millions of US $).1': 'Revenue'})
#gme_revenue = gme_revenue.set_index('Date')
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"") # Removes the $ sign
gme_revenue.dropna(inplace=True) # removes NA
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""] # Removes empty strings
gme_revenue

make_graph(tesla_data, tesla_revenue, 'Tesla')
make_graph(gme_data, gme_revenue, 'GameStop')
