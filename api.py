import pandas as pd
import json
# https://stackoverflow.com/questions/66831999/how-to-import-csv-as-a-pandas-dataframe
import os

class DataFrame:
    def __init__(self, in_path):
        self.path = in_path
        self.df = self.get_data()

    def get_data(self):
        """
        Read CSV file
        :return: DataFrame
        """
        df = pd.read_csv(csv_file, encoding='ISO-8859-1')  # alternative encoding with special characters
        return df

    def get_info(self):
        """
        Principal info about DataFrame
        :return:
        """
        print(self.df.info())


csv_file = os.path.join('data','superstore_final_dataset (1).csv')


data = DataFrame(csv_file)
print(data.df.head())