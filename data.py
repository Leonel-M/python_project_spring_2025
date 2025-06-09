"""
data.py

Defines the SuperstoreData class responsible for loading and preprocessing
the sales dataset used in the dashboard.
"""

import pandas as pd

# https://stackoverflow.com/questions/66831999/how-to-import-csv-as-a-pandas-dataframe
import os

# Dictionary mapping U.S. state names to their standard two-letter postal abbreviations.
us_state_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}


def data_copy(old_obj, ship_value, segment_value, state_value, month_value, week_value):
    """
    Creates a filtered copy of a Data object based on selected filter values.
    :param old_obj: The original Data object to copy and filter.
    :param ship_value: Selected shipping modes.
    :param segment_value: Selected customer segments.
    :param state_value: Selected states.
    :param month_value: Selected order months.
    :param week_value: Selected weekdays.
    :return: A new Data object containing the filtered DataFrame and updated summaries.
    """
    if not hasattr(old_obj, "df") or old_obj.df is None or old_obj.df.empty:
        print("Empty original DataFrame. data_copy will return an empty Data.")
        return Data(old_obj.path)

    new_obj = Data()
    new_obj.df = old_obj.df.copy()
    df = new_obj.df

    # isin() in Pandas is used to check if the values of a column or DataFrame are present in a specified list, series or DataFrame.
    # return True or False
    if ship_value is not None and len(ship_value) > 0:
        df = df[df["Ship_Mode"].isin(ship_value)]
    if segment_value is not None and len(segment_value) > 0:
        df = df[df["Segment"].isin(segment_value)]
    if state_value is not None and len(state_value) > 0:
        df = df[df["State"].isin(state_value)]
    if month_value is not None and len(month_value) > 0:
        df = df[df["Order_Month"].isin(month_value)]
    if week_value is not None and len(week_value) > 0:
        df = df[df["Order_Weekday"].isin(week_value)]

    # Update the new object
    new_obj.df = df
    new_obj.avg_shipping_info = new_obj.shipping_time()
    new_obj.ship_modes_info = new_obj.shipping_by_mode()
    new_obj.orders_per_segment_info = new_obj.orders_per_segment()
    new_obj.orders_per_month_info = new_obj.orders_per_month()
    new_obj.orders_per_week_info = new_obj.orders_per_week()
    new_obj.orders_per_state_info = new_obj.orders_per_state()
    new_obj.orders_per_city_info = new_obj.orders_per_city()

    return new_obj


