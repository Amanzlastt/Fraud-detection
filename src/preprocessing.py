import pandas as pd 
import numpy as np

import sys
import os

path= "C:\\Users\\Aman\\Desktop\\kifyaw8-9\\src"
sys.path.append(os.path.abspath(path=path))

from data_preprocessing import DataPreprocessing


df_Fraud = pd.read_csv('C:\\Users\\Aman\\Desktop\\kifyaw8-9\\data\\raw\\Fraud_Data.csv')
df_IP = pd.read_csv('C:\\Users\\Aman\\Desktop\\kifyaw8-9\\data\\raw\\IpAddress_to_Country.csv')

data_processing = DataPreprocessing()
df_merged= data_processing.assign_country_code(df_Fraud,df_IP)


# Convert timestamps to datetime
df_merged['signup_time'] = pd.to_datetime(df_merged['signup_time'])
df_merged['purchase_time'] = pd.to_datetime(df_merged['purchase_time'])

# Calculate transaction frequency per user
transaction_frequency = df_merged.groupby('device_id').size().reset_index(name='transaction_frequency')

# Calculate transaction velocity (time between transactions)
df_merged = df_merged.sort_values(by=['device_id', 'purchase_time'])  # Sort by user and purchase time
df_merged['time_diff'] = df_merged.groupby('device_id')['purchase_time'].diff().dt.total_seconds()  # Time difference in seconds

# Calculate average transaction velocity per user (transactions per second)
transaction_velocity = df_merged.groupby('device_id')['time_diff'].mean().reset_index(name='avg_transaction_velocity')

# Merge frequency and velocity into one DataFrame
user_transaction_stats = pd.merge(transaction_frequency, transaction_velocity, on='device_id', how='left')
user_transaction_stats['avg_transaction_velocity'].fillna(0,inplace=True)
df_merged['time_diff'].fillna(0, inplace=True)

# Merge user_transaction_stats with the original dataset
df_merged_stats = pd.merge(df_merged, user_transaction_stats, on='device_id', how='left')

# Substituting nan values in country columns with unidentified
df_merged_stats['country'].fillna('Unidentified', inplace=True)

# Extract hour of the day and day of the week
df_merged_stats['hour_of_day'] = df_merged_stats['purchase_time'].dt.hour
df_merged_stats['day_of_week'] = df_merged_stats['purchase_time'].dt.dayofweek  # Monday=0, Sunday=6

# Extract useful features
df_merged_stats['signup_hour'] = df_merged_stats['signup_time'].dt.hour
df_merged_stats['signup_day'] = df_merged_stats['signup_time'].dt.dayofweek


# encodeing device id with a hash encodeing
df_merged_stats['device_id'] = df_merged_stats['device_id'].apply(lambda x: hash(x) % 10)

from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder(sparse_output=False)
df_merged_stats['device_id'] = df_merged_stats['device_id'].apply(lambda x: hash(x) % 10)
df_merged_stats['source'] = encoder.fit_transform(df_merged_stats[['source']])

#  Target Encoding for browser
target_mean_browser = df_merged_stats.groupby('browser')['class'].mean()
df_merged_stats['browser'] = df_merged_stats['browser'].map(target_mean_browser)

df_merged_stats['sex'] = df_merged_stats['sex'].map({'M': 1, 'F':0})

# Target Encoding for country
target_mean_country = df_merged_stats.groupby('country')['class'].mean()
df_merged_stats['country'] = df_merged_stats['country'].map(target_mean_country)

from sklearn.preprocessing import StandardScaler

# Columns to scale
columns_to_scale = ['purchase_value', 'age', 'time_diff', 'transaction_frequency', 
                    'avg_transaction_velocity', 'hour_of_day', 'day_of_week', 
                    'browser', 'country']

# Initialize the scaler
scaler = StandardScaler()

# Fit and transform the data
df_merged_stats[columns_to_scale] = scaler.fit_transform(df_merged_stats[columns_to_scale])

# Saving the processed data
df_merged_stats.drop(['purchase_time','signup_time'], axis=1).to_csv("C:\\Users\\Aman\\Desktop\\kifyaw8-9\\data\\processed\\encoded_froud_data.csv", index=False)