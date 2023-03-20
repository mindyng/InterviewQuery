#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

python are_we_going_to_survive.py original_purchase_order.csv next_purchase_order.csv customer_features.csv product_features.csv last_month_assortment.csv next_month_assortment.csv

Q1. What is the current amount this month of money revenue - expenses?
Q2. How many books are being ordered next month?
Q3. How many books are being sold
Q4. Can we make a profit?
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
import xgboost

import sys
import ast
import os


def main():
    arguments = sys.argv
    if len(arguments) < 7:
        raise
    #reading all files into dataframes
    opo, npo, cf, pf, lma, nma = pd.read_csv(arguments[1]), pd.read_csv(arguments[2]),pd.read_csv(arguments[3]),pd.read_csv(arguments[4]),pd.read_csv(arguments[5]), pd.read_csv(arguments[6])
    """
    testing:
    opo = pd.read_csv('original_purchase_order.csv')
    npo = pd.read_csv('next_purchase_order.csv')
    cf = pd.read_csv('customer_features.csv')
    pf = pd.read_csv('product_features.csv')
    lma = pd.read_csv('last_month_assortment.csv')
    nma = pd.read_csv('next_month_assortment.csv')
    """
    
    #Q1.
    #data munging
    opo = opo.set_index('product_id')
    opo['total_purchase_cost'] = opo['quantity_purchased'] * opo['cost_to_buy']
    original_sold = opo.join(lma.set_index('product_id'))
    #getting cost values
    current_loan = opo['total_purchase_cost'].sum()
    current_sold_df = original_sold[original_sold['purchased'] == True]
    current_sold = current_sold_df['retail_value'].sum()
    current_shipping_cost = 0.6*len(current_sold_df) + 0.6*2*(len(lma) - len(current_sold_df))
    #get the current month revenue - expenses
    current_month_profit = current_sold - current_loan - current_shipping_cost
    
    #Q2.
    npo = npo.set_index('product_id')
    npo['total_purchase_cost'] = npo['quantity_purchased'] * npo['cost_to_buy']
    #get expenses for next month order
    next_month_loan = npo['total_purchase_cost'].sum()
    
    #Q3.
    #train model
    model, pf_df, cf_df = train_model(lma, cf, pf, opo)
    #append the original purchase order to the new one assuming that the assortment doesn't
    #send books it does not have
    nto = opo.append(npo)
    x, test = get_test_dataset(nma, cf_df, pf_df, nto) #get next month dataset
    test['prediction'] = model.predict(x) #predict values for next month dataset
    pred_sold = test[test['prediction'] == True]

    #Q4.
    next_month_revenue = pred_sold.retail_value.sum()
    next_month_shipping = 0.6*len(pred_sold) + 0.6*2*(len(test) - len(pred_sold))
    expenses = abs(current_month_profit - next_month_loan - next_month_shipping)
    profit = next_month_revenue - expenses
    if profit > 0:
        print 'Yes'
    else:
        print 'No'

def munge(cf, pf):
    """
    dummify the datasets
    """
    mlb = MultiLabelBinarizer()
    cf['favorite_genres'] = cf['favorite_genres'].apply(lambda x: ast.literal_eval(x))
    cf_df = cf.join(pd.DataFrame(mlb.fit_transform(cf['favorite_genres']),
                          columns=mlb.classes_,
                          index=cf.index))
    cf_df = cf_df.join(pd.DataFrame(pd.get_dummies(cf['age_bucket'])))
    pf_df = pf.join(pd.DataFrame(pd.get_dummies(pf['genre'])))
    cf_df = cf_df.set_index('customer_id')
    pf_df = pf_df.set_index('product_id')
    return pf_df, cf_df

def join_monthly_assortment(ma, pf_retail, cf_df):
    """
    join to the assortment
    """
    cust = ma.set_index('customer_id').join(cf_df)
    cust = cust.reset_index()
    train = cust.set_index('product_id').join(pf_retail, lsuffix='_product')
    return train

def train_model(lma, cf, pf, opo):
    """
    dummify the customer and product features
    join them to the current month order to create training set
    train the model and return the model and dummified datasets
    """
    pf_df, cf_df = munge(cf, pf)
    pf_retail = pf_df.join(opo['retail_value'])
    train = join_monthly_assortment(lma, pf_retail, cf_df)
    
    x = train.drop(['age_bucket', 'favorite_genres', 'genre', 'customer_id', 'purchased'],axis=1)
    y = train['purchased'].values
    model = xgboost.XGBClassifier()
    
    split = np.random.rand(len(x)) < .9 #train on less than 90 percent of dataset
    train_x = x[split]
    train_y = y[split]
    test_x = x[~split]
    test_y = y[~split]
    model.fit(train_x, train_y)
    
    
    test_x['predict_purchase'] = model.predict(test_x)
    print pd.crosstab(test_x['predict_purchase'], test_y)
    """
    given a test dataset with cross validation, the number of correct values is greater
    than the number of True or False numbers determining its better than just guessing all True or False
    """
    model = xgboost.XGBClassifier()
    model.fit(x, y)
    
    return model, pf_df, cf_df
    
def get_test_dataset(nma, cf_df, pf_df, nto):
    """
    get dataset for next month
    """
    pf_retail = pf_df.join(nto['retail_value'])
    test = join_monthly_assortment(nma, pf_retail, cf_df)
    x = test.drop(['age_bucket', 'favorite_genres', 'genre', 'customer_id'],axis=1)
    return x, test
    
    
    
if __name__ == '__main__':
	main()   
