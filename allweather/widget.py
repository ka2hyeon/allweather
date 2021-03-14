import ipywidgets as iwidgets
from IPython.display import display as idisplay
from termcolor import colored

class Widgets():
    def __init__(self):
        self.widgets = {}
        self.titles = None

    def get_values(self):
        values = {}
        for key, widget in self.widgets.items():
            values[key] = widget.value
        return values

    def display(self):
        for key, widget in self.widgets.items():
            idisplay(widget)
    
    def save(self, path):
        pass

class CurrentStockAmountWidgets(Widgets):
    def __init__(self, portfolio):
        self.widgets = self.make_widgets(portfolio)
        self.titles = None

    def display(self):
        print(colored('현재 종목별 보유량을 입력하세요','red'))
        super().display()

    @classmethod
    def make_widgets(self, portfolio):
        widgets = {}
        for ticker, market, ratio in portfolio:
            widget = iwidgets.BoundedIntText(
                    value= 0,
                    min=0,
                    max=99999,
                    step=1,
                    description='%s:'%ticker,
                    disabled=False
                )
            widgets[ticker] = widget
        return widgets


class CurrentMoneyAmountWidgets(Widgets):
    def __init__(self):
        self.moneys = ['KRW', 'USD']
        self.titles = {'KRW' : 'KRW(만원)', 'USD': 'USD(달러)'}
        self.widgets = self.make_widgets(self.moneys, self.titles)
        

    def display(self):
        print(colored('매수/매도 예정 금액(원/달러)를 입력하세요','red'))
        print(colored('(음수 입력시 매도금액으로 인식합니다)','red'))
        super().display()

    @classmethod
    def make_widgets(self, tickers, titles):
        widgets = {}
        for ticker in tickers:
            widget = iwidgets.BoundedFloatText(
                    value= 0.,
                    min=0.,
                    max=9999999999.,
                    step=0.01,
                    description='%s:'%titles[ticker],
                    disabled=False
                )
            widgets[ticker] = widget
        return widgets


class TargetRatioWidgets(Widgets):
    def __init__(self, portfolio):
        self.widgets = self.make_widgets(portfolio)

    def display(self):
        print(colored('종목별 목표 비율을 입력하세요 (%)','red'))
        super().display()

    @classmethod
    def make_widgets(self, portfolio):
        widgets = {}
        for ticker, market, ratio in portfolio:
            widget = iwidgets.BoundedFloatText(
                    value= ratio,
                    min=0,
                    max=100.0,
                    step=0.1,
                    description='%s:'%ticker,
                    disabled=False
                )

            widgets[ticker] = widget
        return widgets

class MainWidget():
    def __init__(self, portfolio):
        self.target_ratio_widgets = TargetRatioWidgets(portfolio)
        self.current_money_amount_widgets = CurrentMoneyAmountWidgets()
        self.current_stock_amount_widgets = CurrentStockAmountWidgets(portfolio)

    def display_target_ratio_widgets(self):
        self.target_ratio_widgets.display()

    def display_current_money_amount_widget(self):
        self.current_money_amount_widgets.display()
    
    def display_current_stock_amount_widget(self):
        self.current_stock_amount_widgets.display()

    def get_values(self):
        target_ratio = self.target_ratio_widgets.get_values()
        current_stock_amount = self.current_stock_amount_widgets.get_values()
        current_money_amount = self.current_money_amount_widgets.get_values()

        values = {
            'target_ratio' : target_ratio,
            'current_stock_amount' : current_stock_amount,
            'current_money_amount' : current_money_amount
        }
        return values