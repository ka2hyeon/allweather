import numpy as np
import pandas as pd
from IPython.display import display, HTML
from tabulate import tabulate
from termcolor import colored

from allweather.reader import DataReader
from allweather.widget import MainWidget
pd.options.display.float_format = '{:,.2f}'.format

mapper = {
            '가격기준일': '가격기준일',
            '현재가': '현재가',
            '통화': '통화',
            '현재수량': '현재수량(개)',
            '현재가치': '현재가치(통화)',
            '현재비율': '현재비율(%)',
            '매수필요수량': '매수필요수량(개)',
            '매수후비율': '매수후비율(%)'
        }

class PortfolioManager():
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.widget = MainWidget(portfolio)
        self.data_reader = DataReader(portfolio)
        
    def summary(self, verbose = 1):
        tablefmt = 'fancy_grid' #'psql'
        won_dollor_info = self.won_dollor_info
        rebalance_info = self.rebalance_info
        abstract_df = self.get_rebalance_abstract_df(rebalance_info)

        
        dollar_won_rate = won_dollor_info['rate']
        ## set showing items
        if verbose == 0:
            df = self.rebalance_df.copy()
        if verbose == 1:
            cols = ['가격기준일',
                    '현재가',
                    '통화',
                    '현재수량',
                    '현재비율',
                    '매수필요수량',
                    '매수후비율',
                    '목표비율']
            df = self.rebalance_df[cols]
            
        ## set title
        df = df.rename(columns = mapper)

        ### summary1:  rebalance info
        print(colored('리밸런스 요약','red'))
        str1 = '희망매수금액: (달러){USD:.2f}달러, (원화){KRW:d}만원'
        str2 = '실제매수금액: (달러){USD:.2f}달러, (원화){KRW:d}만원'
        str3 = '실제매수금액 원/달러 합산: (달러기준){USD:.2f}달러, (원화기준){KRW:d}만원'
        print(str1.format(USD= rebalance_info['매수희망달러'], KRW= int(rebalance_info['매수희망원화'])))
        print(str2.format(USD= rebalance_info['실제매수금액_달러'], KRW= int(rebalance_info['실제매수금액_원화'])))
        print(str3.format(USD= rebalance_info['실제매수금액_총계_달러'], KRW= int(rebalance_info['실제매수금액_총계_원화'])))
        print('\n')
        
        ### summary2:  exchange info
        print(colored('환율정보','red'))
        print('환율기준일:', won_dollor_info['date'])
        print('기준환율:', won_dollor_info['rate']*10000)
        print('\n')

        print(colored('필요환전액','red'))
        if rebalance_info['필요환전액_원화']>=0:
            str4 = '필요환전액: (원화){KRW:d}만원 --> (달러){USD:.2f}달러'
            print(str4.format(KRW= int(rebalance_info['필요환전액_원화']), USD = rebalance_info['필요환전액_달러']))
        elif rebalance_info['필요환전액_원화']<0:                      
            str4 = '필요환전액:  (달러){USD:.2f}달러 --> (원화){KRW:d}만원'
            print(str4.format(USD = -rebalance_info['필요환전액_달러'], KRW= -int(rebalance_info['필요환전액_원화'])))
        print('\n')

        print(colored('리밸런스 결과','red'))
        #print(tabulate(df, headers='keys', tablefmt=tablefmt))
        display(df)
        print('\n')

        print(colored('리밸런스 전후비교','red'))
        #print(tabulate(abstract_df, headers='keys', tablefmt=tablefmt))
        display(abstract_df)
        
    def read_data(self):
        self.stock_data_df = self.data_reader.get_data() 
        self.rate_date, self.dollar_won_rate = self.data_reader.get_dollar_won_rate() 
        
    def rebalance(self):
        ## get widget data
        widget_valeus = self.widget.get_values() 
        target_ratio = widget_valeus['target_ratio']
        current_stock_amount = widget_valeus['current_stock_amount'] 
        current_money_amount = widget_valeus['current_money_amount']

        ## get stock data
        stock_data_df = self.stock_data_df
        rate_date, dollar_won_rate = self.rate_date, self.dollar_won_rate 

        df = stock_data_df.copy()
        currency_value = 0
        for currency, amount in current_money_amount.items():
            if currency == 'USD':
                currency_value += amount
            elif currency == 'KRW':
                currency_value += amount/dollar_won_rate

        total_current_value = 0
        total_current_dollar_value = 0; total_current_won_value = 0
        df['현재수량'] = 0; df['현재가치'] = 0
        for ticker in df.index:
            current_p = df.at[ticker, '현재가']
            currency = df.at[ticker, '통화']
            current_sa = current_stock_amount[ticker]
            total_v = current_sa*current_p

            df.at[ticker, '현재수량'] = current_sa
            df.at[ticker, '현재가치'] = total_v
            
            if currency == 'USD':
                total_current_dollar_value += total_v
                total_current_value += total_v
            elif currency == 'KRW':
                total_current_won_value+= total_v
                total_current_value += total_v/dollar_won_rate
        total_target_value = currency_value+total_current_value

        total_after_value = 0; total_required_money = 0
        total_required_dollar = 0; total_required_won = 0
        df['목표비율'] = 0; df['목표가치'] = 0; df['현재비율']=0
        df['매수필요액'] = 0; df['매수후가치'] = 0; df['매수필요수량'] = 0
        for ticker in df.index:
            currency = df.at[ticker, '통화']
            if currency == 'USD':
                current_p = df.at[ticker, '현재가']
                current_v =  df.at[ticker, '현재가치']
            elif currency == 'KRW':
                current_p = df.at[ticker, '현재가']/dollar_won_rate
                current_v =  df.at[ticker, '현재가치']/dollar_won_rate

            if total_current_value == 0:
                current_r = 0
            else:
                current_r = (current_v/total_current_value)*100

            target_r = target_ratio[ticker]
            current_a = current_stock_amount[ticker]
            
            target_v = (target_r/100)*total_target_value
            required_v = target_v-current_v
            required_a = np.around(required_v/current_p)
            required_v_rounded = required_a*current_p
            after_v = (required_a+current_a)*current_p
            total_after_value+= after_v
            total_required_money += required_v_rounded
            if currency == 'USD':
                total_required_dollar += required_v_rounded
            elif currency == 'KRW':
                total_required_won += required_v_rounded*dollar_won_rate

            df.at[ticker, '목표비율'] = target_r
            df.at[ticker, '현재비율'] = current_r
            df.at[ticker, '목표가치'] = target_v
            df.at[ticker, '매수필요액'] = required_v
            df.at[ticker, '매수필요수량'] = required_a
            df.at[ticker, '매수후가치'] = after_v
        

        overflow_dollar = current_money_amount['USD']-total_required_dollar
        overflow_won = current_money_amount['KRW']-total_required_won

        if overflow_dollar>=0 and overflow_won>=0:
            required_won_exchange = 0
            required_dollar_exchange = 0
        elif overflow_dollar<0 and overflow_won>=0:
            required_dollar_exchange = total_required_dollar - current_money_amount['USD']
            required_won_exchange = required_dollar_exchange*dollar_won_rate
        elif overflow_dollar>0 and overflow_won<0:
            required_won_exchange = current_money_amount['KRW'] - total_required_won
            required_dollar_exchange = required_won_exchange/dollar_won_rate
        elif overflow_dollar<0 and overflow_won<0:
            raise Error

        #required_won_exchange = required_dollar_exchange*dollar_won_rate
        #assert required_won_exchange + total_required_won < current_money_amount['KRW']

        # compute status after rebalancing
        df['매수후비율'] = 0
        for ticker in df.index:
            after_v = df.at[ticker, '매수후가치']
            if total_after_value == 0:
                after_r = 0
            else:
                after_r = (after_v/total_after_value)*100
            df.at[ticker, '매수후비율'] = after_r   


        self.rebalance_df = df
        self.won_dollor_info = {'date': rate_date,
                                'rate': dollar_won_rate}

        self.rebalance_info = { '매수희망달러' : current_money_amount['USD'],
                                '매수희망원화' : current_money_amount['KRW'],
                                '실제매수금액_원화': total_required_won,
                                '실제매수금액_달러': total_required_dollar,
                                '실제매수금액_총계_달러': total_required_money,
                                '실제매수금액_총계_원화': total_required_money*dollar_won_rate,
                                '필요환전액_달러': required_dollar_exchange,
                                '필요환전액_원화': required_won_exchange,
                                
                                '매수전달러자산가치_달러': total_current_dollar_value,
                                '매수전원화자산가치_원화':total_current_won_value,
                                '매수전총자산가치_달러': total_current_value,
                                '매수전총자산가치_원화': total_current_value*dollar_won_rate,

                                '매수후달러자산가치_달러': total_current_dollar_value+total_required_dollar,
                                '매수후원화자산가치_원화': total_current_won_value+total_required_won,
                                '매수후총자산가치_달러': total_after_value,
                                '매수후총자산가치_원화': total_after_value*dollar_won_rate
                                }
        return self.rebalance_df, self.won_dollor_info, self.rebalance_info


    def get_rebalance_abstract_df(self, rebalance_info):
        info =rebalance_info

        df0 = pd.DataFrame(columns = ['리밸런스전', '리밸런스후', '증감'])
        
        df1 = pd.DataFrame([[info['매수전달러자산가치_달러'], 
                            info['매수후달러자산가치_달러'],
                            info['매수후달러자산가치_달러']-info['매수전달러자산가치_달러']]], 
                            index = ['달러자산가치'], 
                            columns =  ['리밸런스전', '리밸런스후', '증감'])
        
        df2 = pd.DataFrame([[info['매수전원화자산가치_원화'], 
                            info['매수후원화자산가치_원화'],
                            info['매수후원화자산가치_원화']-info['매수전원화자산가치_원화']]], 
                            index = ['원화자산가치'], 
                            columns =  ['리밸런스전', '리밸런스후', '증감'])
        
        df3 = pd.DataFrame([[info['매수전총자산가치_달러'], 
                            info['매수후총자산가치_달러'],
                            info['매수후총자산가치_달러']-info['매수전총자산가치_달러']]], 
                            index = ['총자산합(달러))'], 
                            columns =  ['리밸런스전', '리밸런스후', '증감'])
        
        df4 = pd.DataFrame([[info['매수전총자산가치_원화'], 
                            info['매수후총자산가치_원화'],
                            info['매수후총자산가치_원화']-info['매수전총자산가치_원화']]], 
                            index = ['총자산합(만원)'], 
                            columns =  ['리밸런스전', '리밸런스후', '증감'])

        df = pd.concat([df0, df1, df2, df3, df4])
        return df

        