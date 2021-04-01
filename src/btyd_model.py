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



def  CBCV_steps():
    print('Step 1: Create RFM dataframe from the dataset')
    print('Step 2: FIT Models')
    #Beta Geometric / Negative Binomial distribution model (BG/NBD) to the RFM dataframe to predict transactions (Frequency) and churn (Recency)')
    print('Step 3: PREDICT probability_alive')
    print('Step 4: PREDICT expected number of purchases, pred_num_txn')
    print('Step 5: CHECK predicted data to make sure it makes sense')
    print('TRAIN, TEST SPLIT or  CALIBRATION and HOLDOUT')
    print('Step 6: CHECK correlation of frequency & monetary_value')
    print('Step 7: FIT Gamma-Gamma model to predict monetary value')
    print('Step 8: PREDICT exp_avg_sales and compare to actual')
    print('Step 9: PREDICT Lifetime Value, predicted_ltv')
    print('Step 10: CHECK predicted_ltv to manual_predicted_ltv')
    print('Step 11: Calculate CLV by multipying predicted_ltv * profit_margin')
    print('CLTV = LTV * Profit Margin \n')
    print('CBCV approach:  ')
    # print('FCF = Customer Value - Fixed Cost * 1-Tax Rate
    print('Customer value (CV) - Fixed Cost(FC) * (1-Tax Rate) + Net Operatign Assets (NOA) - Net Debt (ND)')
    print('Customer Value = Present Value of Future Customers + Present Value of Existing Customers')
    print('Present Value of Future Customers = Number of New Customers * ( CLTV of New Customers * Customer Acquisition Costs')
    print('Possibly divide Value of Future Customer by WACC to get Present Value of Future Customers')

def create_rfm_python(data):
    customer = data.groupby('Customer ID').agg({'Date':lambda x: (x.max)() - x.min().days,
                                             'Document_Number': lambda x: len(x),
                                             'Sales Total': lambda x: sum(x)})
    customer.columns = ['Age', 'Frequency', 'Total Sales']
    return customer

def create_rfm_lifetimes(data,observation_period_end):
    summary = lifetimes.utils.summary_data_from_transaction_data(data, 
                                                                customer_id_col = 'Customer ID',
                                                                datetime_col = 'Date',
                                                                monetary_value_col= 'Sales Total',
                                                                observation_period_end=None,
                                                                freq='D')
    summary.reset_index()
    return summary




