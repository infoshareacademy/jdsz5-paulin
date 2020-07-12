from termcolor import colored

from recommendation import Recommendation
from test import Features

if __name__ == "__main__":
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
            print(colored(f"columns: {df_train.columns}", "yellow"))
            m = features.find_missing_cols(df_train)
            n = features.find_numeric_cols(df_train)
            print(df_train.shape)
            print(df_train.info())
            try:
                r = Recommendation(df_train, file.replace(".csv", ""))
                print(r.results_df)
            except Exception as e:
                print(colored(e, "red"))
