# %% Imports
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.compose import ColumnTransformer

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# %% Load Data
df_credit = pd.read_csv('C:\\Users\\Aman\\Desktop\\Fraud-detection\\data\\raw\\creditcard.csv')

# %% Features and Target
x = df_credit.drop('Class', axis=1)
y = df_credit['Class']

# %% Train-test Split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# %% Preprocessing
columns = df_credit.columns[:-1]  # All columns except 'Class'
preprocess = ColumnTransformer([
    ('scaler', StandardScaler(), columns)
])

# %% Pipelines
log_reg = Pipeline([
    ('preprocessor', preprocess),
    ('model', LogisticRegression(class_weight='balanced', max_iter=1000))
])

dec_tre = Pipeline([
    ('preprocessor', preprocess),
    ('model', DecisionTreeClassifier(class_weight='balanced', random_state=42))
])

# %% Train Models
log_reg.fit(x_train, y_train)
dec_tre.fit(x_train, y_train)

# %% Evaluate Models
def evaluate_model(model, x_test, y_test, name="Model"):
    preds = model.predict(x_test)
    print(f"--- {name} ---")
    print("Accuracy :", accuracy_score(y_test, preds))
    print("Precision:", precision_score(y_test, preds))
    print("Recall   :", recall_score(y_test, preds))
    print("F1 Score :", f1_score(y_test, preds))
    print()

evaluate_model(log_reg, x_test, y_test, "Logistic Regression")
evaluate_model(dec_tre, x_test, y_test, "Decision Tree")

# %% Optional: Save models
import joblib
joblib.dump(log_reg, 'credit_logisticreg.joblib')
joblib.dump(dec_tre, 'credit_decisiontree.joblib')

# %%
