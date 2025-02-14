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
    # from data_preprocessing import DataPreprocessing
    from feature_enginerring import FeatureEnginerring
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

# data_processing = DataPreprocessing()




df_fraud = pd.read_csv('C:\\Users\\Aman\\Desktop\\kifyaw8-9\\data\\raw\\Fraud_Data.csv')
# df_country_code = pd.read_csv('C:\\Users\\Aman\\Desktop\\kifyaw8-9\\data\\raw\\IpAddress_to_Country.csv')


# %%



# %%
preprocesser = ColumnTransformer([
    ('scaler', StandardScaler(),['purchase_value', 'age', 'time_diff', 'transaction_frequency', 
                    'avg_transaction_velocity', 'hour_of_day', 'day_of_week', 'country']),
    ('onehot', OneHotEncoder(handle_unknown='infrequent_if_exist', sparse_output=False), ['browser','source'])

])

ran_for = Pipeline([
    ('feature_adder', FunctionTransformer(FeatureEnginerring.feature_enginerring, validate=False)),
    ('preprocessor', preprocesser,),
    ('model', RandomForestClassifier(n_estimators=30, max_depth=2))
])

grad_boost = Pipeline([
    ('feature_adder', FunctionTransformer(FeatureEnginerring.feature_enginerring, validate=False)),
    ('preprocessor', preprocesser,),
    ('model', GradientBoostingClassifier(n_estimators=10, n_iter_no_change=10))
])


# %%
x = df_fraud.drop('class', axis=1)
y = df_fraud['class']

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2)

# ran_for.fit(x_train,y_train)

# %%
grad_boost.fit(x_train, y_train)


# %%
# y_pred = pipeline.predict(x_test)
# from sklearn.metrics import accuracy_score
# accu_score = accuracy_score(y_test, y_pred)
# accu_score 

# # %%
# y_pred_gbc =  pipeline2.predict(x_test)
# gbc_score = accuracy_score(y_test, y_pred_gbc)
# gbc_score

# %%
import joblib
import pickle
import json

# joblib.dump(ran_for,'random_forest_calssifier.pkl')
joblib.dump(grad_boost,'gradient_boosring_classifier.joblib')


