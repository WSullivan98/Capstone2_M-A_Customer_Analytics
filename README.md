<div align="center"> 
<img src='images/CBCV_venn_diagram.png' height='400'>
</div>  

# Using Advanced Customer Analytics to Value a Company

Company valuation traditionally has been calculated two ways
1. Using a frequentist approach to project historical revenues, growth and cashflow numbers forward then discounting them for todays value of money.  


<div align="center"> 
<img src='images/DCF_EV_formula.png' height='200'>
</div>
<br>

2. Market approach similar to pricing a home:
    * Home Price = Total SQFT * $ per SQFT from comparable homes that recently sold or are on the market
    * Company Valuation = EBTIDA & Market Multiple

<div align="center"> 
<img src='images/Median_Deal_Multiple_Pepperdine.png' height='200'>
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

# First: data set of customer transaction histories:

Company: "eChalk" is a supplier and installer of smart school equipment such as "smart boards"  
Dataset: 5 years of customer transaction history

Report example:
<div align="center">
<img src='images/Customer_Transaction_report.png' height='400'>
</div>
<br>

Financials:
<div align="center">
<img src='images/eChalk_5yr_IS.png' height='400'>
</div>
<br>

nunique customers 990  
repeat customers i.e. more than one purchase  
repeat customer %  
Transactions per year  
avg sales per transaction 5 yrs  
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