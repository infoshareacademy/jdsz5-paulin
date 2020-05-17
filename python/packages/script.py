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
        filename = "data/globalterrorismdb_0718dist.csv"
        if self.file_exists(filename):
            df = self.load_df(filename)
        else:
            if not os.path.exists("data"):
                os.makedirs("data")
            self.download_df()
            df = self.load_df(filename)
        return df

    def download_df(self):
        import kaggle
        k = kaggle.KaggleApi({"username": "jdsz5paulina", "key": "5277445bf2e6cef9aac564d8f7c5b87d"})
        k.authenticate()
        print("kaggle.com: authenticated")
        k.dataset_download_cli("START-UMD/gtd", unzip=True, path="data")

    def load_df(self, filename):
        df = pd.read_csv(filename, encoding="ISO-8859-1", low_memory=False)[
            ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'city', 'attacktype1_txt',
             'targtype1_txt', 'weaptype1_txt', 'nkill', 'natlty1_txt']].dropna()
        return df

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
            x_sample = np.random.choice(x, len(x), replace=True)
            y_sample = np.random.choice(y, len(y), replace=True)
            t_student_test = ttest_ind(x_sample, y_sample)
            p = (t_student_test.pvalue < alpha) * 1
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


class GeneralInfo:

    def __init__(self):
        self.st = StatisticTests()
        self.df = self.st.df
        self.plot = Plots()

    def distribution_data(self, region):
        x = self.region_data(region)['nkill']
        self.plot.plot_distribution(x, region)

    def region_data(self, region, columns=None):
        if columns is None:
            columns = ["iyear"]
        df = self.df.loc[self.df["region_txt"].str.contains(region, case=False)]
        t = df.groupby(columns).count()
        targets = df.groupby(columns)["nkill"].sum().reset_index()
        targets['attacks'] = t['nkill'].values
        t = targets['nkill'] / targets['attacks']
        targets['stopa_smierci'] = t
        return targets

    def select_data_year(self, year, region, col_type):
        targets = self.region_data(region, ["iyear", col_type])
        uniques = targets[col_type].unique()
        max_height = self.df.loc[self.df['nkill'].idxmax()]
        x = targets.loc[targets["iyear"] == year]
        l = [0.0] * len(uniques)
        di = dict(zip(uniques, l))
        for i, k in x.iterrows():
            w = k[col_type]
            ki = k['nkill']
            di[w] = ki
        uniq = list(di.keys())
        vals = list(di.values())
        return uniq, vals

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
        attacks = list()
        for attack in attack_types[0]:
            at = self.df['nkill'].where(self.df.attacktype1_txt == attack).groupby(self.df.region_txt).count()
            attacks.append(at)

        r = None
        for i, attack in enumerate(attacks):
            if i == 0:
                r = pd.merge(attacks[i], attacks[i + 1], how='left', left_on=['region_txt'], right_on=['region_txt'])
            elif i == len(attacks):
                r = pd.merge(r, sum_nkill, how='left', left_on=['region_txt'], right_on=['region_txt'])
            else:
                r = pd.merge(r, attacks[i], how='left', left_on=['region_txt'], right_on=['region_txt'])
        r.columns = ['Armed_Assault', 'Assassination', 'Bombing_Explosion', 'Facility_Infrastructure_Attack',
                     'Hijacking', 'Hostage_Taking(Barricade_Incident)', 'Hostage_Taking(Kidnapping)', 'Unarmed_Assault',
                     'Unknown', 'All']
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
        print(columns[1], region_y)
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

    def select_unique_target_types(self):
        unique = self.tests.get_uniques(["targtype1_txt"])
        return unique[0]

    def get_victims(self, region: str, target_x: str, target_y: str, additional_filter: str = None):
        df = self.df.loc[self.df["region_txt"].str.contains(region, case=False)]

        targets = df.groupby(['targtype1_txt', "iyear"]).count()['nkill'].reset_index()

        business = targets.loc[targets['targtype1_txt'].str.contains(target_x, case=False)]['nkill']
        government = targets.loc[targets['targtype1_txt'].str.contains(target_y, case=False)]['nkill']
        x = np.array(business)
        y = np.array(government)
        x_y = self.tests.get_concated_dataframes(business, government,
                                                 [f"{target_x} in {region}", f"{target_y} in {region}"])
        # Test
        t_student_test = ttest_ind(x, y)
        p_value_by_test = t_student_test.pvalue
        statistic_by_test = t_student_test.statistic
        samples = 1000
        p_values_bootstrapping, p_value_bootstrapping_mean = self.dataset.bootstrapping(x, y, n=samples)
        p_values_simulation, p_value_simulation = self.dataset.simulation(x, y, 0, 0.2, 1.5, 1.2)
        lcb, ucb = self.dataset.bootstrap_range_of_difference(x, y)
        print(f"p_value {p_value_by_test} statistic {statistic_by_test}")
        print(
            'Wynik testu istotny w {0} symulacji dla {1} prób'.format("{:.1%}".format(np.mean(p_values_bootstrapping)),
                                                                      samples))

        print('Przedział ufności różnic: ({0},{1})'.format(lcb.round(4), ucb.round(4)))
        if lcb < 0 and ucb > 0:
            info = '0 zawiera się w przedziale ufności, więc nie mamy podstaw twierdzić że róznica jest istotna.'
        else:
            info = '0 nie zawiera się w przedziale ufności, więc przyjmujemy różnicę za istotną.'
        print(info)
        return p_value_by_test, p_value_bootstrapping_mean, p_value_simulation, lcb, ucb


