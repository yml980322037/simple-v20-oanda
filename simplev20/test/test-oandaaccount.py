# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 11:45:44 2017

@author: Johan <kontakt@steunenberg.de>
"""

#from simplev20.oandasession import OandaSession
from simplev20.oandaaccount import OandaAccount
from simplev20.oandasession import OandaSession
from simplev20.oandaorder import OandaOrder

from collections import defaultdict
import unittest

class ShortStub:
    units = -50.0
class LongStub:
    units = 100.0
class V20OrderStub:
    """
    Stub class to mimick trades in OandaAccount 
    without opening a real session
    """
    def __init__(self, tradeid, order_type, price, anid):
        self.tradeID = tradeid
        self.type = order_type
        self.id = anid
        self.price = price
        self.closed = defaultdict(lambda:1)
        self.status = 0
    def close(self, account_id, order_id):
        if self.closed[order_id] == 1:
            self.closed[order_id] = 0
            self.status = 200
        else:
            self.status = 0
        return self
    def market(self, account_id, instrument, units):
        if instrument == 'USD_EUR':
            self.status = 0
        elif units == 0:
            self.status = 0
        else:
            self.status = 200
        return self
        
class V20TradeStub:
    """
    Stub class to mimick trades in OandaAccount 
    without opening a real session
    """
    def __init__(self, ticker, anid, position):
        self.instrument = ticker
        self.id = anid
        self.currentUnits = position
        
class V20PositionStub:
    """
    Stub class to mimick positions in OandaAccount 
    without opening a real session
    """
    def __init__(self, instrument = "EUR_USD"):
        self.instrument = instrument
        self.long = LongStub()
        self.short = ShortStub()
    
class V20SessionStub:
    """
    Stub class to mimick the v20 api usage in OandaAccount 
    without opening a real session
    """
    def __init__(self):
        self.account = self
        self.balance = 1000.0
        self.positions = [V20PositionStub()]
        ticker = "EUR_USD"
        self.trades = [V20TradeStub(ticker, 4711, -1000.0)]
        self.orders = [V20OrderStub(4711, 'TAKE_PROFIT', 1.1234, 4715)]
        self.trade = V20OrderStub(0, 'LIMIT', 1.1234, 4719)
        self.order = self.trade
    def get(self, someparam):
        return self
    def instruments(self,id):
        return["EUR_USD"]
    
        
class TestOandaAccount(unittest.TestCase):
    """
    The test assumes uses a V20SessionStub, so you
    don't have to connect with a real OandaSession object
    Maybe this is not what you'd want in the end
    """
    def setUp(self):
        self.api = V20SessionStub()
        self.testid = 'BLAFASEL'
        self.account = OandaAccount(self.api, self.testid)
        
    def test_create(self):
        """
        An simple test, asserting that the setup of the test
        and the constructor of the account work fine
        """
        self.assertEqual(self.api, self.account.api)
        self.assertEqual(self.testid, self.account.account_id)
        
    def test_balance(self):
        balance = self.account.get_balance()
        self.assertEqual(balance, 1000.0)
        
    def test_get_instruments_with_open_positions(self):
        instruments =self.account.get_instruments_with_open_positions()
        self.assertEqual(len(instruments), 1)
        self.assertEqual(instruments[0], "EUR_USD")
        
    def test_get_position(self):
        self.assertEqual(self.account.get_position("EUR_USD"), 50.0)
        self.assertEqual(self.account.get_position("EUR_USD", 'net'), 50.0)
        self.assertEqual(self.account.get_position("EUR_USD", 'long'), 100.0)
        self.assertEqual(self.account.get_position("EUR_USD", 'short'), -50.0)
        self.assertEqual(self.account.get_position("EUR_GBP"), 0.0)
        self.assertRaises(ValueError, self.account.get_position, ticker='EUR_USD', long_short='nett')

    def test_get_trades(self):
        # account.get_trades returns a dictionary with 
        # key = ticker, val = list of trades
        trades = self.account.get_trades()
        self.assertEqual(len(trades), 1)
        self.assertIsInstance(trades, dict)
        dollartrades = trades['EUR_USD']
        trade1 = dollartrades[0]
        self.assertEqual(trade1['ticker'], 'EUR_USD')
        self.assertEqual(trade1['id'], 4711)
        self.assertEqual(trade1['position'], -1000.0)


    def test_get_orders(self):
        orders = self.account.get_orders('EUR_USD')  
        self.assertEqual(len(orders), 1)
        self.assertIsInstance(orders, list)
        order = orders[0]
        self.assertIsInstance(order, OandaOrder)
        self.assertEqual(order.type, 'TAKE_PROFIT')
        self.assertEqual(order.units, -1000.00)
        self.assertEqual(order.price, 1.1234)
        orders = self.account.get_orders('EUR_USD', 'ALL')  
        self.assertEqual(len(orders), 1)
        orders = self.account.get_orders('EUR_USD', 'TAKE_PROFIT')  
        self.assertEqual(len(orders), 1)
        orders = self.account.get_orders('EUR_USD', 'WHATEVER')  
        self.assertEqual(len(orders), 0)
        
    # close an existing order
    def test_close_order(self):
        self.assertEqual(self.account.close_order(4719), 200)
        # can't close the same order twice
        self.assertNotEqual(self.account.close_order(4719), 200)
        
    # open a market order
    def test_market_order(self):
        ticker = 'EUR_USD'
        wrong_ticker = 'USD_EUR'
        self.assertEqual(self.account.market_order(ticker, 1), 200)
        self.assertNotEqual(self.account.market_order(wrong_ticker, 1), 200)
        self.assertNotEqual(self.account.market_order(ticker, 0), 200)
        
    # get list of tradeable instruments
    def test_get_available_instruments(self):
        #TODO: don't know how to test with dummies
        session = OandaSession()
        self.account=session.get_primary_account()
        self.assertGreater(len(self.account.get_available_instruments()),1);
    
    # this one is also hard to test with a dummy
    def test_get_bid_ask_price(self):
        session = OandaSession()
        self.account=session.get_primary_account()
        ticker = 'EUR_USD'
        bid, ask = self.account.get_bid_ask_price(ticker)
        self.assertGreater(ask, bid);
    # next steps
    # open a limit order
        
        
unittest.main()
