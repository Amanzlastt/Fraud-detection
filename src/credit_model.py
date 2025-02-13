# %%
import pandas as pd 
import numpy as np

# %%
df_credit= pd.read_csv('C:\\Users\\Aman\\Desktop\\kifyaw8-9\\data\\raw\\creditcard.csv')
# df_credit.head()

# %%
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.compose import ColumnTransformer

# %%
columns = df_credit.columns[:-1]
preprocess = ColumnTransformer([
    ('scaler', StandardScaler(),columns)
])
log_reg = Pipeline([
    ('prepeocessor', preprocess),
    ('model', LogisticRegression())
])
dec_tre = Pipeline([
    ('prepeocessor', preprocess),
    ('model', DecisionTreeClassifier())
])


# %%
x = df_credit.drop('Class', axis=1)
y = df_credit['Class']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)


# %%
log_reg.fit(x_train, y_train)

# %%
dec_tre.fit(x_train, y_train)


# %%
# gra_bos.fit(x_train, y_train)

# %%
# ran_for.fit(x_train,y_train)

# %%
from sklearn.metrics import accuracy_score

score = accuracy_score()

# %%
log_reg.score(x_test, y_test)

# %%
dec_tre.score(x_test,y_test)

# %%
import joblib


joblib.dump(log_reg,'credit_logisticreg.pkl')
joblib.dump(dec_tre,'credit_decisiontree.pkl')


