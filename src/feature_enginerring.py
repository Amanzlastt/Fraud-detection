
import pandas as pd 

import sys
import os

path= "C:\\Users\\Aman\\Desktop\\kifyaw8-9\\src"
sys.path.append(os.path.abspath(path=path))

try:
    from data_preprocessing import DataPreprocessing
except:
    print("Import failure")

class FeatureEnginerring(DataPreprocessing):
    def feature_enginerring(df_fraud):
        df = DataPreprocessing.assign_country_code(df_fraud)
        # Convert timestamps to datetime
        df['signup_time'] = pd.to_datetime(df['signup_time'])
        df['purchase_time'] = pd.to_datetime(df['purchase_time'])

        # Calculate transaction frequency per user
        transaction_frequency = df.groupby('device_id').size().reset_index(name='transaction_frequency')

        # Calculate transaction velocity (time between transactions)
        df = df.sort_values(by=['device_id', 'purchase_time'])  # Sort by user and purchase time
        df['time_diff'] = df.groupby('device_id')['purchase_time'].diff().dt.total_seconds()  # Time difference in seconds

        # Calculate average transaction velocity per user (transactions per second)
        transaction_velocity = df.groupby('device_id')['time_diff'].mean().reset_index(name='avg_transaction_velocity')

        # Merge frequency and velocity into one DataFrame
        user_transaction_stats = pd.merge(transaction_frequency, transaction_velocity, on='device_id', how='left')
        user_transaction_stats['avg_transaction_velocity'] = user_transaction_stats['avg_transaction_velocity'].fillna(0)
        df['time_diff'].fillna(0, inplace=True)

        # Merge user_transaction_stats with the original dataset
        df_stats = pd.merge(df, user_transaction_stats, on='device_id', how='left')

        # Substituting nan values in country columns with unidentified
        df['country'].fillna('Unidentified', inplace=True)

        # Extract hour of the day and day of the week
        df_stats['hour_of_day'] = df_stats['purchase_time'].dt.hour
        df_stats['day_of_week'] = df_stats['purchase_time'].dt.dayofweek  # Monday=0, Sunday=6

        # Extract useful features
        df_stats['signup_hour'] = df_stats['signup_time'].dt.hour
        df_stats['signup_day'] = df_stats['signup_time'].dt.dayofweek

        # encodeing device id with a hash encodeing
        df_stats['device_id'] = df_stats['device_id'].apply(lambda x: hash(x) % 10)
        df_stats['country'] = df_stats['country'].apply(lambda x: hash(x) % 10)
        df_stats['sex'] = df_stats['sex'].map({'M': 1, 'F':0})

        return df_stats.drop(['purchase_time','signup_time'], axis=1)