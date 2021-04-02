import numpy as np
import pandas as pd
import datetime as dt 
import dataframe_image as dfi
import matplotlib.pyplot as plt
import os
import lifetimes
import lifetimes.utils
import lifetimes.fitters
import lifetimes.plotting
import sklearn.metrics as metrics





def create_rfm_python(data):
    customer = data.groupby('Customer ID').agg({'Date':lambda x: (x.max)() - x.min().days,
                                             'Document_Number': lambda x: len(x),
                                             'Sales Total': lambda x: sum(x)})
    customer.columns = ['Age', 'Frequency', 'Total Sales']
    return customer

def create_rfm_lifetimes(data,observation_period_end):
    #https://lifetimes.readthedocs.io/en/latest/lifetimes.html#module-lifetimes.utils 
    summary = lifetimes.utils.summary_data_from_transaction_data(data, 
                                                                customer_id_col = 'Customer ID',
                                                                datetime_col = 'Date',
                                                                monetary_value_col= 'Sales Total',
                                                                observation_period_end=None,
                                                                freq='D',
                                                                freq_multiplier=1)
    summary.reset_index()
    return summary

def eval(actuals, predicted):
    d = {'actuals',actuals,
        'predicted', predicted} 
    df = pd.concat(d, axis=1)
    df['MAE'] = metrics.mean_absolute_error(actuals, predicted)
    print(df)
    return df 



