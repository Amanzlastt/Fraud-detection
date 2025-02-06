import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class DataPreprocessing:
    def __init__(self):
        pass
    def to_date(self,column_list,data):
        self.data = data
        for column_name in column_list:
            self.data[column_name] = pd.to_datetime(self.data[column_name])
        return self.data
    def hist_plot(self,categorical_columns):
        fig, axes = plt.subplots(nrows=len(categorical_columns), ncols=1, figsize=(8, 4 * len(categorical_columns)))
        if len(categorical_columns) == 1:
            axes = [axes]
        for ax, col in zip(axes, categorical_columns):
            sns.countplot(x=self.data[col], ax=ax, palette="viridis")
            ax.set_title(f"Histogram of {col}")
            ax.set_xlabel(col)
            ax.set_ylabel("Count")

        plt.tight_layout()
        return plt
    
    def assign_country_code(self,df_Fraud, df_IP):
        country_list = []  # Store results

        for fraud_ip in df_Fraud['ip_address']:
            # Filter the correct country based on IP range
            match = df_IP.loc[(df_IP['lower_bound_ip_address'] <= fraud_ip) & 
                            (df_IP['upper_bound_ip_address'] >= fraud_ip), 'country']

            # Append the first matched country (if any), otherwise append None
            country_list.append(match.iloc[0] if not match.empty else None)

        df_Fraud['country'] = country_list  # Add new column to df_Fraud
        return df_Fraud
