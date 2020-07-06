#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 21:18:48 2020

@author: paulina_cieslinska
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import scipy.stats as st
from pandas import Series, DataFrame
from pandas.core.groupby import GroupBy
from scipy.stats import ttest_ind
from scipy.stats import norm
import os.path


class Dataset:

    def file_exists(self, filename):
        return os.path.isfile(filename)

    # Dataframe load
    def dataset(self):
        filename = "portal-offers-05.06.2020.csv"
        if self.file_exists(filename):
            df = self.load_df(filename)
        else:
            if not os.path.exists("data"):
                os.makedirs("data")
            self.download_df()
            df = self.load_df(filename)
        return df
    
    def load_df(self, filename):
        df = pd.read_csv(filename)
        return df
    
class data_cleaning:
    
    
    def rm_out(self,df,columns=None):
        if columns:
            columns = columns
        else:
            columns = df.columns
            
        df_out = df.copy()
        for c in columns:
            q1 = df[c].quantile(0.25)
            q3 = df[c].quantile(0.75)
            IRQ = q3 - q1
            df_out = df_out.loc[ (df[c] <= q3 + 1.5 * IRQ) & (df[c] >= q1 - 1.5 * IRQ) ]
            
        df_out.index = range(len(df_out))
        return df_out
    
class data_rambling:
    
    def city_size(self,df,column):
        city_size=[]

        for num in df[column]:
            if num >=500000:
                city_size.append('najwieksze_miasta')
            elif num <500000 and num >=250000:
                city_size.append('wieksze_miasta')
            elif num <250000 and num >=100000:
                city_size.append('duze_miasta')
            elif num <100000 and num >=50000:
                city_size.append('srednie_miasta')
            elif num <50000 and num >=25000:
                city_size.append('wieksze_miasta')
            else:
                city_size.append('pozostale')
        
        df['city_size']=city_size
        return df

##################################################################
        
 ################################################################3
 from sklearn.metrics import r2_score
 from statsmodels.formula.api import ols
 import statsmodels.api as sm
 
class Model_ols:
    
    def ols_model(self,df,x,y):
       list_of_responses = list(X.columns)
    
        # list of models
        models = []
        formula='price ~'
        for i, resp in enumerate(list_of_responses):
            if i==0:
                formula += resp 
            else:
                formula+=' + '+resp
            models.append(sm.OLS.from_formula(formula, data).fit())
        return models
        
    def all_stat_ols(self,models):
        for i in range(0,len(models)):
            print(models[i].summary())
            
    def best_model_ols(self,models):
        best = 0
        best_model = {}
        for i in range(0,len(models)):
            r2 = models[i].rsquared
            if r2 > best:
                best = r2
                best_model[i] =r2
                best_model2=f"score: {r2} dla {i}"
                print(best_model2)
            return best_model
       
        def best_params_ols(self,best_model,list_of_responses):
            
            best_number=max(best_model.items(), key=operator.itemgetter(1))[0]
            
            features = []
    
            for i, fea in enumerate(list_of_responses):
                if i<best_number:
                    features.append(fea)
                    #features += fea 
                else:
                    break
            return features
        
        data_feature=pd.DataFrame(data[features])


#####################################
#rest models
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor

from sklearn.metrics import roc_auc_score
import sklearn
import matplotlib.pyplot as plt
import math
import xgboost

from sklearn.model_selection import cross_validate

from sklearn.model_selection import train_test_split
from sklearn import datasets

class rest_models:
    
    Models = {
        "decision_tree": DecisionTreeRegressor(),
        "random_forest": RandomForestRegressor(),
        "xgboost": XGBRegressor(objective="reg:squarederror"),
        "svm": SVR(),
        "knn": KNeighborsRegressor()
    }
    
    model_parameters = {
    "decision_tree": {'max_depth': [3, 4, 5]},
    "random_forest": {'n_estimators': [10, 30, 50]},
    "xgboost": {'n_estimators': [10, 30, 50]},
    "svm": {"C": [0.1, 0.01, 0.03]},
    "knn": {"n_neighbors": [3, 5, 7]}
}
    
    train_x, test_x, train_y, test_y = train_test_split(X,Y)
    
    def best_model(self,models, parameters):
       best_models = {}
    
        for key in Models:
            print(f"Training {key}")
            clf = GridSearchCV(
                models[key],
                parameters[key]
            )
            result = clf.fit(train_x, train_y)
            best_models[key] = result.best_estimator_     
            test_models(best_models, test_x, test_y)
         
        return best_models
    
    def roc_curve(self,best_model_list)
        auc_scores = {}

        for k, model in best_models.items():
            try:
                preds = model.predict_proba(test_x)
                auc_scores[k] = roc_auc_score(test_y, preds[:, 1])
            except:
                auc_scores[k] = None
                
        return auc_scores

