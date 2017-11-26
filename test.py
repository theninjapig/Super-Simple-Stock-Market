from __future__ import division
from datetime import timedelta,datetime
from time import time, sleep
from numpy import array
from SSSM import Stock, Transaction,Market
import unittest


class TestStock(unittest.TestCase):
 
    def setUp(self):
        pass

    def test_Stock_price(self):
        """Testing the method to update the Stock Price"""
        TEA = Stock("TEA",10,100)
        TEA.updatePrice(10)
        self.assertEqual( TEA.get_Price(), 10)

    def test_Dividend_Yield(self):
        """Testing the computation of the dividen Yield"""
        TEA = Stock("TEA",10,100)
        TEA.updatePrice(10)
        self.assertEqual( TEA.findDividendY(), 1)

    def test_PE_Ratio(self):
        """Testing the computation of tha PE Ratio"""
        TEA = Stock("TEA",10,100)
        TEA.updatePrice(10)
        self.assertEqual( TEA.findPERatio(), 1)

    def test_Record_Transactions(self):
        """Testing Recording Transactions"""
        POP = Stock("POP",10,100)
        POP.recTrans(NoSh=5,BorS="buy",Price=49,TS=time())
        POP.recTrans(NoSh=7,BorS="sel",Price=50,TS=time())
        POP.recTrans(NoSh=20,BorS="sel",Price=52,TS=time())
        self.assertEqual( POP.get_numTrans(), 3) 
        
    def test_VWSP(self):
        """ Testing thee computation of the Volume Weighted Stock Price"""
        TEA = Stock("TEA",10,100)
        TEA.updatePrice(10)
        self.assertEqual( TEA.findVWSP(), 0)

        TEA.recTrans(NoSh=10,BorS="buy",Price=20,TS=time())
        TEA.recTrans(NoSh=10,BorS="buy",Price=30,TS=time())
        TEA.recTrans(NoSh=10,BorS="buy",Price=10,TS=time())
        self.assertEqual( TEA.findVWSP(), 20)

    def test_Market(self):
        """Testing the Market class"""

        # Test adding Stocks to the Market
        TEA = Stock("TEA",10,100)
        POP = Stock("POP",8,100)
        ALE = Stock("ALE",23, 60)
        GIN = Stock("GIN",23, 60, Stype="preferred", FDividend=2)
        JOE = Stock("JOE",13, 250)
        
        M=Market()
        
        M.addStock(TEA)
        M.addStock(POP)
        M.addStock(ALE)
        M.addStock(GIN)
        M.addStock(JOE)

        self.assertEqual( M.get_numStocks(), 5)

        # Test updating prices in the Market
        
        #Updating prices of Stocks relying on a dictionary buffer
        current_prices={"TEA":28, "POP":30, "ALE":12, "GIN":22, "JOE":15}
        M.updatePrices(current_prices)

        for key in M.get_Stocks():
            self.assertEqual( M.get_Stocks()[key].get_Price(), current_prices[key])

        #Checking the All Share Index of the Global Beverage Corporation Exchange Market
        self.assertEqual( M.findAShin(), 20.155561176383692)

 


if __name__ == '__main__':

    unittest.main()
