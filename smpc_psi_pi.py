# -*- coding: utf-8 -*-
"""
Created on Fri May 21 13:09:18 2021

@author: user-pc
"""

#get the encrypted polynomial coefficients from the roots (players input)
#This will happen locally for every Pi
#If number of coefficients is smaller than the maximum size, than we padd with encrypted zeros
def get_enc_poly_cof_with_zero_padding(inputs, h, m_max, teg):
    #get poly coefficients from roots
    cof_list=vietaFormula(inputs, teg)
    cof_size = len(cof_list)
    max_cof = m_max + 1
    #pad with zeros if necessary
    if cof_size != max_cof:
        zerosToPad = max_cof - cof_size
        for i in range(zerosToPad):
            cof_list.append(0)
    enc_cof = []
    for cof in cof_list:
        #if coefficient is negative, inverse to get a value from the group
        if cof < 0:
            cof = teg.zp.inverse(cof)
        #append the encrypted coefficient
        enc_cof.append(teg.encrypt(h,teg.zp.convert_val(cof)))
    return enc_cof


#Vieta formula to get the polynomial coefficient from the roots
def vietaFormula(roots, teg):    
    m_i= len(roots)
    # Declare an array for
    # polynomial coefficient.
    cof = [0] * (m_i + 1)  
    # Set Highest Order 
    # Coefficient as 1
    cof[m_i] = 1
    for i in range(1, m_i + 1):
        for j in range(m_i - i - 1, m_i):
            cof[j] += teg.zp.convert_val(((-1) * roots[i - 1] * cof[j + 1])) 
    return cof
