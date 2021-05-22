# -*- coding: utf-8 -*-
"""
Created on Thu May 20 21:37:41 2021

@author: Tal Fiskus
"""

#Group Zp
from random import randrange

class Zp:
    #p must be prime number
    def __init__(self, p):
        self.p = p #prime order
        self.g = 1 #generator
    
    #perform the group action
    def action(self, num1, num2):
        return (num1 + num2) % self.p
    
    #get random value from the group
    def random(self):
        return randrange(self.p)
    
    #perform the group power action
    def power(self, num, power):
        return (num * power) % self.p
    
    #convert a number to a group number
    def convert_val(self, num):
        return num%self.p
    
    #inverse a number from the group
    def inverse(self, num):
        if num < 0:
            num = num*-1
        return self.p-(num%self.p)
    
   