class Data:
    """
    Class to load and preprocess the Superstore dataset for analysis.
    """

    def __init__(self, in_path=None):
        """
        Initializes the data loader with the path to the CSV file.

        :Args: file_path (str): Relative path to the CSV file.
        """
        self.path = in_path
        self.df = self.get_data()
        if self.df is None or self.df.empty:
            print(
                "Data could not be loaded. The Data instance will have an empty DataFrame."
            )
            self.avg_shipping_info = None
            self.ship_modes_info = pd.DataFrame()
            self.orders_per_segment_info = pd.DataFrame()
            self.orders_per_month_info = pd.DataFrame()
            self.orders_per_week_info = pd.DataFrame()
            self.orders_per_state_info = pd.DataFrame()
            self.orders_per_city_info = pd.DataFrame()
            return
        self.df["Ship_Date"] = (
            (self.get_datetime("Ship_Date"))
            if ("Ship_Date" in self.df.columns)
            else pd.NA
        )
        self.df["Order_Date"] = (
            (self.get_datetime("Order_Date"))
            if ("Order_Date" in self.df.columns)
            else pd.NA
        )
        self.df["Shipping_Time"] = (
            self.df["Ship_Date"] - self.df["Order_Date"]
        ).dt.days
        self.avg_shipping_info = self.shipping_time()
        self.ship_modes_info = self.shipping_by_mode()
        self.orders_per_segment_info = self.orders_per_segment()
        self.df["Order_Month"] = self.df[
            "Order_Date"
        ].dt.month_name()  # https://stackoverflow.com/questions/74015822/how-to-extract-year-and-month-from-string-in-a-dataframe
        self.df["Order_Weekday"] = self.df["Order_Date"].dt.day_name()
        self.orders_per_month_info = self.orders_per_month()
        self.orders_per_week_info = self.orders_per_week()
        self.orders_per_state_info = self.orders_per_state()
        self.orders_per_city_info = self.orders_per_city()

    def get_data(self):
        """
        Read CSV file
        :return: DataFrame
        """
        try:
            df = pd.read_csv(
                csv_file, encoding="ISO-8859-1"
            )  # alternative encoding with special characters
            return df
        except FileNotFoundError:
            print(f'Error: CSV file not found in "{self.path}" ')
            return pd.DataFrame()  # Empty DataFrame
        except Exception as e:
            print(f'Error reading "{self.path}": {e}')
            return pd.DataFrame()  # Empty DataFrame

    def get_info(self):
        """
        Principal info about DataFrame
        :return:
        """
        print(self.df.info())

    def get_datetime(self, column):
        """
        Change to a readable date format
        :param column: Name of the column with dates
        :return: pandas datetime format
        """
        return pd.to_datetime(self.df[column], format="%d/%m/%Y")

    def shipping_time(self):
        """
        Generates descriptive statistics for the 'Shipping_Time' column.
        :return: pd.Series: Summary statistics including count, mean, std, min, max, and quartiles.
        """
        return self.df["Shipping_Time"].describe()

    def shipping_by_mode(self):
        """
        Group data by Ship Mode
        :return: DataFrame with Ship Mode and avg
        """
        modes = self.df.groupby("Ship_Mode")["Shipping_Time"].mean().sort_values()
        # https: // stackoverflow.com / questions / 10373660 / converting - a - pandas - groupby - multiindex - output -from-series - back - to - dataframe
        return modes.reset_index()

    def orders_per_segment(self):
        """
        :return: DataFrame with Client's Segments and Clients per Segment
        """
        count = self.df["Segment"].value_counts()
        return count.reset_index()

    def orders_per_month(self):
        """
        :return: Dataframe with Months and Orders per Month  (in calendar order)
        """
        df = self.df.copy()
        df["Order_Month"] = pd.Categorical(
            df[
                "Order_Month"
            ],  # https://stackoverflow.com/questions/72415001/how-to-sort-pandas-dataframe-by-month-name
            categories=[
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ],
            ordered=True,
        )
        count = (
            df.groupby("Order_Month", observed=True)
            .size()
            .reset_index(name="Order_Count")
        )
        return count.rename(
            columns={"Order_Month": "Month"}
        )  # https://docs.kanaries.net/es/topics/Pandas/pandas-rename-column

    def orders_per_week(self):
        """
        :return: Dataframe with Months and Orders per Weekday  (in calendar order)
        """
        df = self.df.copy()
        df["Order_Weekday"] = pd.Categorical(
            df[
                "Order_Weekday"
            ],  # https://stackoverflow.com/questions/72415001/how-to-sort-pandas-dataframe-by-month-name
            categories=[
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ],
            ordered=True,
        )
        count = (
            df.groupby("Order_Weekday", observed=True)
            .size()
            .reset_index(name="Order_Count")
        )
        return count.rename(
            columns={"Order_Weekday": "Weekday", "count": "Order_Count"}
        )

    def orders_per_state(self):
        """
        Calculates the number of orders per state.
        :return: DataFrame with states and order counts
        """
        count = self.df["State"].value_counts().reset_index()
        # https: // www.geeksforgeeks.org / python - map - function /
        count["State_Code"] = count["State"].map(us_state_abbrev)
        return count.rename(columns={"count": "Order_Count"})

    def orders_per_city(self):
        """
        Calculates the number of orders per city.
        :return: DataFrame with cities and order counts
        """
        count = self.df["City"].value_counts().reset_index()
        return count.rename(columns={"count": "Order_Count"})


csv_file = os.path.join("data", "superstore_final_dataset (1).csv")

data = Data(csv_file)

filtered = data_copy(data, None, None, None, None, None)
