# fetcher.py
# This is the data collector. So basically this is where the data stock is gotten from.

import requests

class DataFetcher:
    """
    A class that fetches stock data from the Alpha Vantage API.
    """
    def __init__(self, api_key: str):
        # when the stockfetcher class is created, an api key is given for it to use
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"  # the API's web address

    def fetch_daily_prices(self, ticker: str) -> dict:
        """
        Fetches the last 100 days of daily price data for a stock.
        Returns a dictionary (the raw data from the api).
        """
        # These are the parameters that is sent to the API
        params = {
            "function": "TIME_SERIES_DAILY",  # daily prices
            "symbol": ticker,                  # which stock
            "apikey": self.api_key,            # the key gotten from the vantage site
            "outputsize": "compact"            # compact = last 100 days only
        }

        print(f"  Fetching data for {ticker}...")

        # Send the request to the API and get the response back
        response = requests.get(self.base_url, params=params)

        # Check if something went wrong for example no ticker or no internet
        response.raise_for_status()  # raises an error if the request failed

        data = response.json()  # the response converted into a dictionary

        # If the API returns an error message it's raised
        if "Error Message" in data:
            raise ValueError(f"Invalid ticker '{ticker}'. Please check the symbol.")

        if "Note" in data:
            raise ValueError("API rate limit hit. Wait a minute and try again.")

        return data

    def fetch_multiple(self, tickers: list) -> dict:
        """
        Fetches the data for lots of tickers at the same time.
        Returns a dictionary where each key is a ticker and the value is its raw data.
        """
        results = {}

        for ticker in tickers:
            try:
                results[ticker] = self.fetch_daily_prices(ticker)
                print(f"  ✓ {ticker} fetched successfully")
            except ValueError as e:
                print(f"  ✗ {ticker} failed: {e}")

        return results
