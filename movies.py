# -*- coding: utf-8 -*-
"""Untitled16.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Rs9qYuGJe4SX22Nb2xitcdk8Ud5YZxJZ
"""

pip install scikit-learn==1.2.2

# Commented out IPython magic to ensure Python compatibility.
!pip install category encoders

import warnings
warnings.filterwarnings('ignore')

import category_encoders as ce
# import dtale
import lightgbm as lgb
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pickle
import seaborn as sns
import statsmodels.api as sm
import statsmodels.regression.linear_model as smf
import timeit
import xgboost as xgb

from imblearn.over_sampling import RandomOverSampler
from numba import jit, cuda
# from pandas_profiling import ProfileReport
# from pycaret.classification import *
# from pycaret.regression import *
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, Ridge
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from statsmodels.formula.api import ols
from statsmodels.regression.linear_model import OLS
from statsmodels.stats.outliers_influence import variance_inflation_factor
from wordcloud import WordCloud

sns.set()
# %matplotlib inline

pip install category-encoders

!unzip -q "/content/drive/MyDrive/archive.zip"

df = pd.read_csv("IMDb Movies India.csv", encoding = 'latin-1')
df.head()

df.info()

df.describe()

df.duplicated().sum()

rest_df, test_df = [x for y, x in movies_df.groupby(movies_df['Rating'].isna())]

test_df.head()

rest_df.head()

train_df, validation_df = train_test_split(rest_df, train_size = 0.8, random_state = 101)
train_df.head(2)

validation_df.head(2)

train_df.duplicated().sum()

validation_df.duplicated().sum()

test_df.duplicated().sum()

test_df[movies_df.duplicated(keep = False)]

test_df.drop_duplicates(inplace = True)
test_df.duplicated().sum()

train_df.info()

train_df.describe()

train_df.describe(include = 'all')

validation_df.info()

validation_df.describe()

validation_df.describe(include = 'all')

test_df.info()

train_missing = list(train_df.isnull().sum())
val_missing = list(validation_df.isnull().sum())
test_misisng = list(test_df.isnull().sum())

train_missing_percent = list(train_df.isnull().sum() / len(train_df) * 100)
val_missing_percent = list(validation_df.isnull().sum() / len(validation_df) * 100)
test_misisng_percent = list(test_df.isnull().sum() / len(test_df) * 100)

sns.displot(train_df.isnull())
plt.title("Missing values in training dataset")
plt.show()

sns.displot(validation_df.isnull())
plt.title("Missing values in validation dataset")
plt.show()

sns.displot(validation_df.isnull())
plt.title("Missing values in test dataset")
plt.show()

sns.heatmap(train_df.isnull(), cmap = 'viridis')
plt.title("Missing values in training dataset")
plt.show()

sns.heatmap(validation_df.isnull(), cmap = 'viridis')
plt.title("Missing values in validation dataset")
plt.show()

sns.heatmap(validation_df.isnull(), cmap = 'viridis')
plt.title("Missing values in test dataset")
plt.show()

missing_df = pd.DataFrame({'Columns' : list(train_df.columns), 'Train_missing' : train_missing, 'Percent_Train_missing' : train_missing_percent,
                'Validation_missing' : val_missing, 'Percent_Val_missing' : val_missing_percent, 'Test_missing' : test_misisng,
                           'Percent_Test_missing' : test_misisng_percent})
missing_df

train_df['Year'] = train_df['Year'].str.extract('([0-9]+)').astype(int)
train_df.head(2)

validation_df['Year'] = validation_df['Year'].str.extract('([0-9]+)').astype(int)
validation_df.head(2)

test_df['Year'] = test_df['Year'].str.replace(r'[()]', '', regex=True)
test_df.head(2)

sns.distplot(train_df['Year'].values, label = "Train")
sns.distplot(validation_df['Year'].values, label = "Validation")
sns.distplot(test_df['Year'].values, label = "Test")
plt.legend(['Train', 'Train', 'Validation', 'Validation', 'Test', 'Test'])
plt.xlabel('Year')

plt.show()

mode_year = train_df['Year'].mode()
test_df['Year'] = test_df['Year'].fillna(2019)

test_df['Year'].info()

sns.distplot(train_df['Year'].values, label = "Train")
sns.distplot(validation_df['Year'].values, label = "Validation")
sns.distplot(test_df['Year'].values, label = "Test")
plt.legend(['Train', 'Train', 'Validation', 'Validation', 'Test', 'Test'])
plt.xlabel('Year')

plt.show()

train_df['Duration'] = train_df['Duration'].str.extract('([0-9]+)').astype(float)
train_df.head(2)

