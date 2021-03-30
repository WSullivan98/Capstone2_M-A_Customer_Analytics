import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import datetime as dt
import seaborn as sns 
from operator import attrgetter
import warnings
#warnings.filterwarnings("ignore")









if __name__ == "__main__":
    data = pd.read_csv('../data/processed/sales.csv')
    print(data.head())

    #print(data.describe().transpose())
    # print(data.describe())
    cols = data.columns
    descriptive_stats = pd.DataFrame(data=data.describe(),index=['Unnamed: 0'],  columns=cols).reset_index(drop=True)
    print(descriptive_stats)

    n_orders = data.groupby(['Customer ID'])['Document Number'].nunique()
    mult_orders_perc = np.sum(n_orders >1 ) / data['Customer ID'].nunique()
    print(n_orders.count(),'count of unique orders \n\n')
    print(f'{100* mult_orders_perc:.2f}% of customers ordered more than once \n')

    #HISTOGRAM
    # ax = sns.displot(n_orders, kde=False, hist=True)
    # ax.set(title='Distribution of number of orders per customer', xlabel='# of orders', ylabel='# of customers');


    # ax = sns.histplot(data=n_orders,x=['Document Number'])
    # ax.set(title='Distribution of number of orders per customer', xlabel='# of orders', ylabel='# of customers');

    # fig, ax = plt.subplots()
    # ax.hist(x=['Document Number'],data=n_orders)
    # plt.show()


    # min_year = data.groupby(['Customer'])['Year'].min()
    # data['Cohort Year'] = data.apply(lambda row: min_year.loc[row['Customer']],axis=1)

    # cohorts = data.groupby(data['Cohort Year'])['Customer'].nunique()
    # print(cohorts.sum())
    # cohorts.plot.bar();



    df = data[['Customer ID', 'Document Number', 'Year']].drop_duplicates()
    # df['order_month'] = df['Date'].to_period('')
    df['cohort'] = df.groupby('Customer ID')['Year'].transform('min')

    df_cohort = df.groupby(['cohort', 'Year']).agg(n_customers=('Customer ID', 'nunique')).reset_index(drop=False)
    df_cohort['period_number'] = (df_cohort.Year - df_cohort.cohort)

    cohort_pivot = df_cohort.pivot_table(index = 'cohort',
                                        columns = 'period_number',
                                        values = 'n_customers')

    cohort_size = cohort_pivot.iloc[:,0]
    retention_matrix = cohort_pivot.divide(cohort_size, axis=0) 

    with sns.axes_style("white"):
        fig, ax = plt.subplots(1,2, figsize=(12,8), sharey=True, gridspec_kw={'width_ratios':[1,11]})

        #retention matrix
        sns.heatmap(retention_matrix,
                    mask=retention_matrix.isnull(),
                    annot=True,
                    fmt='.0%',
                    cmap='RdYlGn',
                    ax=ax[1])
        ax[1].set_title('Yearly Cohorts: User Retention', fontsize=16)
        ax[1].set(xlabel='# of periods', ylabel='')

        #cohort size
        cohort_size_df = pd.DataFrame(cohort_size).rename(columns={0: 'cohort_size'})
        white_cmap = mcolors.ListedColormap(['White'])
        sns.heatmap(cohort_size_df,
                    annot=True,
                    cbar=False,
                    fmt='g',
                    cmap=white_cmap,
                    ax=ax[0])
        fig.tight_layout()
        plt.show()
        plt.savefig('../images/cohort_retention.png')