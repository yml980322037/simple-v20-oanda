# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 20:12:57 2017

@author: Johan
"""

class OandaOrder:
    """
    This class encapsulates the values of an OandaOrder
    For a start it's just a simple data container
    using python properties    
    """
    def __init__(self, order_id, order_type, price, units, trade_id):
        self.__id = order_id
        self.__type = order_type
        self.price = price
        self.units = units
        self.__trade_id = trade_id
        
    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        if price <= 0:
            raise ValueError('Negative prices are not possible')
        else:
            self.__price = price
 
    @property
    def units(self):
        return self.__units
 
    @units.setter
    def units(self, units):
        self.__units = units

    """
    type property only has a getter
    """
    @property
    def type(self):
        return self.__type

    """
    id property only has a getter
    """
    @property
    def id(self):
        return self.__id

    """
    trade_id property only has a getter
    """
    @property
    def trade_id(self):
        return self.__trade_id
# 
           