validation_df['Duration'] = validation_df['Duration'].str.extract('([0-9]+)').astype(float)
validation_df.head(2)

test_df['Duration'] = test_df['Duration'].str.extract('([0-9]+)').astype(float)
test_df.head(2)

sns.distplot(train_df['Duration'].values, label = "Duration")
sns.distplot(validation_df['Duration'].values, label = "Validation")
sns.distplot(test_df['Duration'].values, label = "Test")
plt.legend(['Train', 'Train', 'Validation', 'Validation', 'Test', 'Test'])
plt.xlabel('Duration')

plt.show()

plt.figure(figsize = (10, 5))
plt.subplot(1, 2, 1)
sns.boxplot(train_df['Duration'].values)

plt.subplot(1, 2, 2)
sns.boxenplot(train_df['Duration'].values)

plt.show()

median_duration = train_df['Duration'].median()

train_df['Duration'] = train_df['Duration'].fillna(median_duration)
validation_df['Duration'] = validation_df['Duration'].fillna(median_duration)
test_df['Duration'] = test_df['Duration'].fillna(median_duration)

train_df['Duration'].info()

sns.distplot(train_df['Duration'].values, label = "Duration")
sns.distplot(validation_df['Duration'].values, label = "Validation")
sns.distplot(test_df['Duration'].values, label = "Test")
plt.legend(['Train', 'Train', 'Validation', 'Validation', 'Test', 'Test'])
plt.xlabel('Duration')

plt.show()

def expand_genre(df):
    genres_df = df['Genre'].str.split(', ', expand = True)
    df = pd.concat([df, genres_df], axis = 1)
    df.rename(columns = {0 : 'Genre_1', 1 : 'Genre_2', 2 : 'Genre_3'}, inplace = True)
    df.drop('Genre', axis = 1, inplace = True)
    return df

train_df = expand_genre(train_df)
validation_df = expand_genre(validation_df)
test_df = expand_genre(test_df)

print("Train Genre_1 missing :", (train_df['Genre_1'].isnull().sum() / len(train_df['Genre_1']) * 100))
print("Train Genre_2 missing :", (train_df['Genre_2'].isnull().sum() / len(train_df['Genre_2']) * 100))
print("Train Genre_3 missing :", (train_df['Genre_3'].isnull().sum() / len(train_df['Genre_3']) * 100))
print("Validation Genre_1 missing :", (validation_df['Genre_1'].isnull().sum() / len(validation_df['Genre_1']) * 100))
print("Validation Genre_2 missing :", (validation_df['Genre_2'].isnull().sum() / len(validation_df['Genre_2']) * 100))
print("Validation Genre_3 missing :", (validation_df['Genre_3'].isnull().sum() / len(validation_df['Genre_3']) * 100))
print("Test Genre_1 missing :", (test_df['Genre_1'].isnull().sum() / len(test_df['Genre_1']) * 100))
print("Test Genre_2 missing :", (test_df['Genre_2'].isnull().sum() / len(test_df['Genre_2']) * 100))
print("Test Genre_3 missing :", (test_df['Genre_3'].isnull().sum() / len(test_df['Genre_3']) * 100))

def drop_genre(df):
    df.drop(['Genre_2','Genre_3'], axis = 1, inplace = True)
    df.rename(columns = {'Genre_1' : 'Genre'}, inplace = True)
    return df

train_df = drop_genre(train_df)
validation_df = drop_genre(validation_df)
test_df = drop_genre(test_df)

mode_per_year = train_df.groupby('Year')['Genre'].apply(lambda x: x.mode().iloc[0])    # Gives a df with node of each year
train_df['Genre'] = train_df.apply(lambda row: mode_per_year[row['Year']] if pd.isnull(row['Genre']) else row['Genre'], axis=1)
train_df.info()

validation_df['Genre'] = validation_df.apply(lambda row: mode_per_year[row['Year']] if pd.isnull(row['Genre']) else row['Genre'], axis=1)
validation_df.info()

genre_mode = train_df['Genre'].mode()
genre_mode

test_df['Genre'] = test_df['Genre'].fillna('Drama')
test_df.info()

set(test_df['Votes'].tolist())

test_df.index[test_df['Votes'] == '$5.11M']

test_df['Votes'][9500] = pd.NA

def fill_names(df):
    df['Director'] = df['Director'].fillna('Not Available')
    df['Actor 1'] = df['Actor 1'].fillna('Not Available')
    df['Actor 2'] = df['Actor 2'].fillna('Not Available')
    df['Actor 3'] = df['Actor 3'].fillna('Not Available')
    return df

