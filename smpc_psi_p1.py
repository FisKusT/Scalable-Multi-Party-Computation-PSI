# -*- coding: utf-8 -*-
"""
Created on Fri May 21 11:35:25 2021

@author: user-pc
"""

#calculate the encrypted polynom
#since this is additive el gamal we cannot perfomre multiple actions
#therfore we will run in a for loop and perform the add action x^index times on the encrypted a_i:
#each encrypted a_i will be append into c and then we will perform the add action to get the encrypted a_i*x^i
#each encrypted a_i*x^i will be append into p and then we will perform the add action to get the encrypted:
#a_0+a_1*x^1+...+a_n*x^n
def calculate_enc_poly_val(x, pi_enc_poly_cof, teg):
    enc_poly=[]
    for index, cof in enumerate(pi_enc_poly_cof):
        c=[]
        #use the value from the group of x^index, otherwise it will cause the program to loop over huge numbers
        x_power_i = teg.zp.convert_val(x**index)
        #perform a_i*x^i using the group action (since multiply is to sum multiply times)
        for j in range(x_power_i):
            c.append(cof)
        #append the encrypted a_i*x^i
        enc_poly.append(teg.add_encryptions(c))
    #return a_0 + a_1*x^1 +...+ a_n*x^n
    return teg.add_encryptions(enc_poly)

#calculate the total polynom:
#Q_1 (t) = Q_2 (t) +...+ Q_n (t)
def calculate_total_poly_from_enc_polys_cof_list(enc_polys_cof_list, m_max, teg):
    #number of maximum coefficients is the maxium input + 1 (because of a0)
    max_cof = m_max + 1
    enc_total_poly_cof=[]
    #loop over q_i for all i=0->max_cof
    for i in range(max_cof):
        enc_total_poly_cof_i = []
        #put c_2^i = Enc_PK(q_2^i ) ,..., c_n^i = Enc_PK(q_n^i ) in a list
        for cof in enc_polys_cof_list:
            enc_total_poly_cof_i.append(cof[i])
        #calculate q_i=c_2^i +...+ c_n^i = Enc_PK(q_2^i ) +...+ Enc_PK(q_n^i )= Enc_PK (q_2^i +...+ q_n^i)
        #and append q_i to coefficients list
        enc_total_poly_cof.append(teg.add_encryptions(enc_total_poly_cof_i))
    #return q_1 ,..., q_m_max in a list
    return enc_total_poly_cof

#creates ∀j∈{1,…,m_1 }:x_1^j∈X_1, Q_1(x_1^j)
def get_encrypted_polynoms_vals_from_inputs(inputs_list, total_poly, teg):
    Q_x_list = []
    for x_i in inputs_list:
        Q_x_list.append(calculate_enc_poly_val(int(x_i), total_poly, teg))
    return Q_x_list