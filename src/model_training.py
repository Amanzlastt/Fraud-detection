# %%
import warnings
warnings.filterwarnings('ignore')

# %%
import pandas as pd 

import sys
import os

path= "C:\\Users\\Aman\\Desktop\\kifyaw8-9\\src"
sys.path.append(os.path.abspath(path=path))

try:
    from data_preprocessing import DataPreprocessing
except:
    print("Import failure")

# %%
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,FunctionTransformer, OneHotEncoder
from sklearn.compose import ColumnTransformer

# %%

data_processing = DataPreprocessing()




df_fraud = pd.read_csv('C:\\Users\\Aman\\Desktop\\kifyaw8-9\\data\\raw\\Fraud_Data.csv')
# df_country_code = pd.read_csv('C:\\Users\\Aman\\Desktop\\kifyaw8-9\\data\\raw\\IpAddress_to_Country.csv')


# %%
def feature_enginerring(df_fraud):
    df = data_processing.assign_country_code(df_fraud)
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
    user_transaction_stats['avg_transaction_velocity'].fillna(0,inplace=True)
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


# %%
preprocesser = ColumnTransformer([
    ('scaler', StandardScaler(),['purchase_value', 'age', 'time_diff', 'transaction_frequency', 
                    'avg_transaction_velocity', 'hour_of_day', 'day_of_week', 'country']),
    ('onehot', OneHotEncoder(handle_unknown='infrequent_if_exist', sparse_output=False), ['browser','source'])

])

pipeline = Pipeline([
    ('feature_adder', FunctionTransformer(feature_enginerring, validate=False)),
    ('preprocessor', preprocesser,),
    ('model', RandomForestClassifier(n_estimators=30, max_depth=2))
])

pipeline2 = Pipeline([
    ('feature_adder', FunctionTransformer(feature_enginerring, validate=False)),
    ('preprocessor', preprocesser,),
    ('model', GradientBoostingClassifier(n_estimators=10, n_iter_no_change=10))
])


# %%
x = df_fraud.drop('class', axis=1)
y = df_fraud['class']

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2)

pipeline.fit(x_train,y_train)

# %%
pipeline2.fit(x_train, y_train)


# %%
y_pred = pipeline.predict(x_test)
from sklearn.metrics import accuracy_score
accu_score = accuracy_score(y_test, y_pred)
accu_score 

# %%
y_pred_gbc =  pipeline2.predict(x_test)
gbc_score = accuracy_score(y_test, y_pred_gbc)
gbc_score

# %%
# import joblib
# import pickle
# import json

# joblib.dump(pipeline,'random_forest_calssifier.pkl')
# joblib.dump(pipeline2,'gradient_boosring_classifier.pkl')


