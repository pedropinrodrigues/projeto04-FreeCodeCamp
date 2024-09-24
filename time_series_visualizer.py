import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import numpy as np
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
df = df[(df['value'] < df['value'].quantile(0.975)) & (df['value'] > df['value'].quantile(0.025))]


def draw_line_plot():
    fig = plt.figure(figsize=(13, 5))
    plt.plot(df.index, df['value'], label='line')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    df_bar_plot = df.copy()

    df_bar_plot['year'] = df_bar_plot.index.year
    df_bar_plot['month'] = df_bar_plot.index.month
    meses = df_bar_plot['month'].unique()
    anos = df_bar_plot['year'].unique()
    meses.sort()
    meses_str = ['January', 'February', 'March', 'April', 'May', 'June', 
                'July', 'August', 'September', 'October', 'November', 'December']


    meses_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 
                7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    for mes in meses:
        df_bar_plot['month'] = df_bar_plot['month'].replace(mes, meses_dict[mes])

    dados = {}

    for mes in meses_str:
        for ano in anos:
            valor = df_bar_plot[(df_bar_plot['month'] == mes) & (df_bar_plot['year'] == ano)]['value'].sum()
            
            if mes not in dados:
                dados[mes] = [valor]  
            else:
                dados[mes].append(valor) 


    x = np.arange(len(anos))  
    width = 0.05  
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in dados.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        multiplier += 1

    ax.set_xticks(x + width * (len(meses) - 1) / 2)  
    ax.set_xticklabels(anos)

    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('Sales Comparison by Year and Month')
    ax.legend(loc='upper left', ncols=4)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)       
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=month_order, ordered=True)

    fig, axis = plt.subplots(1, 2, figsize=(25, 10)) 

    sns.boxplot(x="year", y="value", data=df_box, ax=axis[0])
    axis[0].set_title('Year-wise Box Plot (Trend)', fontsize=20) 
    axis[0].set_xlabel('Year', fontsize=18)  
    axis[0].set_ylabel('Page Views', fontsize=18)  
    axis[0].tick_params(axis='both', which='major', labelsize=16)  
    axis[0].set_ylim(0, 200000)
    axis[0].set_yticks(np.arange(0, 200001, 20000))

    # Second subplot - Boxplot for months
    sns.boxplot(x="month", y="value", data=df_box, ax=axis[1])
    axis[1].set_title('Month-wise Box Plot (Seasonality)', fontsize=20)  
    axis[1].set_xlabel('Month', fontsize=18)  
    axis[1].set_ylabel('Page Views', fontsize=18)  
    axis[1].tick_params(axis='both', which='major', labelsize=16)  
    axis[1].set_ylim(0, 200000)
    axis[1].set_yticks(np.arange(0, 200001, 20000))

    # Adjust the layout
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
