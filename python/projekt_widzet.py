#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Zainstaluj poniższy pakiet
# pip install plotly==2.0.15
#
#   znajdź plik o nazwie .credentials (powinien być w katalogu C:\users\username\.plotly)
#   Do pliku wprowadź poniższe dane 
#    "username": "leszek.dorozynski",
#    "api_key": "9GzqplM8DFADoRImC3GW",
#    "proxy_username": "leszek.dorozynski",
#    "proxy_password": "leedo0273",
#    "stream_ids": [8tok67udzk]




#https://plotly.com/python/v3/gapminder-example/
import plotly.plotly as py
from plotly.grid_objs import Grid, Column
#from plotly.tools import FigureFactory as FF - oryginalna linijka
from plotly import figure_factory as FF # - po zmianie 

import pandas as pd
import time

url = 'gapminderDataFiveYear.csv'
dataset = pd.read_csv(url)

table = FF.create_table(dataset.head(10))
py.iplot(table, filename='animations-gapminder-data-preview')


# In[39]:


py.get_config()["plotly_domain"]


# In[42]:


years_from_col = set(dataset['year'])
years_ints = sorted(list(years_from_col))
years = [str(year) for year in years_ints]
years.remove('1957')

# make list of continents
continents = []
for continent in dataset['continent']:
    if continent not in continents:
        continents.append(continent)

columns = []
# make grid
for year in years:
    for continent in continents:
        dataset_by_year = dataset[dataset['year'] == int(year)]
        dataset_by_year_and_cont = dataset_by_year[dataset_by_year['continent'] == continent]
        for col_name in dataset_by_year_and_cont:
            # each column name is unique
            column_name = '{year}_{continent}_{header}_gapminder_grid'.format(
                year=year, continent=continent, header=col_name
            )
            a_column = Column(list(dataset_by_year_and_cont[col_name]), column_name)
            columns.append(a_column)

# upload grid
grid = Grid(columns)
url = py.grid_ops.upload(grid, 'gapminder_grid'+str(time.time()), auto_open=False)
url


# In[33]:


figure = {
    'data': [],
    'layout': {},
    'frames': [],
    'config': {'scrollzoom': True}
}

# fill in most of layout
figure['layout']['xaxis'] = {'range': [30, 85], 'title': 'Life Expectancy', 'gridcolor': '#FFFFFF'}
figure['layout']['yaxis'] = {'title': 'GDP per Capita', 'type': 'log', 'gridcolor': '#FFFFFF'}
figure['layout']['hovermode'] = 'closest'
figure['layout']['plot_bgcolor'] = 'rgb(223, 232, 243)'


# In[34]:


sliders_dict = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {'size': 20},
        'prefix': 'Year:',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {'duration': 300, 'easing': 'cubic-in-out'},
    'pad': {'b': 10, 't': 50},
    'len': 0.9,
    'x': 0.1,
    'y': 0,
    'steps': []
}


# In[35]:


figure['layout']['updatemenus'] = [
    {
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 500, 'redraw': False},
                         'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
                'label': 'Play',
                'method': 'animate'
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }
]

custom_colors = {
    'Asia': 'rgb(171, 99, 250)',
    'Europe': 'rgb(230, 99, 250)',
    'Africa': 'rgb(99, 110, 250)',
    'Americas': 'rgb(25, 211, 243)',
    'Oceania': 'rgb(50, 170, 255)'
}


# In[36]:


col_name_template = '{year}_{continent}_{header}_gapminder_grid'
year = 1952
for continent in continents:
    data_dict = {
        'xsrc': grid.get_column_reference(col_name_template.format(
            year=year, continent=continent, header='lifeExp'
        )),
        'ysrc': grid.get_column_reference(col_name_template.format(
            year=year, continent=continent, header='gdpPercap'
        )),
        'mode': 'markers',
        'textsrc': grid.get_column_reference(col_name_template.format(
            year=year, continent=continent, header='country'
        )),
        'marker': {
            'sizemode': 'area',
            'sizeref': 200000,
            'sizesrc': grid.get_column_reference(col_name_template.format(
                 year=year, continent=continent, header='pop'
            )),
            'color': custom_colors[continent]
        },
        'name': continent
    }
    figure['data'].append(data_dict)


# In[37]:


for year in years:
    frame = {'data': [], 'name': str(year)}
    for continent in continents:
        data_dict = {
            'xsrc': grid.get_column_reference(col_name_template.format(
                year=year, continent=continent, header='lifeExp'
            )),
            'ysrc': grid.get_column_reference(col_name_template.format(
                year=year, continent=continent, header='gdpPercap'
            )),
            'mode': 'markers',
            'textsrc': grid.get_column_reference(col_name_template.format(
                year=year, continent=continent, header='country'
                )),
            'marker': {
                'sizemode': 'area',
                'sizeref': 200000,
                'sizesrc': grid.get_column_reference(col_name_template.format(
                    year=year, continent=continent, header='pop'
                )),
                'color': custom_colors[continent]
            },
            'name': continent
        }
        frame['data'].append(data_dict)

    figure['frames'].append(frame)
    slider_step = {'args': [
        [year],
        {'frame': {'duration': 300, 'redraw': False},
         'mode': 'immediate',
       'transition': {'duration': 300}}
     ],
     'label': year,
     'method': 'animate'}
    sliders_dict['steps'].append(slider_step)

figure['layout']['sliders'] = [sliders_dict]


# In[3]:


py.icreate_animations(figure, 'gapminder_example'+str(time.time()))


# In[13]:


#%matplotlib notebook
from ipywidgets import *
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
line, = ax.plot(x, np.sin(x))

def update(w = 1.0):
    line.set_ydata(np.sin(w * x))
    fig.canvas.draw_idle()

interact(update);


# In[38]:


import matplotlib.pyplot as plt
import numpy as np

data = 'gapminderDataFiveYear.csv'
df = pd.DataFrame(pd.read_csv(data))
df.mean(axis = 0)

df.plot(x='year',y='lifeExp',color='red')
plt.show()

# Data for plotting
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
ax.grid()

fig.savefig("test.png")
plt.show()

def update(w = 1.0):
    line.set_ydata(np.sin(w * x))
    fig.canvas.draw_idle()

interact(update);
df

