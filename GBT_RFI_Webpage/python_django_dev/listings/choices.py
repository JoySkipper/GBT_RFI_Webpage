"""
..module:: choices.py
    :synopsis: Dictionary of all choices of receivers on the search page. 
If you wish to add a receiver, the key indicates what you want the user to see in the 
search options. The value indicates the universal name of the receiver within all GBO scripts
..moduleauthor:: Joy Skipper <jskipper@nrao.edu>
Code Origin: https://github.com/JoySkipper/GBT_RFI_Webpage
"""

receiver_choices = {
"Prime Focus":'Prime_Focus',
"L_band":'Rcvr1_2',
"S_band":'Rcvr2_3',
"C_band":'Rcvr4_6',
"X_band":'Rcvr8_10',
"Ku_band":'Rcvr12_18',
"KFPA":'RcvrArray18_26',
"Ka_band":'Rcvr26_40',
"Q_band":'Rcvr40_52',
"W_band":'Rcvr68_92',
"Argus":'RcvrArray75_115',
"MUSTANG":'RcvrMBA1_2'
}

