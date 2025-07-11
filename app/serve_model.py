# serve_model.py
from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import pandas as pd

import sys
import os

path= "C:\\Users\\Aman\\Desktop\\Fraud-detection\\src"
sys.path.append(os.path.abspath(path=path))

try:
    # from data_preprocessing import DataPreprocessing
    from feature_enginerring import FeatureEnginerring
    # print('import done')
except:
    print("Import failure")
# FeatureEngineering= FeatureEnginerring.feature_enginerring
# Load the trained model
with open("C:\\Users\\Aman\\Desktop\\Fraud-detection\\data\\models\\credit_logisticreg.joblib", "rb") as file:
    model = joblib.load(file)

# features used in training
FEATURES = ['user_id', 'signup_time', 'purchase_time', 'purchase_value',
       'device_id', 'source', 'browser', 'sex', 'age', 'ip_address']

# Initialize Flask app
app = Flask(__name__)

@app.route("/", methods=["GET", 'POST'])
def index():
    if request.method == "POST":
        try:
            # Get input values from form
            form_data = {feature: request.form[feature] for feature in FEATURES}
             # Convert datetime field correctly
            form_data["signup_time"] = pd.to_datetime(form_data["signup_time"])

            # Convert to DataFrame
            df = pd.DataFrame([form_data])

            # Ensure numeric columns are converted properly
            numeric_features = ['user_id',  'purchase_value', 'age', 'ip_address']
            df[numeric_features] = df[numeric_features].astype(float)
            
            # Make prediction
            prediction = model.predict(df)[0]

            # Return result
            return render_template("index.html", prediction=prediction)

        except Exception as e:
            return jsonify({"error": str(e)})

    return render_template("index.html", prediction=None)

if __name__ == "__main__":
    app.run(debug=True)
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()  # Get input data in JSON format
        features = np.array(data["features"]).reshape(1, -1)  # Convert to numpy array
        prediction = model.predict(features)  # Predict
        return jsonify({"prediction": int(prediction[0])})  # Return JSON response
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