train_df = fill_names(train_df)
validation_df = fill_names(validation_df)
test_df = fill_names(test_df)

train_df.info()

train_missing = list(train_df.isnull().sum())
val_missing = list(validation_df.isnull().sum())
test_misisng = list(test_df.isnull().sum())

train_missing_percent = list(train_df.isnull().sum() / len(train_df) * 100)
val_missing_percent = list(validation_df.isnull().sum() / len(validation_df) * 100)
test_misisng_percent = list(test_df.isnull().sum() / len(test_df) * 100)

missing_df = pd.DataFrame({'Columns' : list(train_df.columns), 'Train_missing' : train_missing, 'Percent_Train_missing' : train_missing_percent,
                'Validation_missing' : val_missing, 'Percent_Val_missing' : val_missing_percent, 'Test_missing' : test_misisng,
                           'Percent_Test_missing' : test_misisng_percent})
missing_df

filled_df = pd.concat([train_df, validation_df], axis = 0)
filled_df.head(2)

filled_df['Votes'] = filled_df['Votes'].str.replace(',','').astype(int)
train_df['Votes'] = train_df['Votes'].str.replace(',','').astype(int)
validation_df['Votes'] = validation_df['Votes'].str.replace(',','').astype(int)

sns.scatterplot(x = filled_df['Rating'], y = filled_df['Votes'])
plt.show()

numeric_cols = filled_df.select_dtypes(include = np.number)
col_names = list(numeric_cols.columns)
col_index = 0
plt_rows = 2
plt_cols = 2

fig, ax = plt.subplots(nrows = plt_rows, ncols = plt_cols, figsize = (10, 10))

for row_count in range(plt_rows):
    for col_count in range(plt_cols):
        ax[row_count][col_count].scatter(x = filled_df[col_names[col_index]], y = filled_df['Rating'], c = ['b'])
        ax[row_count][col_count].set_ylabel(col_names[col_index])
        col_index += 1

sns.pairplot(filled_df)

col_index = 0

fig, ax = plt.subplots(nrows = plt_rows, ncols = plt_cols, figsize = (10, 10))

for row_count in range(plt_rows):
    for col_count in range(plt_cols):
        ax[row_count][col_count].hist(filled_df[col_names[col_index]])
        ax[row_count][col_count].set_ylabel(col_names[col_index])
        col_index += 1

def top_ten(col):
    filled_df[col].value_counts().sort_values(ascending = False)[:10].plot(kind = "bar")
    plt.title("Top Ten {}s".format(col))
    plt.xlabel(col)
    plt.ylabel("Count")
    plt.show()

def word_map(col):
    text_data = ' '.join(filled_df[col])
    wordcloud = WordCloud(width = 800, height = 400, background_color = 'black').generate(text_data)
    plt.figure(figsize = (10,5))
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis('off')
    plt.show()
top_ten("Name")

top_ten("Year")

top_ten("Director")

top_ten("Actor 1")

top_ten("Actor 2")

top_ten("Actor 3")

top_ten("Genre")

filled_df.head(2)

def rating_per(col, color):
    avg_rating = filled_df.groupby(col)['Rating'].mean().reset_index()
    plt.figure(figsize = (10, 6))
    plt.bar(avg_rating[col], avg_rating['Rating'], color = color)
    plt.title('{}-wise Ratings'.format(col))
    plt.xlabel(col)
    plt.ylabel('Rating')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

rating_per('Year', 'skyblue')

rating_per('Duration', 'black')

rating_per('Votes', 'white')

def top_rated(col):
    avg_rating = filled_df.groupby(col)['Rating'].mean().reset_index()
    top20 = avg_rating.sort_values(by='Rating', ascending=False).head(20)[col]
    top20_df = filled_df[filled_df[col].isin(top20)]
    sorted_top20_df = top20_df.sort_values(by = 'Rating', ascending = False)
    plt.figure(figsize = (12, 8))
    sns.violinplot(x = 'Rating', y = col, data = sorted_top20_df, palette = 'muted')
    plt.title('{}-wise Rating Distribution'.format(col))
    plt.xlabel(col)
    plt.ylabel('Rating')
    plt.show()

top_rated('Director')

top_rated('Genre')

top_movies_overall = filled_df.nlargest(10, 'Rating')

# Find the top 10 movies per year
top_movies_per_year = filled_df.groupby('Year').apply(lambda x: x.nlargest(10, 'Rating')).reset_index(drop=True)

