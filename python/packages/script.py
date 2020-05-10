import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import scipy.stats as st
from pandas import Series, DataFrame
from pandas.core.groupby import GroupBy
from scipy.stats import ttest_ind


class Dataset:

    # Dataframe load
    def dataset(self):
        df = pd.read_csv("data/globalterrorism.csv", encoding="ISO-8859-1", low_memory=False)[
            ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'city', 'attacktype1_txt',
             'targtype1_txt', 'weaptype1_txt', 'nkill', 'natlty1_txt']].dropna()
        return df

    def get_group_by(self, dataframe: DataFrame, group_by_columns: list) -> GroupBy:
        group_by = dataframe.groupby(group_by_columns)
        return group_by

    def get_count_group_by(self, dataframe: DataFrame, group_by_columns: list, compare_columns: str) -> Series:
        group_by = self.get_group_by(dataframe, group_by_columns)
        group_by_count = group_by[compare_columns].count()
        return group_by_count

    def get_sum_group_by(self, dataframe: DataFrame, group_by_columns: list, compare_columns: str) -> Series:
        group_by = self.get_group_by(dataframe, group_by_columns)
        group_by_count = group_by[compare_columns].sum()
        return group_by_count

    def get_describe_group_by(self, dataframe: DataFrame, group_by_columns: list, compare_columns: list) -> DataFrame:
        group_by = self.get_group_by(dataframe, group_by_columns)
        group_by_describe = group_by[compare_columns].describe()
        return group_by_describe

    def bootstrapping(self, x: np.array, y: np.array, n: int = 1000, alpha: float = 0.05):
        p_values = list()
        for i in range(n):
            # print(f"iteration: {i}")
            x_sample = np.random.choice(x, len(x), replace=True)
            y_sample = np.random.choice(y, len(y), replace=True)
            t_student_test = ttest_ind(x_sample, y_sample)
            # checking result importance
            p = (t_student_test.pvalue < alpha) * 1
            # print(f"p value importance {p}")
            p_values.append(p)
        p_value_mean = np.mean(p_values)
        return p_values, p_value_mean

    def simulation(self, x: np.array, y: np.array, xm: float, ym: float, xs: float, ys: float, n=1000, alpha=0.05):
        p_values = []
        for i in range(n):
            sample_x = x + np.random.normal(xm, xs, len(x)).round()
            sample_y = y + np.random.normal(ym, ys, len(y)).round()
            tst = ttest_ind(sample_x, sample_y)
            p = (tst.pvalue < alpha) * 1
            p_values.append(p)
        p_value_mean = np.mean(p_values)
        return p_values, p_value_mean

    def bootstrap_range_of_difference(self, x: np.ndarray, y: np.ndarray, n: int = 1000, alpha: float = 0.05):
        diff = []
        for i in range(n):
            sample_x = np.random.choice(x, len(x), replace=True)
            sample_y = np.random.choice(y, len(y), replace=True)
            diff.append(np.mean(sample_x) - np.mean(sample_y))
        orig_diff = np.mean(x) - np.mean(y)
        lcb = orig_diff + np.percentile(diff, alpha / 2)
        ucb = orig_diff + np.percentile(diff, 1 - alpha / 2)
        return lcb, ucb


class Plots:

    def plot_bars(self, dataframe: DataFrame, y_label: str, title: str):
        cols = dataframe.columns
        labels = dataframe.index.tolist()
        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars
        fig, ax = plt.subplots()

        rects_list = list()
        for col in cols:
            rect = ax.bar(x - width / len(cols), dataframe[col].values, width, label=col)
            rects_list.append(rect)

        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        plt.xticks(rotation=90)

        def autolabel(rects, c):
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / c, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom')

        for rect in rects_list:
            autolabel(rect, len(cols))

        fig.tight_layout()
        plt.show()

    def plot_hist(self, data: Series, title: str, color: str = None, font_size: int = 8):
        plt.figure(figsize=(8, 7))
        d = data.index
        if color is None:
            plt.bar(d, height=data)
        else:
            plt.bar(d, height=data, color=color)
        self.__show_plots(title, data, font_size)

    def plot_hist_and_line(self, data: Series, title: str, color: str = None, font_size: int = 8,
                           color_second: str = None):
        plt.figure(figsize=(8, 7))
        d = data.index
        if color is None:
            plt.bar(d, height=data)
        else:
            plt.bar(d, height=data, color=color)
        if color_second is None:
            plt.plot(d, data)
        else:
            plt.plot(d, data, color=color_second)
        self.__show_plots(title, data, font_size)

    def __show_plots(self, title: str, data: Series, font_size: int):
        plt.xticks(rotation=90)
        plt.title(title)
        for index, data in enumerate(data):
            plt.text(x=index, y=data + 1, s=f"{data}", fontdict=dict(fontsize=font_size), va='center')
        plt.tight_layout()
        plt.show()


