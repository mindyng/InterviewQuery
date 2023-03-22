#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

- Plots of availability across the different cities as time gets closer to date

Assumptions:
    - Data with the scraped_date > date is excluded

"""

import pandas as pd
import os
import seaborn as sns

data = pd.read_csv("scraped_data.csv")

# data cleaning and date processing
data['scraped_date'] = pd.to_datetime(data['scraped_date'])
data['date'] = pd.to_datetime(data['date'])
data['days_til_date'] = data['date'].subtract(data['scraped_date'])
data['days_til_date'] = data['days_til_date'].apply(lambda x: x.days)
data = data[data['days_til_date'] >= 0]

# let's look at data by availability and price
dtd = pd.DataFrame(data.groupby('days_til_date').agg(['mean', 'count'])[['available', 'price']]).reset_index()

ad = data[data['days_til_date'] > 60]
ad = pd.DataFrame(ad.groupby('scraping_id').agg(['sum', 'count'])['available']).reset_index()

ad_low = data[data['days_til_date'] < 10]
ad_low = pd.DataFrame(ad_low.groupby('scraping_id').agg(['sum', 'count'])['available']).reset_index()


# Now let's estimate and calculate revenue

ss = data.groupby('scraping_id').agg(['sum'])['available']
ss = pd.DataFrame(ss).reset_index()
black_out_ids = list(ss[ss['scraping_id'] == 0]['scraping_id'])

dd = data[~data['scraping_id'].isin(black_out_ids)]
dd = dd.groupby(['scraping_id', 'date']).agg(['mean', 'max'])[['available', 'price', 'days_til_date']]
dd = pd.DataFrame(dd).reset_index()
dd['changed'] = dd['available']['mean'].apply(lambda x: 1 if x > 0 and x < 1 else 0)
max_dd = dd[dd['available']['max'] == 1]
ch = max_dd.groupby('scraping_id').agg('mean')['changed']


nb = dd[(dd['available']['mean'] > 0) & (dd['available']['mean'] < 1)]
nb.columns = ['scraping_id', 'date', 'available_mean', 'available_max', 'price_mean',
               'price_max', 'days_til_date_mean', 'days_til_date_max', 'changed']
nb['revenue'] = nb['price_mean']
nb = nb[nb['price_mean'] < 5000]

b = dd[dd['available']['mean'] == 0]
est = b.set_index('scraping_id').join(ch.set_index('scraping_id'))
est.columns = ['date', 'available_mean', 'available_max', 'price_mean',
               'price_max', 'days_til_date_mean', 'days_til_date_max', 'changed', 'changed_percentage']
               
est['days_variable'] = est['days_til_date_max'].apply(lambda x: 15 if x < 15 else x)
est['days_x'] = est['days_variable'].apply(lambda x: (77-x)/62.0)
est['scale'] = est['days_x'] * est['changed_percentage']
est['revenue'] = est['scale'] * est['price_mean']
est = est[est['revenue'] < 5000]

est = est.reset_index()
est_month = est.groupby([est['scraping_id'], pd.Grouper(key='date', freq='M')]).agg(['sum', 'count'])['revenue']
nb_month = nb.groupby([nb['scraping_id'], pd.Grouper(key='date', freq='M')]).agg(['sum', 'count'])['revenue']

total_month = nb_month.append(est_month)
total_month = total_month.reset_index()
result = total_month.groupby(['date']).agg('sum')['sum']
tm = pd.DataFrame(total_month.groupby('scraping_id').agg('sum')['sum'])

listings = pd.read_csv("scraped_data/scraped_listings.csv")
tm = tm.join(listings.set_index('scraping_id'))
tm['bedrooms'] = pd.to_numeric(tm['bedrooms'])
tm['capacity'] = pd.to_numeric(tm['capacity'])
tm['bathrooms'] = pd.to_numeric(tm['bathrooms'])
tm['has_pool'] = pd.to_numeric(tm['has_pool'])
plot = tm.dropna()
beds_df = pd.DataFrame(tm.groupby(['bedrooms']).agg(['sum', 'count'])['sum'])
beds_df['revenue_per'] = beds_df['sum']/beds_df['count']