plt.figure(figsize=(12, 6))
sns.scatterplot(x = 'Year', y = 'Rating', size = 'Votes', data = top_movies_overall, hue = 'Name', sizes = (50, 500), palette = 'viridis', alpha = 0.7)
plt.title('Top 10 Movies Overall (Bubble Chart)')
plt.xlabel('Year')
plt.ylabel('Rating')
plt.legend(bbox_to_anchor = (1, 1), loc = 'upper left', title = 'Movie Title')
plt.show()

mean_rating_per_year = filled_df.groupby('Year')['Rating'].mean().reset_index()

# Merge the mean popularity back into the original dataframe
mean_rated_df = pd.merge(filled_df, mean_rating_per_year, on = 'Year', suffixes=('', '_mean'))

# Use the mean popularity as the threshold
mean_rated_df['IsPopular_Rating'] = mean_rated_df['Rating'] > mean_rated_df['Rating_mean']

# Count the number of popular movies released each year
popular_rated_movies_count = mean_rated_df[mean_rated_df['IsPopular_Rating']].groupby('Year').size().reset_index(name = 'Number of Popular Movies (Rated)')

# Visualize the number of popular movies released each year using a line chart
plt.figure(figsize=(12, 6))
sns.lineplot(x='Year', y='Number of Popular Movies (Rated)', data=popular_rated_movies_count, marker='o', color='b')
plt.title('Number of Popular Movies Released Each Year (Threshold: Mean Rating per year)')
plt.xlabel('Year')
plt.ylabel('Number of Popular Movies')
plt.grid(True)
plt.show()

mean_votes_per_year = filled_df.groupby('Year')['Votes'].mean().reset_index()

# Merge the mean popularity back into the original dataframe
mean_voted_df = pd.merge(filled_df, mean_votes_per_year, on = 'Year', suffixes=('', '_mean'))

# Use the mean popularity as the threshold
mean_voted_df['IsPopular_Voting'] = mean_voted_df['Votes'] > mean_voted_df['Votes_mean']

# Count the number of popular movies released each year
popular_voted_movies_count = mean_voted_df[mean_voted_df['IsPopular_Voting']].groupby('Year').size().reset_index(name = 'Number of Popular Movies (Voted)')

# Visualize the number of popular movies released each year using a line chart
plt.figure(figsize=(12, 6))
sns.lineplot(x='Year', y='Number of Popular Movies (Voted)', data=popular_voted_movies_count, marker='o', color='r')
plt.title('Number of Popular Movies Released Each Year (Threshold: Mean Voting per year)')
plt.xlabel('Year')
plt.ylabel('Number of Popular Movies')
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 6))
sns.lineplot(x='Year', y='Number of Popular Movies (Voted)', data=popular_voted_movies_count, marker='o', color='r')
sns.lineplot(x='Year', y='Number of Popular Movies (Rated)', data=popular_rated_movies_count, marker='o', color='b')
plt.title('Number of Popular Movies Released Each Year (Threshold: Mean Rating/Voting per year)')
plt.xlabel('Year')
plt.ylabel('Number of Popular Movies')
plt.grid(True)
plt.show()

max_rating_per_year = filled_df.groupby('Year')['Rating'].max().reset_index()

# Merge the maximum rating back into the original dataframe
max_rated_df = pd.merge(filled_df, max_rating_per_year, on='Year', suffixes=('', '_max'))

# Count the number of votes for movies that performed better in rating each year
better_movies_votes_per_year = max_rated_df[max_rated_df['Rating'] == max_rated_df['Rating_max']].groupby('Year')['Votes'].sum().reset_index(name = 'Total Votes').sort_values(by = 'Year')

# Count the number of votes for movies that performed better in rating overall
better_movies_votes_overall = max_rated_df[max_rated_df['Rating'] == max_rated_df['Rating_max']].groupby('Name')['Votes'].sum().reset_index(name = 'Total Votes').sort_values(by = 'Total Votes', ascending = False)

plt.figure(figsize = (12, 6))
sns.lineplot(x = 'Year', y = 'Total Votes', data = better_movies_votes_per_year, color = 'green')
plt.title('Number of Votes for Top-Rated Movies per Year')
plt.ylabel('Total Votes')
plt.xlabel('Year')
plt.xlim(left = min(filled_df['Year']), right = 2025)
plt.show()

plt.figure(figsize = (12, 20))
sns.barplot(y = 'Name', x = 'Total Votes', data = better_movies_votes_overall, palette = 'viridis')
plt.title('Number of Votes for Top-Rated Movies Overall')
plt.ylabel('Movie Title')
plt.xlabel('Total Votes')
plt.show()

