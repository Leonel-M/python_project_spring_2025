import pandas as pd
# https://stackoverflow.com/questions/66831999/how-to-import-csv-as-a-pandas-dataframe
import os

class DataFrame:
    def __init__(self, in_path):
        self.path = in_path
        self.df = self.get_data()
        self.df['Ship_Date'] = self.get_datetime('Ship_Date')
        self.df['Order_Date'] = self.get_datetime('Order_Date')
        self.df['Shipping_Time'] = (self.df['Ship_Date'] - self.df['Order_Date']).dt.days

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

    def get_datetime(self,column):
        """
        Change to a readable date format
        :param column: Name of the column with dates
        :return: pandas datetime format
        """
        return pd.to_datetime(self.df[column],format='%d/%m/%Y')

    def shipping_time(self):
        print(self.df['Shipping_Time'].describe())


csv_file = os.path.join('data','superstore_final_dataset (1).csv')

data = DataFrame(csv_file)

