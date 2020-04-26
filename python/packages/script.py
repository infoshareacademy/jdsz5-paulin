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

    def display_all_data(self):
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)


class Plots(Datasets):
    pass
