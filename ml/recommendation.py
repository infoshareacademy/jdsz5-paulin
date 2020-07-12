import pickle
from random import randrange

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import BallTree
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from termcolor import colored


class Recommendation:

    def __init__(self, df, file_name, ball=None):
        if df is None:
            df = self.__prepare_df(file_name)
        self.df = self.prepare_df(df)
        self.file_name = file_name
        self.X_train, self.x_test, self.Y_train, self.Y_test = self.prepare_train_test(df)
        self.train_X_norm, self.test_X_norm = self.prepare_scaling(self.X_train, self.x_test)
        if ball is None:
            self.tree = self.prepare_ball(self.train_X_norm)
        else:
            self.tree = ball
        print(colored(self.test_X_norm.shape, "red"))
        self.dist, self.ind = self.test_ball(self.tree, self.test_X_norm)
        self.test_index = self.prepare_test_index(self.test_X_norm)
        self.results_df = self.results_ball(self.ind, self.df, self.test_index)
        self.summary(self.df, self.results_df, self.x_test, self.test_index)
        self.save_model(self.tree, f"models/recommendation/{self.file_name}_recomendation_knn")

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
            df_train = df.drop(dropped, axis=1)
            df = df_train.dropna()
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
        test_index = randrange(0, len(df) - 1)
        return test_index

    def test_ball(self, tree, test_X_norm, k=5):
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
