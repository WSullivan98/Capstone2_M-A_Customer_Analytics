<div align="center"> 
<img src='images/CBCV_venn_diagram.png' height='500'>
</div>  

# Using Advanced Customer Analytics to Value a Company 

Company valuation traditionally has been calculated two ways
1. **Discounted Cash Flow (DCF)**: a frequentist approach to project historical revenues, growth and cashflow numbers forward then discounting them for todays value of money.  


<div align="center"> 
<img src='images/DCF_EV_formula.png' height='200'>
</div>
<br>

2. **Market Multiple**: similar to pricing a home:
    * Home Price = Total SQFT * $ per SQFT from comparable homes that recently sold or are on the market
    * Company Valuation = EBTIDA * Market Multiple
        * Middle Market Median Deal Multiples - Pepperdine 2020 report:
<div align="center"> 
<img src='images/Median_Deal_Multiple_Pepperdine.png' height='300'>
</div>
<br>



With data science we can better predict revenues, growth and cashflows by segmenting customers into cohorts to:
* Model churn and retention rates for each cohort
* Model expected future amount of transactions
* Model expected average sales per transaction
* Model number of new customers per year
* Calculate average profit margin per customer
* Calculate cash flows from customers aka Customer Life Time Values (CLTV)
* Calculate sum of CLTVs by period cohorts to provide Future Cash Flows that can be discounted to todays value
<br><br>

# Wrangle Customer Data:

Company: "eChalk" is a supplier and installer of smart school equipment such as "smart boards"  
Dataset: 6 years of customer transaction history

Report example:
<div align="center">
<img src='images/Customer_Transaction_report.png' height='200'>
</div>
<br>

Company Financials:
<div align="center">
<img src='images/eChalk_5yr_IS.png' height='300'>
</div>
<br>

### Key Financials takeaways:
* Revenue               = $16,279,057
* Profit Margin         = 26%
* EBTIDA                = 2,387,000   
* WACC                  = 0.25  
* Monthly Discount Rate = 0.02

# Process & Analyze the Data:

To find CLTV we transform sales data to a RFM dataset:
* **Frequency** represents the number of repeat purchases the customer has made. This means that it’s one less than the total number of purchases.
* **Recency** represents the age of the customer when they made their most recent purchases. This is equal to the duration between a customer’s first purchase and their latest purchase. (Thus if they have made only 1 purchase, the recency is 0.)
* **T** represents the age of the customer in whatever time units chosen (daily, in our dataset). This is equal to the duration between a customer’s first purchase and the end of the period under study.
* **Monetary_Value** Total amount of Money the Customers has spent

<div align="center">
<img src='images/rfm.png' height='300'>
</div>
<br>


988 unique customers  
340 are repeat customers i.e. more than one purchase  
34.4% are repeat customers
Transactions per year  
avg sales per transaction 6 yrs  
avg sales per transaction 2020  



<div align="center">
<img src='images/order_count_histogram_eda.png' height='300'>
<img src='images/invoice_scatter.png' height='300'>
</div>
<br>


<div align="center">
<img src='images/cohort_retention.png' height='400'>
</div>
<br>


# Model Selection:


## Model Goals 
A) To predict Frequency (Number of Transactions) & Recency (Prob Alive)  
B) Predict Monetary Value aka Avg Sales per Transaction  
C) A * B = Sales/yr in order to forecast sales  

## Hyperparameters & Holdout
* T = days
* time = year 
* any additional  
* train on 2015-2019
* holdout should be 2020 
<div align="center">
<img src='images/holdout_predicted.png' height='400'>
</div>
<br>

# Model(s)

| Model        | Frequency | Recency | Monetary_Value | Output        |
|--------------|-----------|---------|----------------|---------------|
| DISCRETE     |           |         |                |               |
| BG/NBD       |     X     |         |                | Pred_Txn      |
| BG/NBD       |           |    X    |                | Prob_Alive    |
| Gamma-Gamma  |           |         |        X       | Exp_Avg_Sales |
| NON-DISCRETE |           |         |                |               |
| Pareto/NBD   |           |         |                |               |
| POP+POISSON  |           |         |                |               |
| MBG/NBD      |           |         |                |               |
| TBD          |           |         |                |               |
| BG/BB        |           |         |                |               |





# Train & Evaluate the Model
use Cross Validation Grid Search
train on training data
then evaluate on test data

# HyperParameter Tuning
t =   
t =   
t =  
holdout =  
holdout =  


# Predict with the Best Model:
<div align="center"> 
<img src='images/calculation-for-customer-lifetime-value.jpeg' height='300'>
</div>
<br>

Cohorts | Exp. Avg Value of Sales | Exp. Txn| Retention | LTV | Profit Margin | CLTV | WACC | (PV) CLTV



# CBCV Calculations



# Valuation Comparison




## noted resources
McCarthy papers  
Fader papers  
Hardie notes & papers  
lifetimes package: https://lifetimes.readthedocs.io/en/latest/index.html
Analytics Vidhya CLTV guide: https://www.analyticsvidhya.com/blog/2020/10/a-definitive-guide-for-predicting-customer-lifetime-value-clv/ 
Modelling CLTV for Non-Contractual Business with Python: https://towardsdatascience.com/whats-a-customer-worth-8daf183f8a4f
Cohort Analysis: https://towardsdatascience.com/a-step-by-step-introduction-to-cohort-analysis-in-python-a2cbbd8460ea
https://www.kdnuggets.com/2018/05/general-approaches-machine-learning-process.html
https://www.tablesgenerator.com/markdown_tables