# ASIA
class GeneralInfo:

    def __init__(self):
        self.st = StatisticTests()
        self.df = self.st.df

    def region_plots(self):
        fig, ax = plt.subplots(figsize=(20, 10))
        sns.countplot(self.df.region_txt, ax=ax)
        plt.xticks(rotation=90, size=15)
        plt.title('ilość ataków terrorystycznych w poszczególnych regionach')

    def groupby_attack_type(self, attack_type):
        grouped_count = self.df[['nkill']].where(self.df.attacktype1_txt == attack_type).groupby(
            self.df.region_txt).count()
        return grouped_count

    def box_plots(self):
        attack_types = self.st.get_uniques(["attacktype1_txt"])
        sum_nkill = self.df[['nkill']].groupby(self.df.region_txt).count()
        print(attack_types)
        attacks = list()
        for attack in attack_types:
            at = self.df[['nkill']].where(self.df.attacktype1_txt == attack).groupby(self.df.region_txt).count()
            attacks.append(at)

        r = None
        for i, attack in enumerate(attacks):
            if i == 0:
                r = pd.merge(attacks[i], attacks[i + 1], how='left', left_on=['region_txt'], right_on=['region_txt'])
            elif i == len(attacks):
                r = pd.merge(r, sum_nkill, how='left', left_on=['region_txt'], right_on=['region_txt'])
            else:
                r = pd.merge(r, attacks[i], how='left', left_on=['region_txt'], right_on=['region_txt'])
        plot = r.boxplot(rot=90, figsize=(20, 10), fontsize=15)
        return plot


class StatisticTests:

    def __init__(self):
        self.dataset = Dataset()
        self.df = self.dataset.dataset()

    def run_test_by_region(self, for_attack: str, for_region_x: str, for_region_y: str) -> None:
        columns = ['attacktype1_txt', 'region_txt']
        self.run_test(for_attack, for_region_x, for_region_y, columns, None)

    def run_test_by_targets(self, for_attack: str, for_target_x: str, for_target_y: str, for_region: str) -> None:
        columns = ['attacktype1_txt', 'targtype1_txt']
        self.run_test(for_attack, for_target_x, for_target_y, columns,
                      {"region_txt": for_region, columns[0]: for_attack})

    def run_test(self, for_population: str, for_x: str, for_y: str, columns: list, multiple_populations: dict):
        population, x_types, y_types = self.get_population(for_population, for_x, for_y, columns,
                                                           multiple_populations)
        population_group_by, x_group_by, y_group_by = self.get_grouped_by_column(population, x_types, y_types,
                                                                                 columns)
        x_y = self.get_concated_dataframes(x_group_by, y_group_by, [for_x, for_y])
        self.dataset.plot_bars(x_y, "Victims",
                               f'Compare of victims of {for_population} between {for_x} and {for_y}')
        p_value_by_test, statistic_by_test, p_values_bootstrapping, p_value_bootstrapping_mean, p_values_simulation, p_value_simulation, lcb, ucb = self.compare_sub_datasets(
            x_group_by, y_group_by)
        print(f"result of one test p_value {p_value_by_test} statistic {statistic_by_test}")
        print(f"result of mean p_values {p_value_bootstrapping_mean}")
        print(f"result of simulation p_values {p_value_simulation}")
        print(
            'Result of bootstrapping test is important in {0} simulations'.format(
                "{:.1%}".format(p_value_bootstrapping_mean))
        )
        print('Result of simulation test is important in {0} simulations'.format(
            "{:.1%}".format(p_value_bootstrapping_mean)))
        print('Przedział ufności różnic: ({0},{1})'.format(lcb.round(4), ucb.round(4)))
        if lcb < 0 and ucb > 0:
            info = '0 zawiera się w przedziale ufności, więc nie mamy podstaw twierdzić że róznica jest istotna.'
        else:
            info = '0 nie zawiera się w przedziale ufności, więc przyjmujemy różnicę za istotną.'
        print(info)

    def get_uniques(self, columns) -> list:
        unique_values = list()
        for column in columns:
            unique_values.append(self.df[column].unique())
        return unique_values

    def get_population(self, attack_type: str, region_x: str, region_y: str, columns: list,
                       multiple_types: dict = None) -> (
            DataFrame, DataFrame, DataFrame):
        if multiple_types is not None:
            population = self.df
            for col, m_type in multiple_types.items():
                population = population.loc[self.df[col].str.contains(m_type, case=False)]
        else:
            population = self.df.loc[self.df[columns[0]].str.contains(attack_type, case=False)]
        x_types = population.loc[population[columns[1]].str.contains(region_x, case=False)][population.nkill > 0]
        y_types = population.loc[population[columns[1]].str.contains(region_y, case=False)][population.nkill > 0]
        return population, x_types, y_types

    def get_grouped_by_column(self, population: DataFrame, x_types: DataFrame, y_types: DataFrame,
                              columns: list) -> (
            Series, Series, Series):
        population_group_by = self.dataset.get_group_by(population, [columns[0]])["nkill"].sum()
        x_group_by = self.dataset.get_group_by(x_types, [columns[1]])["nkill"].sum()
        y_group_by = self.dataset.get_group_by(y_types, [columns[1]])["nkill"].sum()
        return population_group_by, x_group_by, y_group_by

    def get_concated_dataframes(self, x_group_by: Series, y_group_by: Series, column_names: list) -> DataFrame:
        x_y = pd.concat([x_group_by.to_frame(), y_group_by.to_frame()], axis=1, sort=False)
        x_y.columns = column_names
        return x_y

    def get_described_data_frames(self, x_group_by: Series, y_group_by: Series) -> (Series, Series):
        x_describe = x_group_by.describe()
        y_describe = y_group_by.describe()
        return x_describe, y_describe

    def compare_sub_datasets(self, x_group_by: Series, y_group_by: Series):
        x = np.array(x_group_by)
        y = np.array(y_group_by)
        t_student_test = ttest_ind(x, y)
        p_value_by_test = t_student_test.pvalue
        statistic_by_test = t_student_test.statistic
        p_values_bootstrapping, p_value_bootstrapping_mean = self.dataset.bootstrapping(x, y)
        p_values_simulation, p_value_simulation = self.dataset.simulation(x, y, 0, 0.2, 1.5, 1.2)
        lcb, ucb = self.dataset.bootstrap_range_of_difference(x, y)
        return p_value_by_test, statistic_by_test, p_values_bootstrapping, p_value_bootstrapping_mean, p_values_simulation, p_value_simulation, lcb, ucb


