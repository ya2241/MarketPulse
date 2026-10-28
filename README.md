# MarketPulse

**A Python command-line stock analysis tool that retrieves daily market data, processes it, and produces readable performance summaries for one or more stocks.**

MarketPulse uses the [Alpha Vantage API](https://www.alphavantage.co/) to retrieve historical daily prices. It then cleans the data with Pandas, calculates performance statistics, and displays the results in the terminal. The project is organised as a modular data pipeline to separate data retrieval, processing, analysis, and reporting.

## Features

- **Market data retrieval:** Fetches up to 100 recent daily price records per ticker from Alpha Vantage.
- **Data processing:** Converts raw API responses into chronological Pandas DataFrames containing open, high, low, close, and volume data.
- **Performance analysis:** Calculates price change over approximately 30 trading observations, period high/low, average daily return, daily-return volatility, average trading volume, best/worst daily returns, and the proportion of positive-return days.
- **Moving average:** Computes a 20-day simple moving average as part of the processed dataset.
- **Stock comparison:** When multiple tickers are supplied, identifies the strongest recent performer, most and least volatile stocks, and highest positive-day rate.
- **Terminal reports:** Prints a formatted summary for each stock and an optional comparison section.

## Tech stack

- **Python** — application logic and command-line interface
- **Pandas** — data cleaning and statistical calculations
- **Requests** — API requests
- **Alpha Vantage API** — historical daily market data

## Getting started

### 1. Install dependencies

Use Python 3.11 and run the following from the project directory:

```bash
python -m pip install -r requirements.txt
```

### 2. Configure your API key securely

Get an API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key).

**Before running the project**, update `main.py` so it reads the key from an environment variable instead of the existing placeholder. Add `import os` alongside the other imports and replace the existing `API_KEY = ...` line with:

```python
API_KEY = os.environ["ALPHA_VANTAGE_API_KEY"]
```

Set the environment variable in the terminal where you plan to run the program:

**macOS / Linux:**

```bash
export ALPHA_VANTAGE_API_KEY="your-api-key"
```

**Windows PowerShell:**

```powershell
$env:ALPHA_VANTAGE_API_KEY="your-api-key"
```

**Never commit your real API key to GitHub.** The environment variable is set locally; it is not part of the repository.

### 3. Run the analysis

Analyse the default ticker (`IBM`):

```bash
python main.py
```

Analyse several stocks:

```bash
python main.py IBM AAPL MSFT
```

The program prints the metrics for each successfully processed ticker, followed by a comparison when more than one stock is analysed. API request limits may affect how many tickers you can fetch in one session.

## Project structure

```text
MarketPulse/
├── main.py           # Runs the data pipeline and reads ticker arguments
├── fetcher.py        # Retrieves stock data from Alpha Vantage
├── processor.py      # Cleans and enriches daily price data
├── analyser.py       # Calculates stock metrics and comparisons
├── reporter.py       # Prints formatted terminal reports
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

## How it works

1. **Fetch:** Requests daily stock prices for each ticker using the Alpha Vantage `TIME_SERIES_DAILY` endpoint.
2. **Process:** Converts API data into a date-sorted DataFrame and adds daily returns and a 20-day moving average.
3. **Analyse:** Produces a summary of recent price performance, return variability, trading volume, and positive/negative days; compares stocks when applicable.
4. **Report:** Displays the summaries and comparison results in the terminal.

## Potential improvements

- Add automated tests for data processing and financial calculations.
- Export analysis results to CSV.
- Introduce charts for price history and moving averages.
- Improve handling of API rate limits and missing data.

## Note

MarketPulse is an educational data analysis project, not an investment recommendation tool. The reported volatility is the standard deviation of daily percentage returns, not an annualised measure. The displayed “30 Day Change” is calculated using up to 30 available price observations rather than an exact 30-calendar-day window.