if __name__ == "__main__":
    #CBCV_steps()
    #print(os.getcwd())
    
    print('Assumptions')
    calibration_period_end='2020-09-30'
    observation_period_end='2020-12-31'
    WACC = .25
    profit_margin = 0.26


    print("Step 0: Read in customer sales data")
    data = pd.read_csv('../data/processed/sales.csv')
    print(data.head())



    print('\n Step 1: Create RFM dataframe from the dataset ')
    summary = create_rfm_lifetimes(data,observation_period_end==observation_period_end)
    summary.to_csv('../data/processed/rfm.csv')
    #dfi.export(summary, '../images/RFM_df.png', max_rows=5)
    print(summary.head(),'\n')
    #visualize it
    # fig = plt.figure(figsize=(12,8))
    # summary['frequency'].plot(kind='hist', bins=35, title='Frequency Histogram') #add labels etc.
    # plt.show()
    print('Descriptive Statistics \n' , summary['frequency'].describe())
    print('--------------------------')
    one_time_buyers = round(sum(summary['frequency'] == 0)/float(len(summary))*(100),2)
    print('Percentage of one time purchasers', one_time_buyers,'%')
    print('\n')



    print('\n\n Step 2: Fit Models')
    
    #Beta Geometric / Negative Binomial distribution model (BG/NBD) to the RFM dataframe to predict transactions (Frequency) and churn (Recency)')
    bgf = lifetimes.BetaGeoFitter(penalizer_coef=0.0)
    bgf.fit(summary['frequency'], summary['recency'], summary['T'])
    print(bgf.summary)
    #visualize
    fig = plt.figure(figsize=(12,8))
    alive = lifetimes.plotting.plot_probability_alive_matrix(bgf)
    plt.show()
    plt.savefig('../images/prob_alive.png')

    #analysis:
    # Probability Alive
    print('\n\n Step 3: Predict probability_alive \n')
    summary['probability_alive'] = bgf.conditional_probability_alive(summary['frequency'], summary['recency'], summary['T'])
    print('Mean probability a customer is alive is ' , round(summary['probability_alive'].mean(),2)*100,'%')
    print('\n', summary.head(10))

    # Predicted Number of Purchases
    print('\n\n Step 4: Predict expected number of purchases, pred_num_txn \n')
    t =365
    summary['pred_num_txn'] = round(bgf.conditional_expected_number_of_purchases_up_to_time(t, summary['frequency'], summary['recency'], summary['T']))
    print(summary.sort_values(by='pred_num_txn', ascending=False).head(10).reset_index())
    print('\n--------------------------')
    print(summary.sort_values(by='pred_num_txn').tail(5))
    

    print('\nTop 5 customers that the model expects to make a purchase in next month')




    print('\n\n Step 5: Check predicted data to make sure it makes sense \n')
    lifetimes.plotting.plot_period_transactions(bgf)
    plt.show()
    summary.to_csv('../data/processed/btyd_step5.csv')
    print(summary.sort_values(by=['pred_num_txn'],ascending=False))
    print('---------------------')
    t=30
    school = summary.loc[100625]
    print(f'/n/n Customer #, {school}, future transaction over next, {t} ,days')
    print(bgf.predict(t, school['frequency'], school['recency'], school['T']))
    # Customer is currently the index...need to create customer id and reset index
    #print(summary.columns)
    # change column to pred_num_txn_t
    # need to come back to this one




    print('\n\nTRAIN, TEST SPLIT or  CALIBRATION and HOLDOUT')
    summary_cal_holdout = lifetimes.utils.calibration_and_holdout_data(data,'Customer ID', 'Date', 
                                                                        calibration_period_end='2020-09-30',
                                                                        observation_period_end='2020-12-31')
    print(summary_cal_holdout.head())

    print('Plot calibration purchases vs holdout purchases')
    bgf.fit(summary_cal_holdout['frequency_cal'],
            summary_cal_holdout['recency_cal'],
            summary_cal_holdout['T_cal'])
    lifetimes.plotting.plot_calibration_purchases_vs_holdout_purchases(bgf,summary_cal_holdout)
    plt.show()


    print('\n\n Step 6: Check correlation of frequency & monetary_value \n')
    return_customers_summary = summary[summary['frequency']>0]
    print(return_customers_summary.head())
    print(return_customers_summary.shape)
    return_customers_summary.to_csv('../data/processed/return_customers_summary.csv')
    '''
    # # TROUBLESHOOTING: ValueError("There exist non-positive (<= 0) values in the monetary_value vector.") ValueError: There exist non-positive (<= 0) values in the monetary_value vector.
    # # line 444 on https://github.com/CamDavidsonPilon/lifetimes/blob/master/lifetimes/utils.py
    # print(return_customers_summary.describe())
    # print(return_customers_summary.info())
    # print('\n monetary_value minimum ', return_customers_summary['monetary_value'].min())
    # print('\n m<=0 ', return_customers_summary[return_customers_summary['monetary_value'] <= 0],'\n')
    # print('\n', return_customers_summary['monetary_value'] <= 0)
    '''
    print('\n',return_customers_summary[['frequency', 'monetary_value']].corr())



    print('\n\n Step 7: Fit Gamma-Gamma model to predict monetary value \n')
    ggf = lifetimes.fitters.gamma_gamma_fitter.GammaGammaFitter(penalizer_coef=0.001)
    ggf.fit(return_customers_summary['frequency'], return_customers_summary['monetary_value'] )
    print(ggf.summary)


    print('\n\n Step 8: Predict exp_avg_sales and compare to actual')
    summary = summary[summary['monetary_value']>0]
    summary['exp_avg_sales'] = ggf.conditional_expected_average_profit(summary['frequency'],summary['monetary_value'])
    print(summary.head())
    print('\n check predicted to actual:')
    print(f'Expected Average Sales:', {summary['exp_avg_sales'].mean()})
    print(f'Actual Average Sales:', {summary['monetary_value'].mean()})


    print('\n\n Step 9: Predict Lifetime Value for t, predicted_ltv')
    summary['predicted_ltv'] = ggf.customer_lifetime_value(bgf, 
                                                            summary['frequency'],
                                                            summary['recency'],
                                                            summary['T'],
                                                            summary['monetary_value'],
                                                            time=1,
                                                            freq='D',
                                                            discount_rate=WACC) #should we breakdown discount rate by 12 since t=30?
    print(summary.head())




    print('\n\n Step 10: Check predicted_ltv to manual_predicted_ltv')
    #summary['manual_predicted_ltv'] = summary['pred_num_txn'] * summary['exp_avg_sales']
    print(summary[summary['pred_num_txn']>0].head())



    print('Step 11: Calculate CLV by multipying predicted_ltv * profit_margin')
    profit_margin = 0.26
    summary['CLV'] = summary['predicted_ltv']*profit_margin
    print(summary[summary['pred_num_txn']>0].head())
    summary.to_csv('../data/processed/BTYD_CLTV.csv')
    print(summary['CLV'].sum())
    print('\n\nCLTV.csv saved')
    # Needs to actually use machine learning and have a train and test aka holdout


