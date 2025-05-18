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
        self.avg_shipping = self.shipping_time()
        self.ship_modes = self.shipping_by_mode()
        self.orders_per_segment = self.orders_per_segment()
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
        return self.df['Shipping_Time'].describe()

    def shipping_by_mode(self):
        """
        Group data by Ship Mode
        :return: DataFrame with Ship Mode and avg
        """
        modes = self.df.groupby('Ship_Mode')['Shipping_Time'].mean().sort_values()
        #https: // stackoverflow.com / questions / 10373660 / converting - a - pandas - groupby - multiindex - output -from-series - back - to - dataframe
        return modes.reset_index()

    def orders_per_segment(self):
        count = self.df['Segment'].value_counts()
        return count.reset_index()

csv_file = os.path.join('data','superstore_final_dataset (1).csv')

data = DataFrame(csv_file)
