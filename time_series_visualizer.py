import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import datetime

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=[0],index_col=[0])

# Clean data
df = df.loc[(df['value'] >= df['value'].quantile(.025)) 
          & (df['value'] <= df['value'].quantile(.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(18,6))  
    ax.plot(df.index.values, df.values, color='red')
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.legend() 

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["month"]= df_bar.index.month
    df_bar["year"]= df_bar.index.year
    df_bar_grouped = df_bar.groupby(["year","month"])["value"].mean().unstack()

    # Draw bar plot
    
    ax = df_bar_grouped.plot.bar(figsize=(14,5))
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(labels = [datetime.datetime.strptime(str(d), "%m").strftime("%B") for d in sorted(df_bar.index.month.unique())])

    fig = ax.get_figure()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['Year'] = [d.year for d in df_box.date]
    df_box['Month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(15, 5), sharey=True)

    axes[0] = sns.boxplot(ax=axes[0], data=df_box, x='Year', y='value')
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    
    axes[1] = sns.boxplot(ax=axes[1], data=df_box, x='Month', y='value',order=[ 'Jan','Feb', 'Mar', 'Apr','May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

