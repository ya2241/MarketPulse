# This file takes the raw messy data from the API and turns it into a clean table. So it basically cleans the data.

import pandas as pd  # pandas lets me work with tables of data

class DataProcessor:
    # A class that takes raw API data and cleans it into a usable pandas DataFrame.

    def process(self, raw_data: dict, ticker: str) -> pd.DataFrame:
        # Takes the raw dictionary from the API and returns a clean DataFrame.

        # The API returns the data nested inside the Time Series. That part is pulled out.
        time_series = raw_data["Time Series (Daily)"]

        # Converts the nested dictionary into a pandas DataFrame
        df = pd.DataFrame(time_series).T  # .T flips the rows and columns the right way

        # Renames the columns to something readable. The API gives  names like "1. open", "4. close" - that's fixed
        df.columns = ["open", "high", "low", "close", "volume"]

        # Converts all the values from strings to numbers
        df = df.astype(float)

        # Converts the row labels from strings to proper dates
        df.index = pd.to_datetime(df.index)

        # Sorts so that the oldest date is first and then the newest is last
        df = df.sort_index()

        # Added the ticker as a column so I know which stock this is
        df["ticker"] = ticker

        return df

    def process_multiple(self, raw_data_dict: dict) -> dict:
        # Processes lots of tickers at the same time at once.

        processed = {}

        for ticker, raw_data in raw_data_dict.items():
            try:
                processed[ticker] = self.process(raw_data, ticker)
                print(f"  ✓ {ticker} processed successfully")
            except KeyError as e:
                print(f"  ✗ {ticker} processing failed: missing key {e}")

        return processed

    def add_returns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds a daily_return column to the DataFrame. It's basically how much the price changed from one day to the next
        for example if the price went from 100 to 102, the daily return would be 2%
        """
        # pct_change() calculates the percentage change between each row
        df["daily_return"] = df["close"].pct_change() * 100
        return df

    def add_moving_average(self, df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
        #This adds a moving average column.

        column_name = f"ma_{window}"
        df[column_name] = df["close"].rolling(window=window).mean()
        return df
