# This file analyses the clean data and calculates the stats that are useful and needed. It does the calculations

import pandas as pd

class StockAnalyser:

    # A class that takes a clean DataFrame and calculates the statistics that are key

    def summarise(self, df: pd.DataFrame, ticker: str) -> dict:
        """
        Calculates a summary of key statistics for a stock
        Returns the results that are shown in a dictionary
        """

        # Get the closing prices as a list we can work with
        prices = df["close"]
        returns = df["daily_return"].dropna()  # If it's empty the first row is removed

        # Current price = the most recent closing price which is the last row
        current_price = prices.iloc[-1]

        # Price 30 days ago or the oldest available if it's less than 30 days
        if len(prices) >= 30:
            price_30d_ago = prices.iloc[-30]
        else:
            price_30d_ago = prices.iloc[0]

        # How much the price has changed over the last 30 days in percentage
        change_30d = ((current_price - price_30d_ago) / price_30d_ago) * 100

        # Highest and lowest price in the dataset
        period_high = prices.max()
        period_low = prices.min()

        # on average how much does it go up or down each day
        avg_daily_return = returns.mean()

        # the volatility is how much the price jumps from day to day. The higher the volatility the more risk
        # I used standard deviation to measure the spread
        volatility = returns.std()

        # The total volume traded
        avg_volume = df["volume"].mean()

        # Best single day and worst single day
        best_day = returns.max()
        worst_day = returns.min()

        # This counts how many days were down and how many were up so the profits
        up_days = (returns > 0).sum()
        down_days = (returns < 0).sum()
        win_rate = (up_days / len(returns)) * 100

        return {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "change_30d_pct": round(change_30d, 2),
            "period_high": round(period_high, 2),
            "period_low": round(period_low, 2),
            "avg_daily_return_pct": round(avg_daily_return, 3),
            "volatility_pct": round(volatility, 3),
            "avg_daily_volume": int(avg_volume),
            "best_day_pct": round(best_day, 2),
            "worst_day_pct": round(worst_day, 2),
            "up_days": int(up_days),
            "down_days": int(down_days),
            "win_rate_pct": round(win_rate, 1),
        }

    def compare(self, summaries: list) -> dict:
        """
        Compares multiple stocks and picks the best or the worst on key metrics.
        A list of summary dictionaries is shown and it's one per stock
        """

        if len(summaries) < 2:
            return {}  # Ive added this if statement (base case) because if there is no more than 1 stock then you can't compare

        def get_change(s):
            return s["change_30d_pct"]

        def get_volatility(s):
            return s["volatility_pct"]

        def get_win_rate(s):
            return s["win_rate_pct"]

        best_performer = max(summaries, key = get_change)
        most_volatile = max(summaries, key = get_volatility)
        most_stable = min(summaries, key = get_volatility)
        highest_win_rate = max(summaries, key = get_win_rate)

        return {
            "best_performer": best_performer["ticker"],
            "best_performer_return": best_performer["change_30d_pct"],
            "most_volatile": most_volatile["ticker"],
            "most_volatile_pct": most_volatile["volatility_pct"],
            "most_stable": most_stable["ticker"],
            "most_stable_pct": most_stable["volatility_pct"],
            "highest_win_rate": highest_win_rate["ticker"],
            "highest_win_rate_pct": highest_win_rate["win_rate_pct"],
        }
