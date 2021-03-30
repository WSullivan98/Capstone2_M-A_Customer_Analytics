import pandas as pd
import numpy as np

def drop_cols(df, columns_to_drop):
    df.drop(columns_to_drop, inplace=True, axis=1)
    return df

def breakout_year_month(df, col):
    df[col] = pd.to_datetime(df[col])
    df['Year'] = df[col].dt.year
    # df['Year'] = pd.to_datetime(df["Year"])
    df['Month'] = df[col].dt.month
    # df['Month'] = pd.to_datetime(df["Month"])
    return df

def dollars_to_numbers(df, cols):
    for col in cols:
        df[col] = df[col].replace('\$|,', '', regex=True)
    return df

def cols_to_string(df, cols):
    for col in cols:
        df[col] = df[col].to_string()
    return df

if __name__ == "__main__":
    sales_2015 = pd.read_csv('../data/raw/CLTV Project Data/product_sales_by_state_and_customer_2015.csv')
    sales_2016 = pd.read_csv('../data/raw/CLTV Project Data/poduct_sales_by_state_and_customer_2016.csv')
    sales_2017 = pd.read_csv('../data/raw/CLTV Project Data/product_sales_by_state_and_customer_2017.csv')
    sales_2018 = pd.read_csv('../data/raw/CLTV Project Data/product_sales_by_state_and_customer_2018.csv')
    sales_2019 = pd.read_csv('../data/raw/CLTV Project Data/Product Sales by State and Customer 2019.csv')
    sales_2020 = pd.read_csv('../data/raw/CLTV Project Data/Product Sales by State and Customer 2020.csv')

    frames = [sales_2020, sales_2019, sales_2018, sales_2017, sales_2016, sales_2015]
    sales = pd.concat(frames)
    columns_to_drop = ['Item']
    sales = drop_cols(sales, columns_to_drop)
    sales = sales.rename({'Address: Billing Address State' :'State', 'Customer/Project: Company Name': 'Customer' }, axis=1)
    sales = breakout_year_month(sales, 'Date')

    col_order = ['Type', 'Date', 'Year', 'Month', 'Document Number', 'Description', 'Qty. Sold',
       'Sales Price', 'Revenue', 'State', 'Customer']
    
    sales = sales[col_order]

    convert_to_str = ['Description', 'State', 'Customer']
    cols_to_string(sales, convert_to_str )

    dollar_cols = ['Revenue', 'Sales Price']
    dollars_to_numbers(sales, dollar_cols)

    rows_to_delete = sales[sales['Type'].isnull()].shape[0]
    #print(rows_to_delete)

    print(sales.info())
    print(sales['Year'])
    #print(sales['Year'])
    #print(sales['State', 'Customer'])