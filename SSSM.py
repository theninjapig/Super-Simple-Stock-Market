from __future__ import division
from datetime import timedelta,datetime
from time import time, sleep
from numpy import array
#from functools import reduce


class Stock:
    """
    Stock class including methods to compute dividend yield, PE ratio and weighted stock price ratio
    """
    def __init__(self,Symbol,LDividend,PValue,Stype="common",FDividend=None, Price=None):
        self.Symbol=Symbol             # Symbol of Stock
        self.Stype = Stype             # Type of Stock (Common/Preferred)
        self.LDividend = LDividend     # Last Dividend
        self.FDividend = FDividend     # Fixed Dividend (Preferred Stock)
        self.PValue = PValue           # Par Value
        self.TL=[]                     # List of transactions
        self.Price=Price               # Current Price
    
    def get_Symbol(self):
        return self.Symbol
    
    def get_Price(self):
        return self.Price
        
    def findDividendY(self,Price=None):
        """ method to compute the dividend yield """
        if Price==None and (self.Price is not None):
            Price=self.Price
        if self.Stype=="common":
            try:
                return self.LDividend/Price
            except ZeroDivisionError:
                print "Oops!  That was no valid price value.  Try again..."
        else:
            try:
                return (self.LDividend*self.PValue)/Price
            except ZeroDivisionError:
                print "Oops!  That was no valid price value.  Try again..."
            
    
    def findPERatio(self,Price=None):
        """method to compute the PE ratio"""
        if Price==None and (self.Price is not None):
            Price=self.Price
        try:
                return Price/self.LDividend
        except ZeroDivisionError:
                print "Oops!  That was no valid dividend value.  Try again..."
                
    def recTrans(self,NoSh,BorS,Price,TS):
        """method to record transactions"""
        self.TL.append(Transaction(NoSh,BorS,Price,TS))
        self.Price=Price

    def get_numTrans(self):
        """method get the number of transactions"""
        return len(self.TL)
    
    def findVWSP(self):
        """ method to compute the Volume Weighted Stock Price"""
        num=0
        den=0
        ban=False
        for el in self.TL:
            if datetime.fromtimestamp(el.TS) > (datetime.now()-timedelta(minutes = 15)):
                ban=True
                num+=el.Price * el.NoSh
                den+= el.NoSh
                
        
        if ban:
            try:
                return num/den
            except ZeroDivisionError:
                print "Oops! the vwsp cannot be computed. Try again..."
        else:
            return 0
            
    def updatePrice(self,Price):
        self.Price=Price


class Transaction:
    """
    Transaction class 
    """
    def __init__(self,NoSh,BorS,Price,TS):
        self.NoSh=NoSh     # Number of shares
        self.BorS=BorS     # Buy or Sell indicator
        self.Price=Price   # Price of share
        self.TS=TS         # Timestasmp


class Market:
    """
    Market class including methods to add stock, update prices and to compute the All Shares Index.
    The method to update prices relies of a dictionary buffer and could be modified/adapted to facilitate
    integration to other modules
    """
    def __init__(self,DoS={}):
        self.DoS = DoS    # dictionary of stocks indexed by symbol

    def addStock(self,Stock):
        """ method to add stocks"""
        self.DoS[Stock.get_Symbol()]=Stock

    def get_numStocks(self):
        """ method to get the number of stocks"""
        return len(self.DoS)

    def get_Stocks(self):
        """ method to get the stocks"""
        return self.DoS

        
    def updatePrices(self,dd):
        """ method to update prices"""
        for key in dd:
            self.DoS[key].updatePrice(dd[key])
    def findAShin(self):
        """ method to computer All Share Index"""
        #return reduce(lambda x, y: x*y, [self.DoS[key].get_price() for key in self.DoS] )
        a = array([self.DoS[key].get_Price() for key in self.DoS])
        return a.prod()**(1.0/len(a))
    

if __name__ == '__main__':


    # creating stocks    
    TEA = Stock("TEA",10,100)
    POP = Stock("POP",8,100)
    ALE = Stock("ALE",23, 60)
    GIN = Stock("GIN",23, 60, Stype="preferred", FDividend=2)
    JOE = Stock("JOE",13, 250)

    # Creating the Global Beverage Corporation Exchange Market
    M=Market()

    #Adding stocks
    M.addStock(TEA)
    M.addStock(POP)
    M.addStock(ALE)
    M.addStock(GIN)
    M.addStock(JOE)


    # Checking Symbols of loaded Stocks

    print "\n The symbols of added Stocks are:"
    for key in M.DoS:
        print M.DoS[key].get_Symbol()

    #Updating prices of Stocks relying on a dictionary buffer
    current_prices={"TEA":28, "POP":30, "ALE":12, "GIN":22, "JOE":15}
    M.updatePrices(current_prices)


    #Computing the All Share Index of the Global Beverage Corporation Exchange Market
    print "\n The current All Share Index of the Global Beverage Corporation Exchange Market is:"
    print M.findAShin()
    

















    

    
