import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import numpy as np
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col=0)

# Clean data
df = df[df.value.between(np.percentile(df.value, 2.5), np.percentile(df.value, 97.5))]


def draw_line_plot():
  # Draw line plot
  fig, ax = plt.subplots(figsize=(19, 7))
  df.plot(y='value', use_index=True, ax=ax, color='r', title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
  ax.xaxis.set_label_text('Date')
  ax.yaxis.set_label_text('Page Views')

  # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig

def draw_bar_plot():

  # Copy and modify data for monthly bar plot
  months=  ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
  df_bar = pd.DataFrame([[df.reset_index()[df.reset_index().date.astype(str).str.contains(f"201{j}-{'0' + str(i) if len(str(i))==1 else i}")].value.mean() for i in range(1,13)] for j in range(6,10)], columns=months, index=['2016', '2017', '2018', '2019'])
  
  # Draw bar plot
  fig, ax = plt.subplots(figsize=(15,10))
  df_bar.plot.bar(ax=ax)
  ax.xaxis.set_label_text('Years')
  ax.yaxis.set_label_text('Average Page Views')
  plt.legend(title='Months')

  # Save image and return fig (don't change this part)
  fig.savefig('bar_plot.png')
  return fig

# just discovored that i could convert it into datetime format
df = pd.read_csv('fcc-forum-pageviews.csv', index_col=0, parse_dates=[0])

df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_box_plot():

  # Prepare data for box plots (this part is done!)
  df_box = df.copy()
  df_box.reset_index(inplace=True)
  df_box['year'] = [d.year for d in df_box.date]
  df_box['month'] = [d.strftime('%b') for d in df_box.date]
  # to start boxplot from january
  df_box.sort_values(by=['year','date'], ascending=[False, True], inplace=True)
  # Draw box plots (using Seaborn)
  fig, ax = plt.subplots(1,2, figsize=(18, 7))
  box_1 = sns.boxplot(x='year', y='value', data=df_box, ax=ax[0])
  box_2 = sns.boxplot(x='month', y='value', data=df_box, ax=ax[1])
  box_1.axes.set_title('Year-wise Box Plot (Trend)')
  box_2.axes.set_title('Month-wise Box Plot (Seasonality)')
  ax[0].xaxis.set_label_text('Year')
  ax[0].yaxis.set_label_text('Page Views')
  ax[1].xaxis.set_label_text('Year')
  ax[1].yaxis.set_label_text('Page Views')
  ax[0].set(ylim=(0,200000))
  ax[1].set(ylim=(0,200000))

  # Save image and return fig (don't change this part)
  fig.savefig('box_plot.png')
  return fig
