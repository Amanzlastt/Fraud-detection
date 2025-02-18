import pandas as pd 
from flask import Flask, jsonify


app = Flask(__name__)

df = pd.read_csv('C:\\Users\\Aman\\Desktop\\kifyaw8-9\\data\\raw\\Fraud_Data.csv')
df['signup_time'] = pd.to_datetime(df['signup_time'], errors='coerce')
df['signup_week'] = df['signup_time'].dt.isocalendar().week
df['device_id'] = df['device_id'].apply(lambda x: hash(x) % 10)

@app.route('/summary')
def summary():
    total_transactions = len(df)
    fraud_cases = df[df['class'] == 1].shape[0]
    fraud_percentage = round((fraud_cases / total_transactions) *100, 2)

    return jsonify({
        "total_transactions": total_transactions,
        "fraud_cases": fraud_cases,
        "fraud_percentage": fraud_percentage
    })

@app.route("/fraud_trends")
def fraud_trends():
    fraud_counts = df.groupby('signup_week')['class'].sum().reset_index()
    return fraud_counts.to_json(orient="records")

@app.route("/fraud_by_device")
def fraud_by_device():
    fraud_counts = df[df["class"] == 1]["device_id"].value_counts().reset_index()
    fraud_counts.columns = ["device_id", "class"]
    return fraud_counts.to_json(orient="records")

if __name__ == "__main__":
    app.run(debug=True)