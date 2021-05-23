# -*- coding: utf-8 -*-
"""
Created on Thu May 20 19:51:44 2021

@author: Tal Fiskus
"""

import pandas as pd
from datetime import datetime

from threshold_el_gamal import Threshold_El_Gamal
import smpc_psi_p1 as smpc_p1
import smpc_psi_pi as smpc_pi

#Protocol process functions
#get player inputs from players_inputs data frame
def get_player_input(players_inputs, index):
    return players_inputs.iloc[:,index].dropna(axis=0)


def print_timestamp(msg):
    print(msg)
    print(datetime.now())

#Protocol process:
#Players types:
#P1: Star player
#Pi: every player from 2 to n

#Print timestamp at the begining of the protocol
print_timestamp("Start of protocol")

#get players data
players_inputs = pd.read_excel(r"C:\Users\user-pc\Desktop\final_project\PlayersInputs_100_5.xlsx")

#get P1 inputs
p1_input = get_player_input(players_inputs,0)

#get every Pi inputs
pi_players_input = players_inputs.drop('P1',axis=1)

# get maximum inputs of player and number of players besides P1
m_max,n = pi_players_input.shape

# set number of players
n=n+1

#Pashe 1: Key generation stage
#Threshold El Gamal
# p is prime = 7919 (the players inputs are values that are belong to the group)
teg = Threshold_El_Gamal(7919)

zp = teg.zp

#P1 and for all Pi local actions:
#choose secret key
sk = []
h_i = []
for i in range(n):
    sk.append(zp.random())
    h_i.append(teg.get_h_i(sk[i]))

#P1 recevies from every P_i his h_i, and Generates PK=<G,p,g,h>
h = teg.get_h(h_i)
#P1 shares PK with every Pi

#Pashe 2: 2PC stage
#Pi local actions:
p_i_enc_poly_cof=[]
for i in range(n-1):
    #Pi Sends encrypteds coefficients to P1 (here we append them to the list)
    p_i_enc_poly_cof.append(smpc_pi.get_enc_poly_cof_with_zero_padding(get_player_input(pi_players_input, i), h, m_max, teg))

#P1 local actions:
#P1 received all encrypted coefficients of all Pi polynoms: p_i_enc_poly_cof
#P1 calculates the total polynom: Q_1 (t) = Q_2 (t) +...+ Q_n (t)
Q1_enc_poly_cof = smpc_p1.calculate_total_poly_from_enc_polys_cof_list(p_i_enc_poly_cof,m_max,teg)

#P1 takes his inputs and creates ∀j∈{1,…,m_1 }:x_1^j∈X_1, Q_1(x_1^j)
p1_inputs = get_player_input(players_inputs, 0)
Q_x_list = smpc_p1.get_encrypted_polynoms_vals_from_inputs(p1_inputs, Q1_enc_poly_cof, teg)

#Phase 3: decrypt each of P1 encrypted values (Q_1(x_1^j)) using the threshold El-Gamal decryption scheme
mpsi=[]
for index, Q_x_i in enumerate(Q_x_list):
    #P1 sends Q_x_i for every Pi and receives the decrepted shares:
    decrpted_shares=[]
    for i in range(n):
        decrpted_shares.append(teg.decrypt_s_i(Q_x_i,sk[i]))
    if(teg.decrypt_msg(Q_x_i,decrpted_shares) == 0):
        mpsi.append(p1_inputs[index])

#print the Multi Party PSI
print(mpsi)
print(len(mpsi))

#Print timestamp at the end of the protocol
print_timestamp("End of protocol")
