'''
Author: Melissa Lawrence
Date Created: 8/16/2023
Functionality: Complete Week 10 Discussion
Notes: Week 10 discussion involves writing test scripts for functions or methods. I am chossing to do test scripts for my holdings calculations. 
'''

import unittest
from holdings_classes import Stock
from datetime import date
from dateutil.relativedelta import relativedelta

class stock_values_tests(unittest.TestCase):
    def test_earnings_per_stock_share(self):
        '''Create method to test per stock share'''      
        test_stock = Stock('Test','1.111',(date.today() - relativedelta(years=1)),2.222,1,'2')
        result = test_stock.earnings_per_stock_share()
        self.assertEqual(result,1.11)
      
    def test_earnings_per_stock_holding(self):
        '''Create method to test per stock holding'''
        test_stock = Stock('Test',1.111,(date.today() - relativedelta(years=1)),2.222,1,2)
        result = test_stock.earnings_per_stock_holding()
        self.assertEqual(result,2.22)

    def test_avg_ann_per_stock_share(self):
        '''Create method to test average 
        annual yield/loss per stock share 
        as percent increase/decrease'''
        test_stock = Stock('Test',1.111,(date.today() - relativedelta(years=1)),2.222,1,2)
        result = test_stock.avg_ann_per_stock_share()
        self.assertEqual(result,100)

def main():
        unittest.main()

if __name__ == "__main__":
        main()
      