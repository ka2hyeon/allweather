import pandas as pd
import pandas_datareader as pdr

import datetime
from forex_python.converter import CurrencyRates

class DataReader():
    def __init__(self, portfolio):
        self.portfolio = portfolio
    
    def get_data(self):
        data = self.update(self.portfolio)
        return data
    
    @classmethod
    def update(self, portfolio):
        df = pd.DataFrame(columns = ['가격기준일', '현재가', '통화'])
        for port in portfolio:
            ticker = port.ticker
            market = port.market
            print('가격정보 받아오는중: %s'%ticker)

            if market == 'US':
                func_read = self.read_from_us_market
            elif market == 'krx':
                func_read = self.read_from_krx

            latest_date, latest_price, currency = func_read(ticker)
            new_df = pd.DataFrame([[latest_date, latest_price, currency]], 
                                    index = [ticker],
                                    columns =  ['가격기준일', '현재가', '통화'])
            df = pd.concat([df, new_df])
        return df
            
    @classmethod
    def read_from_us_market(self, ticker):
        today = datetime.date.today()
        #a_year_ago = today - datetime.timedelta(years=1)
        a_week_ago = today - datetime.timedelta(weeks=1)

        data = pdr.DataReader(ticker, 'yahoo', a_week_ago, today)
        latest_date = data.index[-1].to_pydatetime().strftime("%Y-%m-%d")
        latest_price = data.iloc[-1]['Close']
        currency = 'USD'
        return latest_date, latest_price, currency
        
    @classmethod
    def read_from_krx(self, ticker):
        latest_date = '2021-03-11'
        latest_price = 139
        currency = 'KRW'
        return latest_date, latest_price, currency

    @classmethod
    def get_dollar_won_rate(self):
        '''
        url = 'https://v6.exchangerate-api.com/v6/
        '''
        print('환율정보 받아오는중')
        today = datetime.date.today()
        c = CurrencyRates()
        rate = c.get_rate('USD','KRW',today)
        return today.strftime("%Y-%m-%d"), rate/10000.