if __name__ == "__main__":

    # Assumptions/Drivers
    training_end ='2019-12-31'
    validation_end ='2020-12-31'
    WACC = .25
    monthly_discount_rate = WACC/12
    profit_margin = 0.26
    t_params= [ 1, 30, 90, 365 ]


    # LOAD AND PROCESS DATA
    # ------------------------------------------------------------------------------------------------
    transactions = pd.read_csv('../data/processed/sales.csv')
    rfm_actuals = lifetimes.utils.summary_data_from_transaction_data(transactions, 
                                                                customer_id_col = 'Customer ID',
                                                                datetime_col = 'Date',
                                                                monetary_value_col= 'Sales Total',
                                                                observation_period_end=None,
                                                                freq='D',
                                                                freq_multiplier=1)
    rfm_actuals.reset_index()
    rfm_actuals

    rfm_actuals.to_csv('../data/processed/rfm.csv')
    print(rfm_actuals.head(),'\n')
    # -------------------------------------------------------------------------------------------------




    # SPLIT
    # -----------------------------------------------------------------------------------------------------------------------------
    # https://lifetimes.readthedocs.io/en/latest/lifetimes.html#module-lifetimes.utils
    '''
    calibration_and_holdout_data() function returnds df with following _cal as calibration columns and _holdout as holdout columns:
      frequency_cal
      recency_cal
      T_cal
      frequency_holdout  
      duration_holdout = End of Period - First purchase date
    '''
    rfm_train_test = lifetimes.utils.calibration_and_holdout_data(transactions,'Customer ID', 'Date', 
                                                                        calibration_period_end=training_end,
                                                                        observation_period_end=validation_end,
                                                                        monetary_value_col='Sales Total')
    
    rfm_train_test = rfm_train_test.loc[rfm_train_test['frequency_cal'] >0,:]
    train = rfm_train_test[['frequency_cal', 'recency_cal', 'T_cal']]
    test  = rfm_train_test[['frequency_holdout', 'duration_holdout']]
    print(rfm_train_test.head())
    print(rfm_train_test.shape)

    # ---------------------------------------------------------------------------------------------------------------------------





    # TRAIN
    # -------------------------------------------------------------------------------------------------------------------------
    #Beta Geometric / Negative Binomial distribution model (BG/NBD) to predict transactions (Frequency) and churn (Recency)')
    bgf = lifetimes.BetaGeoFitter(penalizer_coef=0.0)
    bgf.fit(rfm_train_test['frequency_cal'], rfm_train_test['recency_cal'], rfm_train_test['T_cal'])
    print(bgf.summary)

    lifetimes.plotting.plot_calibration_purchases_vs_holdout_purchases(bgf,rfm_train_test)
    plt.savefig('../images/split.png')
    plt.show()

    #_________________________________________________________________________________________________________________________




    #PREDICT
    # --------------------------------------------------------------------------------------------------------------------------
    # Probability Alive
    alive_prediction_bgf= bgf.conditional_probability_alive(rfm_train_test['frequency_cal'],
                                         rfm_train_test['recency_cal'],
                                         rfm_train_test['T_cal'])
    
    rfm_train_test['probability_alive'] = alive_prediction_bgf

    print('Mean probability a customer is alive is ' , round(rfm_train_test['probability_alive'].mean(),2)*100,'%')
    print('\n', rfm_actuals.head(10))

    # Predicted Number of Purchases
    t =30
    purchase_prediction_bgf = round(bgf.conditional_expected_number_of_purchases_up_to_time(t,
                                                                              rfm_train_test['frequency_cal'],
                                                                              rfm_train_test['recency_cal'],
                                                                              rfm_train_test['T_cal']))    
    rfm_train_test['predicted_purchases'] = purchase_prediction_bgf
    print(rfm_train_test.head())
    # --------------------------------------------------------------------------------------------------------------------------


    print('\n\n Check predicted data to make sure the model makes sense \n')
    lifetimes.plotting.plot_period_transactions(bgf)
    plt.savefig('../images/period_transactions.png')
    plt.show()

    print('\n 10 Best Customers\n')
    print(rfm_train_test.sort_values(by='predicted_purchases', ascending=False).head(10).reset_index())
    print('\n--------------------------')

    print('\n\nTop 5 customers that the model expects to make a purchase in next month\n')
    print('Predicted Purchase mean :', rfm_train_test['predicted_purchases'].mean())
    print(rfm_train_test.sort_values(by='predicted_purchases').tail(5))




    # FIT GAMMMA-GAMMA MODEL
    # -------------------------------------------------------------------------------------------------------------------
    print('\n\n Check correlation of frequency & monetary_value \n')
    print('\n',rfm_train_test[['frequency_cal', 'monetary_value_cal']].corr())

    print('\n\n Fit Gamma-Gamma model to predict monetary value \n')
    ggf = lifetimes.fitters.gamma_gamma_fitter.GammaGammaFitter(penalizer_coef=0.0001)
    ggf.fit(rfm_train_test['frequency_cal'],
            rfm_train_test['monetary_value_cal'] )
    print(ggf.summary)


    # GAMMMA-GAMMA PREDICTION
    # -------------------------------------------------------------------------------------------------------------------
    print('\n\n Predict exp_avg_sales')

    monetary_pred = ggf.conditional_expected_average_profit(rfm_train_test['frequency_holdout'],
                                                       rfm_train_test['monetary_value_holdout'])
    
    rfm_train_test['exp_avg_sales'] = monetary_pred
    
    print(rfm_train_test.head())




    # PREDICT CLV
    # -------------------------------------------------------------------------------------------------------------------

    print('\n\n Predict Lifetime Value for t, predicted_ltv')
    ltv = ggf.customer_lifetime_value( bgf, 
                                        rfm_train_test['frequency_cal'],
                                        rfm_train_test['recency_cal'],
                                        rfm_train_test['T_cal'],
                                        rfm_train_test['monetary_value_cal'],
                                        time=30, # 1 yr
                                        discount_rate = 0.02
                                        )                         
                                                                
    rfm_train_test['predicted_ltv'] = ltv

    print('\n\n Calculate CLV by multipying predicted_ltv * profit_margin')
    rfm_train_test['CLV'] = rfm_train_test['predicted_ltv']*profit_margin
    print(rfm_train_test[rfm_train_test['predicted_purchases']>0].head())

    # ------------------------------------------------------------------------------------------------------------------------------




    # Evaluate
    # ------------------------------------------------------------------------------------------------------------------------------








    # RETRAINING THE MODEL
    # ------------------------------------------------------------------------------------------------------------------------------
    #RFM

    rfm = rfm_actuals = lifetimes.utils.summary_data_from_transaction_data(transactions, 
                                                                            customer_id_col = 'Customer ID',
                                                                            datetime_col = 'Date',
                                                                            monetary_value_col= 'Sales Total',
                                                                            observation_period_end=None,
                                                                            freq='D',
                                                                            freq_multiplier=1)
    rfm = rfm.loc[rfm.frequency > 0, :]


    #BG/NBD
    bgf = lifetimes.BetaGeoFitter(penalizer_coef=0.0)
    bgf.fit(rfm['frequency'], rfm['recency'], rfm['T'])


    #GG
    ggf = lifetimes.fitters.gamma_gamma_fitter.GammaGammaFitter(penalizer_coef = 0)
    ggf.fit(rfm['frequency'], rfm['monetary_value'])

    #CLV model
    ltv = ggf.customer_lifetime_value(
                                    bgf, #the model to use to predict the number of future transactions
                                    rfm['frequency'],
                                    rfm['recency'],
                                    rfm['T'],
                                    rfm['monetary_value'],
                                    time=30, # months
                                    discount_rate=0.01 # monthly discount rate ~ 12.7% annually
                                    )

    rfm['predicted_ltv'] = ltv
    rfm['CLV'] = rfm['predicted_ltv']*profit_margin
    
    
    print(rfm.head())
    
    print('rfm_actuals',rfm_actuals.mean())
    print('\n\n' )
    print('rfm_train_test',rfm_train_test.mean())
    print('\n\n' )  
    print('\n\n CLV means\n',rfm.mean())
    print('\nCLV sum ',rfm['CLV'].sum(),'\n')


    metrics.mean_absolute_error(rfm_actuals['frequency'],rfm_train_test['frequency_cal'])




    # Save the Model
    # ------------------------------------------------------------------------------------------------------------------------------
    

    # rfm.to_csv('../data/processed/BTYD_CLTV.csv')
    # print('CLV sum ',rfm_train_test['CLV'].sum())
    # print('\n\nCLTV.csv saved')




    # create scorer function 

    # pass in test and train data with time interval
    # predict
    # compare 
    # score



    # print('R-Square:', metrics.r2_score( actual purchase num 2020 , predicted purchase count 2020))
    # print('MAE:', metrics.mean_absolute_error(test, train))
    # print('MSE', metrics.mean_squared_error(test, train))
    # print('RMSE:', np.sqrt(metrics.mean_squared_error(test, train)))