class Victims:

    def __init__(self):
        self.tests = StatisticTests()
        self.df = self.tests.df[self.tests.df.nkill > 0]
        self.df_non_nkill = self.tests.df
        self.dataset = self.tests.dataset
        self.df_columns = self.df.columns

    def get_victims(self, region: str, target_x: str, target_y: str, additional_filter: str = None):
        df = self.df.loc[self.df["region_txt"].str.contains(region, case=False)]

        targets = df.groupby(['targtype1_txt', "iyear"]).count()['nkill'].reset_index()
        target_types = targets.groupby('targtype1_txt').mean()
        # dataset.plot_hist(target_types, "means of targets")

        business = targets.loc[targets['targtype1_txt'].str.contains(target_x, case=False)]['nkill']
        government = targets.loc[targets['targtype1_txt'].str.contains(target_y, case=False)]['nkill']
        business_series = pd.Series({target_x: business.sum()}, index=[target_x])
        government_series = pd.Series({target_y: government.sum()}, index=[target_y])
        x = np.array(business)
        y = np.array(government)
        x_y = self.tests.get_concated_dataframes(business, government,
                                                 [f"{target_x} in {region}", f"{target_y} in {region}"])
        if additional_filter is None:
            message = f"Victims in {region}: {target_x} and {target_y} sections"
        else:
            message = f"Victims in {region}: {target_x} and {target_y} sections ({additional_filter})"
        self.dataset.plot_bars(x_y, "Victims", message)

        # Test
        t_student_test = ttest_ind(x, y)
        p_value_by_test = t_student_test.pvalue
        statistic_by_test = t_student_test.statistic

        p_values_bootstrapping, p_value_bootstrapping_mean = self.dataset.bootstrapping(x, y)
        p_values_simulation, p_value_simulation = self.dataset.simulation(x, y, 0, 0.2, 1.5, 1.2)
        lcb, ucb = self.dataset.bootstrap_range_of_difference(x, y)
        print(f"result of one test p_value {p_value_by_test} statistic {statistic_by_test}")
        if p_value_bootstrapping_mean > 0.5:
            print('Result of bootstrapping test is important in {0} simulations'.format(
                "{:.1%}".format(p_value_bootstrapping_mean)))
        else:
            print('Result of bootstrapping test is important in {0} simulations'.format(
                "{:.1%}".format(p_value_bootstrapping_mean)))

        # if p_value_simulation > 0.5:
        #     print_accept('Result of simulation test is important in {0} simulations'.format(
        #         "{:.1%}".format(p_value_simulation)))
        # else:
        #     print('Result of simulation test is important in {0} simulations'.format(
        #         "{:.1%}".format(p_value_simulation)))
        print('Przedział ufności różnic: ({0},{1})'.format(lcb.round(4), ucb.round(4)))
        if lcb < 0 and ucb > 0:
            info = '0 zawiera się w przedziale ufności, więc nie mamy podstaw twierdzić że róznica jest istotna.'
        else:
            info = '0 nie zawiera się w przedziale ufności, więc przyjmujemy różnicę za istotną.'
        print(info)
        return p_value_by_test, p_value_bootstrapping_mean, p_value_simulation, lcb, ucb


