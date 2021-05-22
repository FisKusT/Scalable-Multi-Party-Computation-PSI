# -*- coding: utf-8 -*-
"""
Created on Thu May 20 22:11:27 2021

@author: user-pc
"""
from group import Zp

class Threshold_El_Gamal:
    #p must be prime number
    def __init__(self, p):
        self.zp = Zp(p)

    #h_i=g^(s_i)
    def get_h_i(self, s_i):
        return self.zp.power(self.zp.g,s_i)
    
    #h=∏(i=1->n)h_i 
    def get_h(self, h_i_list):
        h = 0
        for h_i in h_i_list:
            h = self.zp.action(h, h_i)
        return h
    
    #PK=<G,p,g,h>
    #r⟵Z_p, Enc_PK (m;r)=<g^r,h^r+g^m> 
    def encrypt(self, h, m):
        g = self.zp.g
        r = self.zp.random()
        return [self.zp.power(g,r),self.zp.action(self.zp.power(h,r),self.zp.power(g,m))]
    
    #c[0]^(s_i)+ c[0]^(s_i)
    def decrypt_s_i(self, c, s_i):
        return self.zp.power(c[0], s_i)
    
    #c[1]+[∏_(i=1->n)c[0]^(s_i)+ c[0]^(s_i)]^(-1)
    def decrypt_msg(self,c, temp_c_list):
        temp_c = 0
        for temp_c_s_i in temp_c_list:
            temp_c = self.zp.action(temp_c, temp_c_s_i)
        return self.zp.action(c[1],self.zp.inverse(temp_c))

    def add_encryptions(self,enc_list):
        c = [0,0]
        for c_i in enc_list:
            c = [self.zp.action(c[0],c_i[0]), self.zp.action(c[1],c_i[1])]
        return c
    
    def check(self):
        #Try Threshold El-Gamal
        sk1 = self.zp.random()
        sk2 = self.zp.random()
        h1 = self.get_h_i(sk1)
        h2 = self.get_h_i(sk2)
        h_list = [h1,h2]
        h = self.get_h(h_list)
        m1=3543
        m2 = 2000
        m3 = 1200
        c1 = self.encrypt(h,m1)
        c2 = self.encrypt(h,m2)
        c3 = self.encrypt(h,m3)
        c = self.add_encryptions([c1,c2,c3])
        temp_c_s_1 = self.decrypt_s_i(c, sk1)
        temp_c_s_2 = self.decrypt_s_i(c, sk2)
        temp_c_s_i = [temp_c_s_1, temp_c_s_2]
        return self.decrypt_msg(c,temp_c_s_i)
        #END of El-Gamal
        