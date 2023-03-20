# -*- coding: utf-8 -*-
"""

"""

import pandas as pd
import nltk
from nltk.collocations import *
from nltk.stem.snowball import SnowballStemmer
import re
from collections import Counter
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import numpy as np

""" HELPER FUNCTIONS """
def lambda_num_license(x):
    """ Takes in a string and returns the number of licenses in string """
    if isinstance(x, basestring):
        return len(str(x).split(','))
    else:
        return 0
        
def lambda_businessname(x, business_list):
    """ Set the top N number of businessnames as factors """
    if isinstance(x, basestring):
        if x in business_list:
            return x
        else:
            return 'OTHER'
    else:
        return "NONE"

def tokenize_and_stem(text, stopwords, stemmer):
    """ Tokenize and stem the text and return a list of individual words """
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent) if word not in stopwords]
    filtered_tokens = []
    # filter out any tokens not containing letters 
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return [stemmer.stem(t) for t in filtered_tokens]

def lambda_num_keys(x, key_list):
    """ Return number of keywords in description """
    try:
        if isinstance(x, basestring):
            return len([z for word in x.split() for z in key_list if z in word.lower()])
        else:
            return 0
    except: #For non unicode 8 formatted text
        return 0

def summary(outcome, pred):
    """ Summary statistics for classification """
    incorrect = (outcome != pred).sum()
    print 'Number of misclassified: ' + str(incorrect)
    print 'Number of samples: ' + str(len(outcome))
    print 'Percent Classfied Correctly: ' + str(float((len(outcome)-incorrect))/len(outcome))
    
def count_words(data, binary):
    """ Takes in a dataframe and a binary value and returns a Counter object
        with the highest frequencies of tokenized words for non-electric and electric datasets
    """   
    stopwords = nltk.corpus.stopwords.words('english')
    stemmer = SnowballStemmer("english")
    electric = data[(data['y'] == binary)]
    electric = electric.dropna(subset=['description'])
    tokens = []
    for index, row in electric.iterrows():
        try:
            tokens.extend(tokenize_and_stem(row['description'], stopwords, stemmer))
        except:
            #print index
            pass
    return Counter(tokens)

def get_business_list(data, top_business):
    """ Get list of businessnames and remove non-unicode """
    business = list(data['businessname'].value_counts()[0:top_business].index)
    return business
    

def get_key_words(diff, threshold):
    """ Get keywords that pass the threshold of making a difference inbetween
        two datasets of data of being electrical and one being non-electrical
    """
    key_list = []
    for word in diff:
        if np.abs(float(word[2])/word[1]) < threshold:
            key_list.append(word[0])
    return key_list

def read_data(train_file, test_file):  
    """READ IN TEST AND TRAINING DATA"""
    data = pd.read_table(train_file)
    test = pd.read_table(test_file)
    return data, test

"""PREPROCESSING"""

def set_y_value(data):
    """ Set Y Value "Electric" to binary 1 or 0 """
    data['y'] = data['type'].apply(lambda x: 1 if isinstance(x, basestring) and x == "ELECTRICAL" else 0)
    return data
    
def train_key_words(data, top_words):
    """ NLTK analysis for frequent words. This methods returns a list of words that
        helps partition the dataset into what commonly occuring words happen in "electrical"
        remodels and what commonly occuring words happen in non-electrical remodels
    """
    electric = count_words(data, 1) #get most frequent words for electrical descriptions
    non_electric = count_words(data, 0) #get most frequent words for non-electrical descriptions
    
    #Normalize the frequency between the two datasets
    len_electric = len(data[data['y']==1])
    len_non = len(data[data['y']==0])
    normalize = float(len_electric)/len_non
    norm_non_electric = [(x[0],normalize*x[1]) for x in non_electric.most_common(10000)]
    norm_electric = electric.most_common(10000)
    
    #Get a list of tuples with word, difference in occurence, and total occurence in electrical dataset
    diff = []
    for tup in norm_electric:
        for non in norm_non_electric:
            if tup[0] == non[0]:
                diff.append((tup[0], tup[1]-non[1], tup[1])) #word name, difference in occurrence, total occurence
                break      
            
    # Pick key words with low difference between total occurence and difference in occurrence
    #EX. wire, 4757 diffference in occurence, 4813 occurences in electric dataset  
    ekeys_most_common = sorted(diff, key=lambda tup: tup[1], reverse=True)[0:top_words] 
    nkeys_most_common = sorted(diff, key=lambda tup: tup[1])[0:top_words]
    ekeys_contains = get_key_words(ekeys_most_common, 1.05) #Get the most distinct "electrical" keywords
    nkeys_contains = get_key_words(nkeys_most_common, 0.05) #Get the most non-electrical keywords
    return ekeys_contains, nkeys_contains
    
