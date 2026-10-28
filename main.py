# this file is where the program is run
import os
import sys
from fetcher import DataFetcher
from processor import DataProcessor
from analyser import StockAnalyser
from reporter import Reporter


# Get a free API key at https://www.alphavantage.co/support/#api-key
# Then replace the string below with your key
API_KEY = os.environ["ALPHA_VANTAGE_API_KEY"]

# The stocks you want to analyse
TICKERS = ["IBM"]

def run_pipeline(tickers: list, api_key: str):
     # Runs the full data pipeline from the fetch → process → analyse → report.

    reporter = Reporter()
    reporter.print_header()

    print("[ Step 1/4 ] Fetching data from API...")
    fetcher = DataFetcher(api_key=api_key)
    raw_data = fetcher.fetch_multiple(tickers)

    if not raw_data:
        print("No data fetched. Check your tickers and API key.")
        sys.exit(1)

    print()

    print("[ Step 2/4 ] Cleaning and processing data...")
    processor = DataProcessor()
    clean_data = processor.process_multiple(raw_data)

    # This adds extra columns for the daily returns and the 20 day moving average
    for ticker, df in clean_data.items():
        clean_data[ticker] = processor.add_returns(df)
        clean_data[ticker] = processor.add_moving_average(df, window=20)

    print()

    print("[ Step 3/4 ] Analysing data...")
    analyser = StockAnalyser()
    summaries = []

    for ticker, df in clean_data.items():
        summary = analyser.summarise(df, ticker)
        summaries.append(summary)
        print(f"  ✓ {ticker} analysed")

    # This compares stocks if more than one was requested
    comparison = analyser.compare(summaries) if len(summaries) > 1 else {}

    print()

    print("[ Step 4/4 ] Generating report...\n")

    for summary in summaries:
        reporter.print_stock_summary(summary)

    if comparison:
        reporter.print_comparison(comparison)

    reporter.print_footer(list(clean_data.keys()))

# This part only runs when you run this file directly
if __name__ == "__main__":

    # lets the tickers to be passed as command line arguments
    if len(sys.argv) > 1:
        tickers = [t.upper() for t in sys.argv[1:]]
    else:
        tickers = TICKERS

    run_pipeline(tickers=tickers, api_key=API_KEY)