class Plots:

    def plot_distribution(self, x, title):
        title = f"Histogram ilości ofiar śmiertelnych wraz z rozkładami w kontynencie: {title}"
        g = sns.distplot(x, fit=norm).set_title(title)
        plt.legend(title="Legenda", loc='upper right', labels=["Rozkład normalny", "Rozkład ilości ofiar śmiertelnych"])
        plt.show(g)

    def plot_with_subplots(self, x, y_min=0, y=None, cstm=None):
        if cstm is not None:
            fig, ax = plt.subplots(1, 1)
            # color = next(ax._get_lines.prop_cycler)['color']
            ax.plot(x, cstm.pmf(x), 'ro', ms=12, markeredgecolor='none')
            ax.vlines(x, y_min, cstm.pmf(x), colors=['r', 'b'], lw=4)
            # frame = pd.DataFrame({"x": x, "y": cstm.pmf(x)})
            # sns.lmplot(x='x', y='y', data=frame, palette='hls', fit_reg=False, size=5,
            #            aspect=5 / 3, legend_out=False, scatter_kws={"s": 70})
        elif x is not None and y is not None:
            fig, ax = plt.subplots(1, 1)
            ax.plot(x, st.poisson.pmf(x, y), 'bo', ms=8)
            ax.vlines(x, 0, st.poisson.pmf(x, y), colors='b', lw=5, alpha=0.5)
        elif y is not None:
            fig, ax = plt.subplots(1, 1)
            ax.plot(x, y, 'ro', ms=12, mec='r')
            ax.vlines(x, y_min, y, colors='r', lw=4)
        plt.show()

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


class ResultsModel:
    gaussian_message_for_x = None
    gaussian_message_for_y = None
    gaussian_p_value_x = None
    gaussian_p_value_y = None
    t_welch_message = None
    t_welch_p_value = None
    is_gaussian_x = None
    is_gaussian_y = None
    is_poisson_x = None
    is_poisson_y = None

    def __str__(self) -> str:
        return f"ResultsModel[" \
               f"\n gaussian_message_for_x={self.gaussian_message_for_x}," \
               f"\n gaussian_message_for_y={self.gaussian_message_for_y}," \
               f"\n gaussian_p_value_x={self.gaussian_p_value_x}," \
               f"\n gaussian_p_value_y={self.gaussian_p_value_y}," \
               f"\n t_welch_message={self.t_welch_message}," \
               f"\n t_welch_p_value={self.t_welch_p_value}," \
               f"\n is_poisson_x={self.is_poisson_x}," \
               f"\n is_poisson_x={self.is_poisson_y}" \
               f"\n ]"


