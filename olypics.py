# -*- coding: utf-8 -*-
"""olypics.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qvaeDekwIftfDrLoHuBPpQrTuNo5mfe8
"""



import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

import warnings
warnings.filterwarnings('ignore')

data = pd.read_excel('/content/olypics.xlsx')

data

data.info()

data.shape

data.columns

import matplotlib.pyplot as plt
import seaborn as sns

data['Throw'] = data['Throw'].astype(str).str.replace('m', '').astype(float)
data.info()

data.describe()

plt.figure(figsize=(10,6))
sns.histplot(data['Throw'], kde=True, bins=10)  # Use histplot for distribution of a single variable
plt.title('Distribution of Throw Distances')
plt.xlabel('Throw Distance (meter)')
plt.ylabel('Frequency')

mean_throw = data['Throw'].mean()
median_throw = data['Throw'].median() # Changed 'meadin' to 'median'
plt.axvline(mean_throw, color='r', linestyle='--', label=f'Mean: {mean_throw:.2f}')
plt.axvline(median_throw, color='g', linestyle='--', label=f'Median: {median_throw:.2f}')
plt.show()

plt.figure(figsize=(10,6))
sns.boxplot(data['Throw'])
plt.title('Box Plot of Throw Distances')
plt.xlabel('Throw Distance (meter)')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(10,6))
ax=sns.countplot(data['Competition'])
plt.title('Competition Distarbution')
plt.xlabel('Number of Throws')
plt.ylabel('Competition')

for p in ax.patches:
    ax.annotate(format(p.get_width(), '.0f'),
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center', va = 'center',
                xytext = (0, 10),
                textcoords = 'offset points')
plt.show()

data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%y') # Use the correct format string
data['Date'] = data['Date'].dt.strftime('%d-%m-%y')

data

highest_throw = data.loc[data['Throw'].idxmax()]
print(highest_throw)

smallest_throw = data.iloc[data['Throw'].idxmin()]
print(smallest_throw)

from statsmodels.tsa.arima.model import ARIMA
data_sorted = data.sort_values(by='Date')
data_sorted.set_index('Date', inplace=True)
data_sorted

data_sorted = data_sorted.drop('Competition',axis=1)
data_sorted

plt.figure(figsize=(10,6))
plt.plot(data_sorted.index, data_sorted['Throw'], marker='o', linestyle='-', label='Throw')
plt.xticks(rotation=45)

for x, y in zip(data_sorted.index, data_sorted['Throw']):
  plt.annotate(f'{y}', (x,y), textcoords='offset points', xytext=(0,10), ha='center')

plt.title('Throw Over Time')
plt.xlabel('Date')
plt.ylabel('Throw Distance')
plt.legend()
plt.show()

from sklearn.linear_model import LinearRegression
from datetime import datetime

data_sorted.index = pd.to_datetime(data_sorted.index)
data_sorted['Date_Ordinal'] = data_sorted.index.map(datetime.toordinal)
x=data_sorted['Date_Ordinal'].values.reshape(-1,1)
y=data_sorted['Throw']

model=LinearRegression()
model.fit(x,y)

LinearRegression()

data_sorted['Predicted_Throw'] = model.predict(x)
plt.figure(figsize=(10,6))
plt.plot(data_sorted.index, data_sorted['Throw'], marker='o', linestyle='-', label="Actual Throw")
plt.plot(data_sorted.index, data_sorted['Predicted_Throw'], marker='o', linestyle='-', label='Predicted_Throw')
plt.xticks(rotation=45)
plt.title('Actual vs Predicted Throw')
plt.xlabel('Date')
plt.ylabel('Throw Distance')
plt.legend()
plt.show()