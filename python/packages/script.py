import pandas as pd
from pandas import DataFrame


class Datasets:
    df: DataFrame = None

    def __init__(self):
        self.df = self.__load_data()

    def __load_data(self,
                    file_path: str = 'data/globalterrorism.csv',
                    encoding: str = "ISO-8859-1",
                    low_memory: bool = True):
        return pd.read_csv(file_path, encoding=encoding, low_memory=low_memory)

    def select_columns(self, df: DataFrame, columns: list, with_dropna: bool = False):
        if not with_dropna:
            return df[columns]
        else:
            return self.clean_data(df[columns])

    def clean_data(self, df: DataFrame):
        return df.dropna()

    def get_cleaned_data(self):
        df = self.__load_data()
        self.select_columns(df, ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'city', 'attacktype1_txt',
                                 'targtype1_txt', 'weaptype1_txt', 'nkill', 'natlty1_txt'])

    def display_all_data(self):
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)


class Plots(Datasets):
    pass
