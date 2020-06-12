from bs4 import BeautifulSoup
import requests
import pandas as pd

def annualized_return(total_return):
    return ((1+total_return)**(1/10.5))-1

def calculate_annual_returns(df):
    yearly_returns = {
        'Year End 2009':1,
        'Year End 2010':1,
        'Year End 2011':1,
        'Year End 2012':1,
        'Year End 2013':1,
        'Year End 2014':1,
        'Year End 2015':1,
        'Year End 2016':1,
        'Year End 2017':1,
        'Year End 2018':1,
        'Year End 2019':1,
        'Year End 2020':1,
    }

    
    for i in range(0,len(df)):
        year = df.index[i].year
        if df['daily return'][i]!=0 and year!=2009:
            yearly_returns['Year End '+str(year)] *= (df['daily return'][i] + 1)
    
    for year in yearly_returns:
        yearly_returns[year] -= 1
        
    yearly_returns = pd.DataFrame.from_dict(yearly_returns, orient='index', columns=['return'])
        
    
    return yearly_returns

def calculate_risk(df):
    daily_return = df[['daily return']]
    risk = daily_return.fillna(0).std()[0]
    
    return risk

def get_beta(ticker):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    url = 'https://finance.yahoo.com/quote/{}?p={}.tsrc=fin-srch'.format(ticker,ticker)
    
    try:
        yahoo_finance = requests.get(url, headers=headers)
    except:
        beta = 'Request error, could not fetch beta'
    else:
        soup = BeautifulSoup(yahoo_finance.content, 'html.parser')
        beta = soup.find('td',attrs={'data-test':'BETA_5Y-value'}).find("span").text
    
    return beta