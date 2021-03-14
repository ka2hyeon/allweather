from collections import namedtuple

Stock = namedtuple('stock', ['ticker', 'market', 'ratio'])

class portfolio():
    def __init__(self):
        self._stocks = []
        self.make_portfolio()
        self._validity_check()

    def __iter__(self):
        self._idx = 0
        self._max_iter = len(self._stocks)
        return self

    def __next__(self):
        if self._idx >=self._max_iter:
            raise StopIteration
        else:
            item = self._stocks[self._idx]
            self._idx+=1
            return item

    def make_portfolio(self):
        raise NotImplementedError

    def add_stock(self, ticker, market, ratio):
        self._stocks.append(Stock(ticker, market, ratio))

    def _validity_check(self):
        total_ratio = 0
        for (ticker, market, ratio) in self._stocks:
            total_ratio += ratio
        if total_ratio != 100.0:
            raise Error
        
class Allweather1(portfolio):
    def make_portfolio(self):
        self.add_stock('TLT', 'US', 40.0)
        self.add_stock('IEF', 'US', 15.0)
        self.add_stock('VTI', 'US', 30.0)
        self.add_stock('GLD', 'US', 7.5)
        self.add_stock('DBC', 'US', 7.5)
        
class Allweather2(portfolio):
    def make_portfolio(self):
        self.add_stock('VTI', 'US', 12.0)
        self.add_stock('VEA', 'US', 12.0)
        self.add_stock('VWO', 'US', 12.0)
        self.add_stock('EDV', 'US', 18.0)
        self.add_stock('LTPZ', 'US', 18.0)
        self.add_stock('VCLT', 'US', 7.0)
        self.add_stock('EMLC', 'US', 7.0)
        self.add_stock('DBC', 'US', 7.0)
        self.add_stock('gold', 'krx', 7.0)


    