def preprocessing(data, business_list, ekeys_contains, nkeys_contains):
    """ Preprocessing for one line apply methods """
    data['num_license'] = data['licensetype'].apply(lambda_num_license) #get number of licenses
    data['has_electric_license'] = data['licensetype'].apply(lambda x: 1 if isinstance(x, basestring) and "ELECTRIC" in x else 0)
    
    #Set top businessnames 
    data['business_top'] = data['businessname'].apply(lambda x: lambda_businessname(x, business_list)) #Set top N businessnames as factors
    data['electric_in_name'] = data['businessname'].apply(lambda x: 1 if isinstance(x, basestring) and "ELECTRIC" in x else 0)
    
    #Legaldescription
    data['has_ld'] = data['legaldescription'].apply(lambda x: 1 if isinstance(x, basestring) else 0)
    
    #get number of keys in description  
    data['num_electric_keys'] = data['description'].apply(lambda x: lambda_num_keys(x, ekeys_contains))
    data['num_non_keys'] = data['description'].apply(lambda x: lambda_num_keys(x, nkeys_contains))
    
    #job value
    data['int_job_value'] = data['job_value'].apply(lambda x: float(str(x).replace('$', '').replace(',','')))
    
    return data  

"""MACHINE LEARNING"""

def machine_learning_prep(data):
    """ Dummify the x variables for machine learning processing """
    x_factor = ['business_top', 'subtype']
    x = data[['num_license', 'has_electric_license', 'business_top', 'has_ld', 'subtype',
              'num_electric_keys', 'num_non_keys', 'electric_in_name']]
    x = x.fillna('NONE')
    x_lin = pd.concat([pd.get_dummies(x[col]) for col in x[x_factor]], axis=1, keys=x_factor)
    x = x.drop(x_factor, 1)
    x[x_lin.columns] = x_lin
    return x
    
def train_model(x, y):
    """ Takes in features and y values and returns a model """
    rf = RandomForestClassifier()
    rf_fit = rf.fit(x, y)
    return rf_fit
    
def cross_validate(x, y):
    """ K FOLD cross validation partitioning and checking """
    rf = RandomForestClassifier()
    num_folds = 5
    subset_size = len(x)/num_folds #divide length into subsets
    for i in xrange(0, num_folds):
        #Divide data into test and train
        test_x = x[i*subset_size:][:subset_size]
        train_x = pd.concat([x[:i*subset_size], x[(i+1)*subset_size:]], axis=0)
        test_y = y[i*subset_size:][:subset_size]
        train_y = list(y[:i*subset_size]) + list(y[(i+1)*subset_size:])
        #Fit the model
        rf_fit = rf.fit(train_x, train_y)
        y_pred = rf_fit.predict(test_x)
        summary(test_y, y_pred) #classification cross validating statistics


def train_classifier(data):
    """ Takes in a training dataset and returns a model and lists of keywords""" 
    data = set_y_value(data) #set the y value to 1 or 0
    business_list = get_business_list(data, 100) #list of top N business names as factors
    #list of keywords in the description that help partition data into either electrical or not
    ekeys_contains, nkeys_contains = train_key_words(data, 100) 
    data = preprocessing(data, business_list, ekeys_contains, nkeys_contains) #more data munging and apply all new columns
    #Train model
    y = data['y'].values 
    x = machine_learning_prep(data)
    model = train_model(x, y)
    cross_validate(x, y) #cross validate model
    return model, business_list, ekeys_contains, nkeys_contains
    
    

def main():
    """ MAIN PROGRAM """
    train_file = './data/train_data.csv'
    test_file = './data/xtest_data.csv'
    data, test_data = read_data(train_file, test_file) #read in the data
    model, business_list, ekeys_contains, nkeys_contains = train_classifier(data) #train the classifier
    
    test_data = preprocessing(test_data, business_list, ekeys_contains, nkeys_contains) #preprocess the test data
    x = machine_learning_prep(test_data) #preprocess the test data for machine learning
    y_pred = model.predict(x) #predict the new values
    pd.DataFrame(y_pred).to_csv('./data/ytest_pred.csv', index=False, header=False)

if __name__ == '__main__':
    main()
        
        
        
"""
ekeys_contains = ['electric', 'amp', 'wire', 'wiring', 'volt', 'light',
                 'circuit', 'transform', 'outlet', 'power', 'alarm', 
                 'system', 'panel', 'system', 'secur', 'joint', 'receptacl',
                 'cabl', 'control', 'rewir', 'feeder', 'fixtur', 'meter', 'branch']
ekeys_exact = ['ac', 'dc']
nkeys_contains = ['plan', 'construct', 'famili', 'singl', 'resid', 'alter', 
                  'field', 'subject', 'stfi', 'establish', 'interior', 'structur',
                  'dwell', 'sewer', 'occupi', 'attach', 'parcel', 'demolish', 'land',
                  'deck', 'accessori', 'applic', 'ductwork', 'grade', 'portion', 'non-structur']

ANALYSIS
base = pd.crosstab(data['has_electric_license'], data['y'])
ld = pd.crosstab(data['has_ld'], data['y'])
print "Base Percentage Classification " + str(float((base[0][0] + base[1][1]))/len(data))
pd.crosstab(data['y'], data['num_electric_keys'])
"""