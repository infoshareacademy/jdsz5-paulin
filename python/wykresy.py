#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp 
import seaborn as sns
import itertools
import scipy.stats as ssp
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns

import scipy.stats as st
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import squarify 
df = pd.read_csv('globalterrorismdb_0718dist.csv', encoding="ISO-8859-1", low_memory=False)

df2=df[['iyear','imonth','iday','country_txt','region_txt','city','attacktype1_txt','targtype1_txt','weaptype1_txt','nkill','natlty1_txt']]


# In[13]:


df3 = df.loc[df["region_txt"].str.contains("Europe", case=False)]
targets = df3.groupby(["iyear"]).count()['nkill'].reset_index()
targets.plot(kind='bar',x='iyear',y='nkill')
plt.show()


# In[50]:


# If you have 2 lists
df3 = df2.loc[df["region_txt"].str.contains("Africa", case=False)]
targets = df3.groupby(["iyear"]).count()['nkill'].reset_index()
squarify.plot(sizes=targets['nkill'], label=targets["iyear"],alpha=0.4)
plt.axis('off')
plt.show()


# In[54]:


# If you have 2 lists
targets = df2.groupby(["region_txt"]).count()['nkill'].reset_index()
squarify.plot(sizes=targets['nkill'], label=targets["region_txt"],alpha=0.2)
plt.axis('off')
plt.show()

