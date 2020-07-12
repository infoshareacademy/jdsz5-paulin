#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 21:18:48 2020

@author: paulina_cieslinska
"""

import operator
import os.path
import pickle
import random

import joblib
import numpy as np
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from matplotlib import rcParams
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import make_scorer, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, cross_validate, cross_val_predict
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors._ball_tree import BallTree
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.svm import SVR, SVC
from sklearn.tree import DecisionTreeRegressor
from sklearn_pandas import GridSearchCV
from termcolor import colored
from tqdm import tqdm
from xgboost import XGBRegressor
import xgboost as xgb

colors = ["grey",
          "red",
          "green",
          "yellow",
          "blue",
          "magenta",
          "cyan",
          "white"]

model_names = [
    DecisionTreeRegressor().__class__.__name__,
    XGBRegressor().__class__.__name__,
    KNeighborsRegressor().__class__.__name__,
    SVR().__class__.__name__,
    RandomForestRegressor().__class__.__name__,
]


class Dataset:

    def file_exists(self, filename):
        return os.path.isfile(filename)

    # Dataframe load
    def df_set(self, preprocess=False):
        df = None
        filename = "data/final_estates.csv"
        if self.file_exists(filename):
            df = self.load_df(filename)
            if preprocess:
                df = self._preprocess(df)
        return df

    def _preprocess(self, df):
        features = Features()
        df = features.prepare_df(None, df)
        df = features.test_features(df)
        return df

    def load_df(self, filename):
        df = pd.read_csv(filename, low_memory=False)
        return df


class Data_cleaning:

    def rm_out(self, df, columns=None):
        if columns:
            columns = columns
        else:
            columns = df.columns

        df_out = df.copy()
        for c in columns:
            q1 = df[c].quantile(0.25)
            q3 = df[c].quantile(0.75)
            IRQ = q3 - q1
            df_out = df_out.loc[(df[c] <= q3 + 1.5 * IRQ) & (df[c] >= q1 - 1.5 * IRQ)]

        df_out.index = range(len(df_out))
        return df_out

    @staticmethod
    def normalize(x, y, as_df=False):
        scale1 = MinMaxScaler().fit(x)
        x_norm = scale1.transform(x)
        scale2 = MinMaxScaler().fit(y)
        y_norm = scale2.transform(y)
        train_x, test_x, train_y, test_y = train_test_split(x_norm, y_norm, test_size=0.2)
        if as_df:
            pd_x_norm = pd.DataFrame(data=x_norm, columns=x.columns)
            pd_y_norm = pd.DataFrame(data=y_norm, columns=y.columns)
            pd_train_x = pd.DataFrame(data=train_x, columns=x.columns)
            pd_train_y = pd.DataFrame(data=train_y, columns=y.columns)
            pd_test_x = pd.DataFrame(data=test_x, columns=x.columns)
            pd_test_y = pd.DataFrame(data=test_y, columns=y.columns)
            return pd_train_x, pd_train_y, pd_test_x, pd_test_y, pd_x_norm, pd_y_norm
        else:
            return train_x, test_x, train_y, test_y, x_norm, y_norm


class Data_rambling:

    def city_size(self, df, column):
        city_size = []

        for num in df[column]:
            if num >= 500000:
                city_size.append('najwieksze_miasta')
            elif 500000 > num >= 250000:
                city_size.append('wieksze_miasta')
            elif 250000 > num >= 100000:
                city_size.append('duze_miasta')
            elif 100000 > num >= 50000:
                city_size.append('srednie_miasta')
            elif 50000 > num >= 25000:
                city_size.append('wieksze_miasta')
            else:
                city_size.append('pozostale')

        df['city_size'] = city_size
        return df


##################################################################
class General_data():

    def box_plot(self, df, y='apartment_room_number', x='pop_province'):
        fig, ax = plt.subplots(figsize=(20, 8))
        bplot = sns.boxplot(y=y, x=x,
                            data=df,
                            width=0.5,
                            palette="colorblind",
                            orient='v',
                            linewidth=0.5)
        plt.xticks(rotation=90, size=10)
        plt.title('Rozkład kolumny: liczba {} z podziałem na {}'.format(y, x))
        plt.show(block=False)

    def single_box_plot(self, df, x='apartment_room_number', ):
        fig, ax = plt.subplots(figsize=(20, 8))
        bplot = sns.boxplot(x=x,
                            data=df,
                            width=0.5,
                            palette="colorblind",
                            orient='v',
                            linewidth=0.5)
        plt.xticks(rotation=90, size=10)
        plt.title('Rozkład kolumny: liczba {}'.format(x))
        plt.show(block=False)

    def hists(self, df, x='apartment_room_number'):
        fig, ax = plt.subplots(figsize=(20, 8))
        n, bins, patches = plt.hist(df[x], 5, density=True, facecolor='g', alpha=0.75)
        plt.grid(True)
        plt.show()

    def feature_importants(self, df):
        import warnings
        warnings.filterwarnings("ignore")
        features = Features()
        df = features.prepare_df(None, df, True)
        y = df[['price']]
        x = df.drop(['price'], axis=1)
        # X_train, X_test, Y_train, Y_test = Data_cleaning.normalize(x, y)
        X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2)
        xg_reg = xgb.XGBRegressor()
        xg_reg.fit(X_train, Y_train)
        rcParams["figure.figsize"] = 10, 8
        xgb.plot_importance(xg_reg)
        plt.show(block=False)


################################################################3


class Model_ols:

    def __init__(self, df):
        y = df[['price']]
        x = df.drop(['price'], axis=1)
        # train_x, test_x, train_y, test_y, x_norm, y_norm = Data_cleaning.normalize(x, y, True)
        train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2)
        x_norm = x
        y_norm = y
        model = self.ols_model(df, x_norm, y_norm)
        self.model = model
        self.all_stat_ols(model)
        best_model = self.best_model_ols(model)
        self.best_model = best_model
        self.features = self.best_params_ols(best_model, list(x_norm.columns))

    def ols_model(self, df, x, y):
        list_of_responses = list(x.columns)
        # list of models
        models = []
        formula = f"{y.columns[0]} ~"
        for i, resp in enumerate(list_of_responses):
            if i == 0:
                formula += resp
            else:
                formula += ' + ' + resp
            models.append(sm.OLS.from_formula(formula, df).fit())
        print(f"features: {models}")
        return models

    def all_stat_ols(self, models):
        for i in range(0, len(models)):
            print(models[i].summary())

    def best_model_ols(self, models):
        best = 0
        best_model = {}
        for i in range(0, len(models)):
            r2 = models[i].rsquared
            if r2 > best:
                best = r2
                best_model[i] = r2
                best_model2 = f"score: {r2} dla {i}"
                print(colored(best_model2, random.choice(colors)))
        return best_model

    def best_params_ols(self, best_model, list_of_responses):
        best_number = max(best_model.items(), key=operator.itemgetter(1))[0]
        features = []
        for i, fea in enumerate(list_of_responses):
            if i < best_number:
                features.append(fea)
                # features += fea
            else:
                break
        return features

        # data_feature = pd.DataFrame(data[features])


#####################################
# rest models

class rest_models():
    res = None
    test_score = None
    scorer = None
    y_pred = None

    def __init__(self, df, file, start_model=True, add_to_name=None):
        try:
            self.add_to_name = add_to_name
            self.file_name = file.replace(".csv", "")
            self.f = open(f'output/{file}_results.txt', 'a')
            y = df[['price']]
            x = df.drop(['price'], axis=1)
            # self.train_x, self.train_y, self.test_x, self.test_y, self.x_norm, self.y_norm = Data_cleaning.normalize(x, y, True)
            self.train_x, self.test_x, self.train_y, self.test_y = train_test_split(x, y, test_size=0.2)
            self.x_norm = x
            self.y_norm = y
            xg_boost_params = {
                'n_estimators': [400, 700, 1000],
                'max_depth': [15, 20, 25]
            }
            self.Models = {
                "decision_tree": DecisionTreeRegressor(),
                "random_forest": RandomForestRegressor(),
                # "xgboost_logistic_gblinear": XGBRegressor(objective="reg:logistic", booster="gblinear"),
                "xgboost_squarederror_gblinear": XGBRegressor(objective="reg:squarederror", booster="gblinear"),
                # "xgboost_logistic_gbtree": XGBRegressor(objective="reg:logistic", booster="gbtree"),
                "xgboost_squarederror_gbtree": XGBRegressor(objective="reg:squarederror", booster="gbtree"),
                "svm": SVR(),
                "knn": KNeighborsRegressor()
            }
            self.model_parameters = {
                "decision_tree": {'max_depth': [3, 4, 5]},
                "random_forest": {'n_estimators': [10, 30, 50]},
                # "xgboost_logistic_gblinear": xg_boost_params,
                "xgboost_squarederror_gblinear": xg_boost_params,
                # "xgboost_logistic_gbtree": xg_boost_params,
                "xgboost_squarederror_gbtree": xg_boost_params,
                "svm": {
                    "C": [.001, .01, .1, 1, 10, 100],
                    "gamma": ['scale', 'auto'],
                    "kernel": ['linear', 'poly', 'rbf']
                },
                "knn": {"n_neighbors": [3, 5, 7]}
            }
            # self.test_models(self.Models, self.test_x, self.test_y)
            if start_model:
                self.best_models_dict = self.best_models(self.Models, self.model_parameters)
                print(self.best_models_dict)
                self.f.write(str(self.best_models_dict))
                # self.res = self.results(m, self.model_parameters)
                # self.f.write(str(self.test_score))
                # self.f.write(str(self.y_pred))
                # self.f.write(str(self.scorer))
                self.f.close()
        except:
            pass

    def test_models(self, trained_models, test_x, test_y):
        results = {
            "model_name": [],
            "test_score": []
        }
        try:
            test_score = None
            if trained_models.__class__.__name__ == "XGBRegressor":
                try:
                    test_score = trained_models.score(test_x, test_y)
                except Exception as e:
                    test_score = trained_models.score(test_x.values, test_y.values)
                    print(e)
                else:
                    test_score = trained_models.score(test_x, test_y)
            self.f.write("{0} score = {1}".format(trained_models.__class__.__name__, test_score) + "\n")
            print(
                colored("{0} score = {1}".format(trained_models.__class__.__name__, test_score), random.choice(colors)))
        except Exception as e:
            test_score = None
            print(colored(e, "blue"))
        results["model_name"].append(trained_models.__class__.__name__)
        results["test_score"].append(test_score)
        try:
            self.test_score, self.scorer, self.y_pred = self.cross_val_rest_models(trained_models, self.x_norm,
                                                                                   self.y_norm)
            results["test_score_cv"] = self.test_score
            results["scorer"] = self.scorer
            results["y_pred"] = self.y_pred
        except Exception as e:
            print("cross val err!")
            print(e)
        return results

    def best_models(self, models, parameters):
        best_models = {}
        for key in tqdm(self.Models):
            print(f"Training {key}")
            self.f.write(f"Training {key}" + "\n")
            clf = GridSearchCV(
                models[key],
                parameters[key],
                # verbose=5,
                # return_train_score=True,
                n_jobs=-1
            )
            try:
                result = clf.fit(self.train_x, self.train_y)
                print("test_X cols", self.test_x.columns)
                print("train_X cols", self.train_x.columns)
                print("test_Y cols", self.test_y.columns)
                print("train_Y cols", self.train_y.columns)
                tests = self.test_models(clf, self.test_x, self.test_y)
                best_parameters = clf.best_params_
                try:
                    grid_search_score = clf.score(self.test_x, self.test_y)
                    print(colored('score:{} !!'.format(grid_search_score), random.choice(colors)))
                except Exception as e:
                    grid_search_score = None
                    print(colored(e, "red"))
                try:
                    score = self.scores(key, models[key], self.test_x, self.test_y, self.y_norm, tests)
                except Exception as e:
                    score = None
                    print(colored(e, "green"))
                res = {"grid_search": clf, "model": models[key], "best_estimator": result.best_estimator_,
                       "test_models": tests, "score": score, "grid_search_score": grid_search_score,
                       "best_params": best_parameters}
                if self.add_to_name is not None:
                    name = f"models/price_prediction/{models[key].__class__.__name__}_{self.file_name}_price_prediction_{self.add_to_name}"
                else:
                    name = f"models/price_prediction/{models[key].__class__.__name__}_{self.file_name}_price_prediction"
                self.save_model(clf.best_estimator_, name, save_type="joblib")
                best_models[key] = res
            except Exception as e:
                print(e)
        return best_models

    def load_ball(self, df):
        models = self.load_model("classification", select_file_name="final_estates")
        print("loaded")
        recommendation = Recommendation(df, "final_estates.csv", ball=models)
        return recommendation

    def load_model(self, problem_type, load_type="pickle", select_file_name=None, return_type="list"):
        models = []
        models_dict = {}
        if problem_type == "regression":
            files = self.paths("models/price_prediction")
        elif problem_type == "classification":
            files = self.paths("models/recommendation")
        for f in files:
            try:
                path = ""
                if problem_type == "regression":
                    path = "models/price_prediction"
                elif problem_type == "classification":
                    path = "models/recommendation"
                path += f"/{f}"
                if load_type == "pickle":
                    with open(path, "rb") as pf:
                        model = pickle.load(pf)
                elif load_type == "joblib":
                    model = joblib.load(path)
                if select_file_name is None:
                    if return_type == "list":
                        models.append(model)
                    else:
                        models_dict[f] = model
                else:
                    if select_file_name in f:
                        return model
            except Exception as e:
                print("error!!")
                print(e)
        if return_type == "list":
            return models
        else:
            return models_dict

    def save_model(self, model, model_name, save_type="pickle"):
        if save_type == "pickle":
            decision_tree_pkl_filename = f"{model_name}.pkl"
            model_pkl = open(decision_tree_pkl_filename, 'wb')
            pickle.dump(model, model_pkl)
            model_pkl.close()
            print(colored(f"model: {model_name} saved", "magenta"))
        elif save_type == "joblib":
            joblib.dump(model, f"{model_name}.pkl")

    def paths(self, path):
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        return onlyfiles

    def scores(self, key, model, test_x, test_y, y, results):
        Miary_modeli = {
            "decision_tree": metrics.mean_squared_error,  # (test_y, y_)
            "random_forest": model.mse,  # (test_x, test_y)),
            "xgboost": mean_squared_error,  # (y_test_pred, y_test)
            "svm": r2_score,  # (y, y_),
            "knn": r2_score  # (y, y_)
        }

        value = Miary_modeli[key]
        y_ = model.predict(test_x)
        models_results = pd.DataFrame.from_dict(results)
        models_results.to_csv('model_results.csv')
        greatest_model = models_results.sort_values('test_score', ascending=False).head(1)
        score = None
        if key == greatest_model.model_name.values:
            if key == "decision_tree":
                score = value(test_y, y_)
            elif key == "random_forest":
                score = value(test_x, test_y)
            elif key == "xgboost":
                score = value(y_, test_y)
            elif key == "svm":
                score = value(y, y_)
            elif key == "knn":
                score = value(y, y_)
        return score

    def results(self, best_models, best_params):
        results = self.test_models(best_models, self.test_x, self.test_y)
        models_results = pd.DataFrame.from_dict(results)
        # save results whole models
        models_results.to_csv('model_results.csv')
        greatest_model = models_results.sort_values('test_score', ascending=False).head(1)
        best_model = ()
        for key, value in self.Models.items():
            if key == greatest_model.model_name.values:
                best_model = value
        for key, value in self.model_parameters.items():
            if key == greatest_model.model_name.values:
                best_params = value
        model = best_model
        params = best_params
        model_regressor_search = GridSearchCV(model, params, cv=5)
        model_regressor_search.fit(self.train_x, self.train_y)
        score = model_regressor_search.score(self.test_x, self.test_y)
        # mse=model_regressor_search.mse(test_x, test_y)
        best_parameters = model_regressor_search.best_params_
        self.f.write('score:{}'.format(score) + "\n")
        print(colored('score:{}'.format(score), random.choice(colors)))
        try:
            # save model
            model_regressor_search.to_pickle("./best_ml_model.pkl")
            # load model
            load_model = pd.read_pickle("./best_ml_model.pkl")
        except:
            print("")

    def cross_val_rest_models(self, load_model, x_norm, y_norm):
        last_model = load_model
        cv_results = cross_validate(last_model, x_norm, y_norm, cv=10)
        scorer = make_scorer(mean_squared_error)
        y_pred = cross_val_predict(last_model, x_norm, y_norm, cv=10)
        return cv_results['test_score'], scorer, y_pred


class knn_class():

    def best_offerst(self):
        pass


class SVM_model:
    def __init__(self):
        self.parametr_c = [.001, .01, .1, 1, 10, 100]
        self.gamma = ['scale', 'auto']
        self.kernel = ['linear', 'poly', 'rbf']

    def svm(self, df, X_train, X_test, y_train, y_test):
        best = 0
        best_model = ''
        for k in self.kernel:
            for d in range(2, 6):
                for g in self.gamma:
                    for c in self.parametr_c:
                        if k == 'linear':
                            model = SVC(kernel='linear', C=c)
                            model.fit(X_train, y_train)
                            score = model.score(X_test, y_test)
                        elif k == 'poly':
                            model = SVC(kernel='poly', C=c, degree=d)
                            model.fit(X_train, y_train)
                            score = model.score(X_test, y_test)
                        else:
                            model = SVC(kernel='rbf', C=c, gamma=g)
                            model.fit(X_train, y_train)
                            score = model.score(X_test, y_test)
                        if score > best:
                            best = score
                            best_model = f'score = {score} kernel = {k}  c = {c} degree = {d}  gamma = {g}'

        return best_model


class Features:

    def uniques(self, df, col):
        if col in df.columns:
            uniq = df[col].unique()
            print(colored(uniq, "blue"))
            return uniq

    def fix_province(self, df, column):
        provinces = [
            "wielkopolskie", "wielko polskie",
            "śląskie", "slaskie", "ślaskie", "sląskie",
            "mazowieckie",
            "malopolskie", "małopolskie", "mało polskie", "malo polskie",
            "pomorskie",
            'kujawsko-pomorskie', 'kujawsko pomorskie', 'kujawskopomorskie',
            "podkarpackie",
            "lódzkie", "lodzkie", "łódzkie",
            "zachodniopomorskie", "zachodnio pomorskie", "zachodnio-pomorskie",
            "dolnośląskie", "dolnoslaskie", "dolnosląskie", "dolnoślaskie",
            "lubelskie",
            "podlaskie",
            "lubuskie",
            "opolskie",
            "warminsko-mazurskie", "warminskomazurskie", "warminsko mazurskie",
            "swietokrzyskie", "świetokrzyskie", "świętokrzyskie", "swiętokrzyskie",
        ]
        for province in provinces:
            key = np.NaN
            if province in ["wielkopolskie", "wielko polskie"]:
                key = "wielkopolskie"
            if province in ["śląskie", "slaskie", "ślaskie", "sląskie"]:
                key = "śląskie"
            if province in ["mazowieckie"]:
                key = "mazowieckie"
            if province in ["malopolskie", "małopolskie", "mało polskie", "malo polskie"]:
                key = "małopolskie"
            if province in ["pomorskie"]:
                key = "pomorskie"
            if province in ['kujawsko-pomorskie', 'kujawsko pomorskie', 'kujawskopomorskie']:
                key = 'kujawsko-pomorskie'
            if province in ["podkarpackie"]:
                key = "podkarpackie"
            if province in ["lódzkie", "lodzkie", "łódzkie"]:
                key = "łódzkie"
            if province in ["zachodniopomorskie", "zachodnio pomorskie", "zachodnio-pomorskie"]:
                key = "zachodniopomorskie"
            if province in ["dolnośląskie", "dolnoslaskie", "dolnosląskie", "dolnoślaskie"]:
                key = "dolnośląskie"
            if province in ["lubelskie"]:
                key = "lubelskie"
            if province in ["podlaskie"]:
                key = "podlaskie"
            if province in ["lubuskie"]:
                key = "lubuskie"
            if province in ["opolskie"]:
                key = "opolskie"
            if province in ["warminsko-mazurskie", "warminskomazurskie", "warminsko mazurskie"]:
                key = "warminsko-mazurskie"
            if province in ["swietokrzyskie", "świetokrzyskie", "świętokrzyskie", "swiętokrzyskie"]:
                key = "świętokrzyskie"
            df.loc[df[column].astype(str).str.contains(province, na=False, case=False), column] = key
        provinces.append(str(np.NaN))
        df.loc[~df[column].astype(str).isin(provinces)] = np.NaN
        return df

    def prepare_df(self, file, m_df=None, pp=False):
        if m_df is None:
            df = pd.read_csv(f"data/{file}", low_memory=False)
        else:
            df = m_df
        if pp:
            drop_cols = [
                "Unnamed: 0",
                "Unnamed: 1",
                "Unnamed: 0.1",
                "Unnamed: 0.1.1",
                "description",
                "fixed_city",
                "city",
                # "fixed_province",
                "province",
                "fixed_street",
                "street",
                "price_permeter",
                "source_update_date",
                "source_add_date",
                "district",
                "fixed_precinct",
                "precinct",
                "fixed_country",
                "fixed_commune",
                "raw_data",
                "fixed_place",
                "fixed_neighbourhood",
                "fixed_district",
                "fixed_postal_code",
                "crm_number",
                # "id",
                "add_date",
                "update_date",
                "update_date",
                "last_scan_date",
                "building_floornumber",
            ]
            for drop in drop_cols:
                if drop in df.columns:
                    df = df.drop([drop], axis=1)
            # df = df.dropna()
            df = self.test_features(df)
            dropped = []
            to_drop = ["fixed_province",
                       "pop_province",
                       "offer_transaction",
                       "offer_transaction_knn",
                       "id",
                       "portal_id",
                       # "fixed_latitude", "fixed_longitude",
                       "private_offer",
                       "private_offer_knn",
                       "main_type_id",
                       "main_type_id_knn",
                       "pop_city",
                       "pop_district",
                       "area_total_knn",
                       "pop_man_knn",
                       "pop_woman_knn",
                       "pop_population_knn",
                       "pop_long_knn",
                       "pop_lat_knn",
                       "fixed_longitude_knn",
                       "fixed_latitude_knn",
                       "building_year_knn",
                       "apartment_room_number_knn",
                       "apartment_floor_knn",
                       "price_knn",
                       "apartment_floor",
                       ]
            for d in to_drop:
                if d in df.columns:
                    dropped.append(d)
            df_train = df.drop(dropped, axis=1)
            df = df_train.dropna()
        return df

    def paths(self, path):
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        return onlyfiles

    def ranges_features(self, df):
        range_features = {
            "longitude": {"less": 14.00, "high": 25.00},
            "latitude": {"less": 48.00, "high": 55.00},
            "fixed_longitude": {"less": 14.00, "high": 25.00},
            "fixed_latitude": {"less": 48.00, "high": 55.00},
            "building_year": {"less": 1800, "high": 2077},
        }
        for col, vals in range_features.items():
            if col in df.columns:
                df.loc[~(df[col] >= vals["less"]) & ~(df[col] <= vals["high"]), col] = np.NaN
        return df

    def set_knns(self, df):
        if "price_knn" in df.columns:
            df["price"] = df["price_knn"]
        if "area_total_knn" in df.columns:
            df["area_total"] = df["area_total_knn"]
        if "apartment_room_number_knn" in df.columns:
            df["apartment_room_number"] = df["apartment_room_number_knn"]
        if "apartment_floor_knn" in df.columns:
            df["apartment_floor"] = df["apartment_floor_knn"]
        if "building_year_knn" in df.columns:
            df["building_year"] = df["building_year_knn"]
        if "building_year_knn" in df.columns:
            df["building_year"] = df["building_year_knn"]
        if "fixed_latitude_knn" in df.columns:
            df["fixed_latitude"] = df["fixed_latitude_knn"]
        if "fixed_longitude_knn" in df.columns:
            df["fixed_longitude"] = df["fixed_longitude_knn"]
        if "pop_lat_knn" in df.columns:
            df["pop_lat"] = df["pop_lat_knn"]
        if "pop_long_knn" in df.columns:
            df["pop_long"] = df["pop_long_knn"]
        if "pop_population_knn" in df.columns:
            df["pop_population"] = df["pop_population_knn"]
        if "pop_woman_knn" in df.columns:
            df["pop_woman"] = df["pop_woman_knn"]
        if "pop_man_knn" in df.columns:
            df["pop_man"] = df["pop_man_knn"]
        return df

    def test_features(self, df):
        df = df.replace(to_replace=[None], value=np.nan)
        df = df.replace('None', np.NaN)
        df = self.set_knns(df)
        features = [
            "area_total",
            "apartment_room_number",
            "fixed_longitude",
            "fixed_latitude",
            "longitude",
            "latitude",
            "building_year",
            "price",
            "apartment_floor",
        ]
        for feature in features:
            if feature in df.columns:
                df[feature] = df[feature].replace(',', '.', regex=True)
                df[feature] = pd.to_numeric(df[feature], errors='coerce')
        if "fixed_province" in df.columns:
            df = self.fix_province(df, "fixed_province")
            labelencoder = LabelEncoder()
            df['fixed_province'] = df['fixed_province'].replace(np.nan, "")
            df["location_province"] = labelencoder.fit_transform(df["fixed_province"])
        if "pop_province" in df.columns:
            df = self.fix_province(df, "pop_province")
            labelencoder = LabelEncoder()
            df['pop_province'] = df['pop_province'].replace(np.nan, "")
            df["location_pop_province"] = labelencoder.fit_transform(df["pop_province"])
        df = self.ranges_features(df)
        return df

    def find_missing_cols(self, df):
        print(colored("missed cols", "magenta"))
        any_nulls = df.columns[df.isnull().any()]
        miss = df.isnull().sum() / len(df)
        miss = miss[miss > 0]
        miss.sort_values(inplace=True)
        print(colored(miss, "magenta"))
        return miss

    def find_numeric_cols(self, df):
        print(colored("numeric cols", "cyan"))
        numerics = df.applymap(np.isreal).sum() / len(df)
        numerics = numerics[numerics > 0]
        numerics.sort_values(inplace=True)
        print(colored(numerics, "cyan"))
        return numerics

    def save_entries(self, m, f):
        for entry in m:
            f.write(str(entry) + "\n")


class Recommendation:

    def __init__(self, df, file_name, ball=None):
        print(f"ball is none: {ball is None}")
        if df is None:
            df = self.__prepare_df(file_name, pp=True)
        df.info()
        self.df = self.prepare_df(df)
        self.file_name = file_name

        if ball is None:
            self.X_train, self.x_test, self.Y_train, self.Y_test = self.prepare_train_test(df)
            self.train_X_norm, self.test_X_norm = self.prepare_scaling(self.X_train, self.x_test)
            self.tree = self.prepare_ball(self.train_X_norm)
            self.dist, self.ind = self.test_ball(self.tree, self.test_X_norm)
            self.test_index = self.prepare_test_index(self.test_X_norm)
            self.results_df = self.results_ball(self.ind, self.df, self.test_index)
            self.summary(self.df, self.results_df, self.x_test, self.test_index)
            if ball is None:
                self.save_model(self.tree, f"models/recommendation/{self.file_name}_recomendation_knn")
        else:
            self.test_X_norm = self.df.to_numpy()
            # scalar = MinMaxScaler().fit(self.df)
            # self.test_X_norm = scalar.transform(self.df)
            print(colored(self.test_X_norm.shape, "cyan"))
            self.tree = ball
            self.dist, self.ind = self.test_ball(self.tree, self.test_X_norm)
            self.results_df = self.results_ball(self.ind, self.df, self.test_index)
            self.summary(self.df, self.results_df, self.x_test, self.test_index)

    def prepare_df(self, df):
        if "main_type_id" in df.columns:
            df = df[(df["main_type_id"] == 2)]
        return df

    def fix_province(self, df, column):
        provinces = [
            "wielkopolskie", "wielko polskie",
            "śląskie", "slaskie", "ślaskie", "sląskie",
            "mazowieckie",
            "malopolskie", "małopolskie", "mało polskie", "malo polskie",
            "pomorskie",
            'kujawsko-pomorskie', 'kujawsko pomorskie', 'kujawskopomorskie',
            "podkarpackie",
            "lódzkie", "lodzkie", "łódzkie",
            "zachodniopomorskie", "zachodnio pomorskie", "zachodnio-pomorskie",
            "dolnośląskie", "dolnoslaskie", "dolnosląskie", "dolnoślaskie",
            "lubelskie",
            "podlaskie",
            "lubuskie",
            "opolskie",
            "warminsko-mazurskie", "warminskomazurskie", "warminsko mazurskie",
            "swietokrzyskie", "świetokrzyskie", "świętokrzyskie", "swiętokrzyskie",
        ]
        for province in provinces:
            key = np.NaN
            if province in ["wielkopolskie", "wielko polskie"]:
                key = "wielkopolskie"
            if province in ["śląskie", "slaskie", "ślaskie", "sląskie"]:
                key = "śląskie"
            if province in ["mazowieckie"]:
                key = "mazowieckie"
            if province in ["malopolskie", "małopolskie", "mało polskie", "malo polskie"]:
                key = "małopolskie"
            if province in ["pomorskie"]:
                key = "pomorskie"
            if province in ['kujawsko-pomorskie', 'kujawsko pomorskie', 'kujawskopomorskie']:
                key = 'kujawsko-pomorskie'
            if province in ["podkarpackie"]:
                key = "podkarpackie"
            if province in ["lódzkie", "lodzkie", "łódzkie"]:
                key = "łódzkie"
            if province in ["zachodniopomorskie", "zachodnio pomorskie", "zachodnio-pomorskie"]:
                key = "zachodniopomorskie"
            if province in ["dolnośląskie", "dolnoslaskie", "dolnosląskie", "dolnoślaskie"]:
                key = "dolnośląskie"
            if province in ["lubelskie"]:
                key = "lubelskie"
            if province in ["podlaskie"]:
                key = "podlaskie"
            if province in ["lubuskie"]:
                key = "lubuskie"
            if province in ["opolskie"]:
                key = "opolskie"
            if province in ["warminsko-mazurskie", "warminskomazurskie", "warminsko mazurskie"]:
                key = "warminsko-mazurskie"
            if province in ["swietokrzyskie", "świetokrzyskie", "świętokrzyskie", "swiętokrzyskie"]:
                key = "świętokrzyskie"
            df.loc[df[column].astype(str).str.contains(province, na=False, case=False), column] = key
        provinces.append(str(np.NaN))
        df.loc[~df[column].astype(str).isin(provinces)] = np.NaN
        return df

    def set_knns(self, df):
        if "price_knn" in df.columns:
            df["price"] = df["price_knn"]
        if "area_total_knn" in df.columns:
            df["area_total"] = df["area_total_knn"]
        if "apartment_room_number_knn" in df.columns:
            df["apartment_room_number"] = df["apartment_room_number_knn"]
        if "apartment_floor_knn" in df.columns:
            df["apartment_floor"] = df["apartment_floor_knn"]
        if "building_year_knn" in df.columns:
            df["building_year"] = df["building_year_knn"]
        if "building_year_knn" in df.columns:
            df["building_year"] = df["building_year_knn"]
        if "fixed_latitude_knn" in df.columns:
            df["fixed_latitude"] = df["fixed_latitude_knn"]
        if "fixed_longitude_knn" in df.columns:
            df["fixed_longitude"] = df["fixed_longitude_knn"]
        if "pop_lat_knn" in df.columns:
            df["pop_lat"] = df["pop_lat_knn"]
        if "pop_long_knn" in df.columns:
            df["pop_long"] = df["pop_long_knn"]
        if "pop_population_knn" in df.columns:
            df["pop_population"] = df["pop_population_knn"]
        if "pop_woman_knn" in df.columns:
            df["pop_woman"] = df["pop_woman_knn"]
        if "pop_man_knn" in df.columns:
            df["pop_man"] = df["pop_man_knn"]
        return df

    def test_features(self, df):
        df = df.replace(to_replace=[None], value=np.nan)
        df = df.replace('None', np.NaN)
        df = self.set_knns(df)
        features = [
            "area_total",
            "apartment_room_number",
            "fixed_longitude",
            "fixed_latitude",
            "longitude",
            "latitude",
            "building_year",
            "price",
            "apartment_floor",
        ]
        for feature in features:
            if feature in df.columns:
                df[feature] = df[feature].replace(',', '.', regex=True)
                df[feature] = pd.to_numeric(df[feature], errors='coerce')
        if "fixed_province" in df.columns:
            df = self.fix_province(df, "fixed_province")
            labelencoder = LabelEncoder()
            df['fixed_province'] = df['fixed_province'].replace(np.nan, "")
            df["location_province"] = labelencoder.fit_transform(df["fixed_province"])
        if "pop_province" in df.columns:
            df = self.fix_province(df, "pop_province")
            labelencoder = LabelEncoder()
            df['pop_province'] = df['pop_province'].replace(np.nan, "")
            df["location_pop_province"] = labelencoder.fit_transform(df["pop_province"])
        df = self.ranges_features(df)
        return df

    def ranges_features(self, df):
        range_features = {
            "longitude": {"less": 14.00, "high": 25.00},
            "latitude": {"less": 48.00, "high": 55.00},
            "fixed_longitude": {"less": 14.00, "high": 25.00},
            "fixed_latitude": {"less": 48.00, "high": 55.00},
            "building_year": {"less": 1800, "high": 2077},
        }
        for col, vals in range_features.items():
            if col in df.columns:
                df.loc[~(df[col] >= vals["less"]) & ~(df[col] <= vals["high"]), col] = np.NaN
        return df

    def __prepare_df(self, file, m_df=None, pp=False):
        if m_df is None:
            df = pd.read_csv(f"data/{file}", low_memory=False)
        else:
            df = m_df
        if pp:
            drop_cols = [
                "Unnamed: 0",
                "Unnamed: 1",
                "Unnamed: 0.1",
                "Unnamed: 0.1.1",
                "description",
                "fixed_city",
                "city",
                # "fixed_province",
                "province",
                "fixed_street",
                "street",
                "price_permeter",
                "source_update_date",
                "source_add_date",
                "district",
                "fixed_precinct",
                "precinct",
                "fixed_country",
                "fixed_commune",
                "raw_data",
                "fixed_place",
                "fixed_neighbourhood",
                "fixed_district",
                "fixed_postal_code",
                "crm_number",
                # "id",
                "add_date",
                "update_date",
                "update_date",
                "last_scan_date",
                "building_floornumber",
            ]
            for drop in drop_cols:
                if drop in df.columns:
                    df = df.drop([drop], axis=1)
            # df = df.dropna()
            df = self.test_features(df)
            dropped = []
            to_drop = ["fixed_province",
                       "pop_province",
                       "offer_transaction",
                       "offer_transaction_knn",
                       "id",
                       "portal_id",
                       # "fixed_latitude", "fixed_longitude",
                       "private_offer",
                       "private_offer_knn",
                       "main_type_id",
                       "main_type_id_knn",
                       "pop_city",
                       "pop_district",
                       "area_total_knn",
                       "pop_man_knn",
                       "pop_woman_knn",
                       "pop_population_knn",
                       "pop_long_knn",
                       "pop_lat_knn",
                       "fixed_longitude_knn",
                       "fixed_latitude_knn",
                       "building_year_knn",
                       "apartment_room_number_knn",
                       "apartment_floor_knn",
                       "price_knn",
                       "apartment_floor",
                       ]
            for d in to_drop:
                if d in df.columns:
                    dropped.append(d)
            df = df.drop(dropped, axis=1)
            df = df.dropna()
        return df

    def prepare_train_test(self, df):
        y = df[['price']]
        x = df.drop(['price'], axis=1)
        X_train, x_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2)
        return X_train, x_test, Y_train, Y_test

    def prepare_scaling(self, X_train, X_test):
        scalar = MinMaxScaler().fit(X_train)
        train_X_norm = scalar.transform(X_train)
        test_X_norm = scalar.transform(X_test)
        return train_X_norm, test_X_norm

    def prepare_ball(self, train_X_norm, leaf_size=100, metric="euclidean"):
        tree = BallTree(train_X_norm, leaf_size=leaf_size, metric=metric)
        return tree

    def prepare_test_index(self, df):
        test_index = random.randrange(0, len(df) - 1)
        return test_index

    def test_ball(self, tree, test_X_norm, k=5):
        print(test_X_norm)
        print(test_X_norm.shape)
        dist, ind = tree.query(test_X_norm, k=k)
        return dist, ind

    def results_ball(self, ind, df, test_index):
        results_df = pd.DataFrame(
            columns=['price', 'area_total', 'price_permeter', 'apartment_room_number', 'apartment_floor',
                     'building_year'])
        for i in ind[test_index]:
            id = df.index[i]
            price = float(df.price[id])
            area_total = round(df.area_total[id], 1)
            price_per_m = round(df.price[id] / df.area_total[id], 1)
            apartment_room_number = df.apartment_room_number[id]
            apartment_floor = df.apartment_floor[id]
            building_year = df.building_year[id]
            results_df = pd.DataFrame(
                np.array([[price, area_total, price_per_m, apartment_room_number, apartment_floor, building_year]]),
                columns=['price', 'area_total', 'price_permeter', 'apartment_room_number', 'apartment_floor',
                         'building_year']).append(results_df, ignore_index=True)

        return results_df

    def save_model(self, model, model_name):
        decision_tree_pkl_filename = f"{model_name}.pkl"
        model_pkl = open(decision_tree_pkl_filename, 'wb')
        pickle.dump(model, model_pkl)
        model_pkl.close()

    def summary(self, df, result_df, test_X, test_index):
        print('Wycena mieszkania na podstawie mieszkań podobnych:')
        print('1. Wg cena całkowitych mieszkań podobnych')
        print(" - cena średnia:", pd.to_numeric(result_df['price'], errors='coerce').apply(float).mean())
        print(" - cena minimalna: ", pd.to_numeric(result_df['price'], errors='coerce').apply(float).min())
        print(" - cena maksymalna: ", pd.to_numeric(result_df['price'], errors='coerce').apply(float).max())
        print('2. Wg cen za m2 mieszkań podobnych')
        print(" - średnia cena za m2:", pd.to_numeric(result_df['price_permeter'], errors='coerce').apply(float).mean())
        print(" - cena minimalna za m2: ",
              pd.to_numeric(result_df['price_permeter'], errors='coerce').apply(float).min())
        print(" - cena maksymalna za m2: ",
              pd.to_numeric(result_df['price_permeter'], errors='coerce').apply(float).max())
        print("3. Wycena mieszkania testowego na podstawie średniej ceny mieszkań podobnych: ", round(
            test_X.iloc[test_index]['area_total'] * pd.to_numeric(result_df['price_permeter'], errors='coerce').apply(
                float).mean(), 1))
        try:
            offer_id = df.index[test_index]
            print(f"4. testowa oferta")
            print(colored(df.loc[offer_id, :], "red"))
        except Exception as e:
            print(colored(e, "red"))


class TTT:

    def __init__(self):
        features = Features()
        files = features.paths("data")
        for file in files:
            if "fixed_estates" in file:
                print(
                    colored(
                        f"!!!======================={colored(file, 'green')}{colored('=======================!!!', 'red')}",
                        "red"))
                df = features.prepare_df(file)
                df = features.test_features(df)
                dropped = []
                to_drop = ["fixed_province",
                           "pop_province",
                           "offer_transaction",
                           "offer_transaction_knn",
                           "id",
                           "portal_id",
                           # "fixed_latitude", "fixed_longitude",
                           "private_offer",
                           "private_offer_knn",
                           "main_type_id",
                           "main_type_id_knn",
                           "pop_city",
                           "pop_district",
                           "area_total_knn",
                           "pop_man_knn",
                           "pop_woman_knn",
                           "pop_population_knn",
                           "pop_long_knn",
                           "pop_lat_knn",
                           "fixed_longitude_knn",
                           "fixed_latitude_knn",
                           "building_year_knn",
                           "apartment_room_number_knn",
                           "apartment_floor_knn",
                           "price_knn",
                           ]
                for d in to_drop:
                    if d in df.columns:
                        dropped.append(d)
                df_train = df.drop(dropped, axis=1)
                df_train = df_train.dropna()
                try:
                    r = Recommendation(df_train, file.replace(".csv", ""))
                    print(r.results_df)
                except Exception as e:
                    print(colored(e, "red"))
