import numpy as np
import pandas as pd
    
#pd.read_excel(path, sheet_name=)    

# FROM FINANCIALS
TTM_REV = 16,279,000
GM      = 0.26
FC      = 
TR      = 0.35
VC      =
CaC     = 
g       = 


# DCF APPROACH
print('DCF approach:  ')
FCF     = (TTM_REV * GM - FC - CaC * g) *  (1-TR)
OA      =  
NOA     = 
ND      = 
DCF_TEV = OA + NOA - ND



# MARKET MULTIPLE APPROACH
print('Market Multiple approach:  ')
TTM_EBITDA = 2347000
Multiple = 4.5
Multiple_TEV = TTM_EBTIDA * Multiple
print(Multiple_TEV, ' Enterprise Value from Market Multiple approach')



# CBCV APPROACH
print('CBCV approach:  ')
PV_Existing_Customers = np.sum(CLTV['CLV'],axis=1)
PV_Future_Customers = np.sum(Forecast['CLV'], axis=1)
CV = PV_Existing_Customers + PV_Future_Customers
CBCV_TEV = ( (CV - FC - CAC) * (1-TR) ) + NOA - ND 
print('\n',CBCV_TEV, ' Enterprise Value from CBCV approach \n'



    


#need to state:
    # cac
        #chart cac/yer
    # actual ARPU
        #chart ARPU/yr
    # NOA
    # ND
    # FC
    # TR
    # WACC

#cohort analysis to find existing customer expected CLTV
    #and to find expected customer acquisition 