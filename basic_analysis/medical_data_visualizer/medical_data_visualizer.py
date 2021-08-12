#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')
df


# In[2]:


df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2)).map(lambda r : 1 if r > 25 else 0)


# In[3]:


#normalizing data of cholesterol and gluc
def func(r):
    r[r == 1] = 0
    r[r > 1] = 1
    return r
df.loc[:, 'cholesterol': 'gluc'] = df.loc[:, 'cholesterol': 'gluc'].apply(func)


# ###  Draw Categorical Plot

# In[4]:


# Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active',  'overweight'])
df_cat


# In[5]:


# Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
df_cat = df_cat.groupby(['cardio', 'variable', 'value']).variable.count()
df_cat


# In[6]:


df_cat = df_cat.rename('total').reset_index()
df_cat


# In[7]:


# Draw the catplot with 'sns.catplot()'
fig = sns.catplot(x='variable', y='total', col='cardio', hue='value', data=df_cat, kind='bar')
plt.show()


# In[8]:


# Do not modify the next two lines
fig.savefig('catplot.png')


# ### Draw Heat Map

# In[9]:



# Clean the data
df_heat = df[(df['height'] >= df['height'].quantile(0.025)) & (df['ap_lo'] <= df['ap_hi']) & (df['height'] <= df['height'].quantile(0.975)) & (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))]
df_heat


# In[10]:


# Calculate the correlation matrix
corr = df_heat.corr()
corr


# In[11]:


# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr.corr()))
mask


# In[12]:


# Set up the matplotlib figure
fig, ax = plt.subplots(figsize=(15, 12))
# Draw the heatmap
sns.heatmap(corr, mask=mask, ax=ax, annot=True, fmt='.1f', vmax=0.32, vmin=-0.16, center=0, cbar_kws={'shrink': 0.5})
plt.show()


# In[13]:


# Do not modify the next two lines
fig.savefig('heatmap.png')

