import io

import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

from sklearn.preprocessing import LabelEncoder
from termcolor import colored

# from ml._init import Model_ols, rest_models, General_data
# from ml.arguments_cmd import CMD
from _init import Model_ols, rest_models, General_data
from arguments_cmd import CMD


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

    def prepare_df(self, file, m_df=None):
        if m_df is None:
            df = pd.read_csv(f"data/{file}", low_memory=False)
        else:
            df = m_df
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

    def get_arguments(self):
        return CMD(
            args=[
                {"command": "--file", "type": str, "help": "file name"},
                {"command": "--add_to_name", "type": str, "help": "file name"},
                {"command": "--portal_mask", "type": int, "help": "declare portal scrapping"},
            ]
        ).get_args()


def run(file, add_to_name, portal_mask):
    try:
        f = open(f'output/{file}_results.txt', 'a')
        f.write(f"!!!======================={file}=======================!!!" + "\n")
        df = features.prepare_df(file)
        if portal_mask is not None and portal_mask != 0:
            df = df[df["portal_id"] == portal_mask]
        if "3" in df.columns:
            df["price"] = df["3"]
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
                   "apartment_floor",
                   ]
        for d in to_drop:
            if d in df.columns:
                dropped.append(d)
        df_train = df.drop(dropped, axis=1)
        df_train = df_train.dropna()
        f.write(f"columns: \n{df_train.columns}" + "\n")
        print(colored(f"columns: {df_train.columns}", "yellow"))
        # features.uniques(df, "fixed_province")
        m = features.find_missing_cols(df_train)
        f.write("missed cols" + "\n")
        features.save_entries(m, f)
        n = features.find_numeric_cols(df_train)
        f.write("numeric cols" + "\n")
        features.save_entries(n, f)
        f.write("shape: \n" + str(df_train.shape) + "\n")
        print(df_train.shape)
        buffer = io.StringIO()
        df_train.info(buf=buffer)
        s = buffer.getvalue()
        f.write("df_train info: \n" + s + "\n")
        print(df_train.info())
        # general_info.feature_importants(df_train)
        # mo = Model_ols(df_train)
        # f.write("model: \n" + str(mo.model) + "\n")
        # f.write("best model: \n" + str(mo.best_model) + "\n")
        # f.write("features: \n" + str(mo.features) + "\n")
        # f.close()
        print("closing")
        rm = rest_models(df_train, file,
                         add_to_name=add_to_name
                         )
        results.append(rm.res)
    except Exception as e:
        print(colored(e, "red"))


if __name__ == "__main__":
    features = Features()
    args = features.get_arguments()
    file_name = args.file
    add_to_name = args.add_to_name
    portal_mask = args.portal_mask
    print(f"portal model: {portal_mask}")
    # file_name = "final_estates.csv"
    files = features.paths("data")
    results = []
    general_info = General_data()

    for file in files:
        print(
            colored(
                f"!!!======================={colored(file, 'green')}{colored('=======================!!!', 'red')}",
                "red"))
        if file_name is None:
            run(file, add_to_name, portal_mask)
        else:
            if file_name == file:
                run(file, add_to_name, portal_mask)
