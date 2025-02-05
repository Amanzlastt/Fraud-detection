import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class DataPreprocessing:
    def __init__(self, data):
        self.data = data
    def to_date(self,column_list):
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