# PAULINA
class Propability:

    def __init__(self):
        self.tests = StatisticTests()
        self.df = self.tests.df

    # wybranie tylko używanych kolumn
    def dataset(self):
        df_pred = self.df['iyear', 'region_txt', 'targtype1_txt', 'weapon']
        return df_pred

    # definicja po czym bedzie grupowanie (lista)
    def filtr(self, df_pred, col_name=None, col_val=None):
        if col_val is None:
            col_val = ['USA', 'Firearms']
        if col_name is None:
            col_name = ['region_txt', 'weapon']
        mask = (self.dataset()[col_name[0]] == col_val[0]) & (self.dataset()[col_name[1]] == col_val[1])
        group = df_pred.ix(mask)
        return group

    # co jest naszym celem do wyznaczenia prawdopodobieństwa
    def goal(self, group, target):
        item_predict = group[target].count()
        return item_predict

    def whole(self, df_pred):
        item_all = df_pred.count()
        return item_all

    def possibility(self, goal, item_all):
        possib = goal / item_all
        return possib


# PAULINA
class Thesis:

    def __init__(self, x, y):
        self.tests = StatisticTests()
        self.df = self.tests.df
        if len(x) < 60 or len(y) < 60:
            print('grupa niereprezentatywna do działań statystycznych')
        elif len(x) > 60 and len(y) > 60:
            pass

    def dataset(self):
        df_pred = self.df('iyear', 'region_txt', 'targtype1_txt', 'weapon')
        return df_pred

    def filtr(self, df_pred, col_name=None, col_val=None, goal=None):
        if col_val is None:
            col_val = ['USA', 'Firearms', '1970']
        if col_name is None:
            col_name = ['region_txt', 'weapon', 'iyear']
        if goal is None:
            goal = df_pred['nkill']

        x = df_pred.loc[(df_pred[col_name[0]] == col_val[0]) & (df_pred[col_name[1]] == col_val[1]) & (
                df_pred[col_name[2]] == col_val[2]), [goal]]
        y = df_pred.loc[(df_pred[col_name[0]] == col_val[0]) & (df_pred[col_name[1]] == col_val[1]) & (
                df_pred[col_name[2]] == col_val[2]), [goal]]
        return x, y

    def question(self, x, y):
        print(
            'W ROKU {} W REGIONIE{} DOSZŁO DO WIEKSZEJ ILOŚCI PRZESTĘPSTW Z UZYCIEM {} NIŻ ZA POMOCĄ {} W REGIONIE {}'.format(
                x[2], x[0], x[1], y[1], y[0]))
        # czyli mx>my
        x_avg = x.mean()
        x_std = x.std()
        x_n = len(x)
        y_avg = y.mean()
        y_std = y.std()
        y_n = len(y)
        alfa = 0.05  # założone do porówanania z pval
        # tools gorsze niż pozostałe czyli lewostronny obszar krytyczny
        # hipoteza alternatywna (!=)
        u = (x_avg - y_avg) / np.sqrt(x_std ** 2 / x_n + y_std ** 2 / y_n)
        norm = st.norm()
        pval = norm.cdf(u)
        print('x_mean:', x_avg)
        print('y_mean:', y_avg)
        if pval > alfa:
            print(
                'brak mozliwości odrzucenia hipotezy 0: brak różnicy w średniej ilości zabitych zgodnie z zaznaczonymi kategotiami')
        elif pval < alfa:
            if x_avg > y_avg:
                print('')
        print('statystyka testowa:', u, 'p-value:', pval,
              'p-val wysokie, brak możliwości odrzucenia hipotezy zerowej, dlatego też hipoteza alternatywna nie jest rozważana')