class PValueTests:

    def __init__(self):
        self.st = StatisticTests()
        self.df = self.st.df[self.st.df.nkill > 0]
        self.ploting = Plots()
        self.result_model = ResultsModel()

    def select_unique_weapons(self):
        unique = self.st.get_uniques(["weaptype1_txt"])
        return unique[0]

    def __get_variables(self, year=None, weapons=None):
        if year is None:
            year = 1970
        if weapons is None:
            weapons = ['Firearms', 'Explosives']
        x = self.df.loc[(self.df['weaptype1_txt'] == weapons[0]) & (self.df['iyear'] == year), ['nkill']]
        y = self.df.loc[(self.df['weaptype1_txt'] == weapons[1]) & (self.df['iyear'] == year + 1), ['nkill']]
        return x, y

    def __group_variable(self, variable):
        dictionary = variable.groupby(['nkill'])['nkill'].sum()
        return dictionary

    def __prepare_discrete_variable(self, d, columns=None):
        if columns is None:
            columns = {'nkill': 'suma'}
        discrete_x = pd.DataFrame.from_dict(d)
        discrete_x.rename(columns=columns, inplace=True)
        discrete_x.reset_index(level=0, inplace=True)
        discrete_x['density'] = discrete_x['suma'] / sum(discrete_x['suma'])
        return discrete_x

    def __create_discrete_object(self, xk, pk):
        custm = st.rv_discrete(name='custm', values=(xk, pk))
        return custm

    def __select_values_for_discrete(self, discrete):
        xk = discrete['nkill']
        pk = discrete['density']
        return xk, pk

    def __check_gaussian_distribution(self, y):
        Y = pd.DataFrame.to_numpy(y)
        y_normed = Y / Y.max(axis=0)
        k2, p = st.normaltest(y_normed)
        alpha = 0.05
        print("p_value = {}".format(p))
        if p < alpha:  # null hypothesis: x comes from a normal distribution
            message = "dane nie podlegają rozkładowi normalnemu"
            res = False
        else:
            message = "dane podlegają rozkładowi normalnemu"
            res = True
        return message, p, res

    def __check_poisson_distribution(self, x):
        mu = np.mean(x['nkill'])
        mean, var, skew, kurt = st.poisson.stats(mu, moments='mvsk')
        kw = np.arange(st.poisson.ppf(0.01, mu),
                       st.poisson.ppf(0.99, mu))
        self.ploting.plot_with_subplots(x=kw, y=mu)
        prob = st.poisson.cdf(kw, mu)
        poisson_result = np.allclose(kw, st.poisson.ppf(prob, mu))
        return poisson_result

    def __t_welch_test(self, x, y):
        X = pd.DataFrame.to_numpy(x)
        Y = pd.DataFrame.to_numpy(y)
        n1 = len(X)
        n2 = len(Y)
        rvs1 = st.norm.rvs(size=n1, loc=0., scale=1)
        rvs2 = st.norm.rvs(size=n2, loc=0., scale=1)
        st.ttest_ind(rvs1, rvs2)
        ttest = st.ttest_ind(rvs1, rvs2, equal_var=False)
        alpha = 0.05
        if ttest.pvalue < alpha:
            message = "dla testu T Welcha rozkłady są do siebie zbliżone, potwierdzenie hipotezy zero"
        else:
            message = "dla testu T Welcha rozkłady nie są do siebie zbliżone, potwierdzenie hipotezy alternatywnej."
        return message, ttest.pvalue

    def run(self, year=None, weapons=None):
        if weapons is None:
            weapons = ['Firearms', 'Explosives']
        x, y = self.__get_variables(year, weapons)
        dictionary = self.__group_variable(x)
        discrete_x = self.__prepare_discrete_variable(dictionary)
        xk, pk = self.__select_values_for_discrete(discrete_x)
        custm = self.__create_discrete_object(xk, pk)
        yk = custm.pmf(x)
        self.ploting.plot_with_subplots(xk, cstm=custm)
        try:
            message, p, res = self.__check_gaussian_distribution(y)
            self.result_model.gaussian_message_for_y = message
            self.result_model.gaussian_p_value_y = p
            self.result_model.is_gaussian_y = res
            if not res:
                self.result_model.is_poisson_y = self.__check_poisson_distribution(x)
        except Exception as e:
            self.result_model.gaussian_message_for_y = f"Brak danych dla roku {year} oraz broni: {weapons[1]}"
        try:
            message, p, res = self.__check_gaussian_distribution(x)
            self.result_model.gaussian_message_for_x = message
            self.result_model.gaussian_p_value_x = p
            self.result_model.is_gaussian_x = res
            if not res:
                self.result_model.is_poisson_x = self.__check_poisson_distribution(x)
        except Exception as e:
            self.result_model.gaussian_message_for_x = f"Brak danych dla roku {year} oraz broni: {weapons[0]}"
        self.result_model.t_welch_message, self.result_model.t_welch_p_value = self.__t_welch_test(x, y)
