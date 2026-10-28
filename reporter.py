from datetime import datetime

class Reporter:
    def print_header(self):
        print("================================")
        print("  MarketPulse - Stock Analysis  ")
        print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("================================")
        print()

    def print_stock_summary(self, summary):
        print(f"--- {summary['ticker']} ---")
        print(f"Current Price:     ${summary['current_price']}")
        print(f"30 Day Change:     {summary['change_30d_pct']}%")
        print(f"Period High:       ${summary['period_high']}")
        print(f"Period Low:        ${summary['period_low']}")
        print(f"Avg Daily Return:  {summary['avg_daily_return_pct']}%")
        print(f"Volatility:        {summary['volatility_pct']}%")
        print(f"Avg Daily Volume:  {summary['avg_daily_volume']:,}")
        print(f"Best Day:          +{summary['best_day_pct']}%")
        print(f"Worst Day:         {summary['worst_day_pct']}%")
        print(f"Up Days:           {summary['up_days']}")
        print(f"Down Days:         {summary['down_days']}")
        print(f"Win Rate:          {summary['win_rate_pct']}%")
        print()

    def print_comparison(self, comparison):
        if not comparison:
            return
        print("--- Comparison Summary ---")
        print(f"Best Performer:   {comparison['best_performer']} ({comparison['best_performer_return']:+.2f}%)")
        print(f"Most Volatile:    {comparison['most_volatile']} ({comparison['most_volatile_pct']}%)")
        print(f"Most Stable:      {comparison['most_stable']} ({comparison['most_stable_pct']}%)")
        print(f"Best Win Rate:    {comparison['highest_win_rate']} ({comparison['highest_win_rate_pct']}%)")
        print()

    def print_footer(self, tickers):
        print("================================")
        print(f"  Analysed: {', '.join(tickers)}")
        print(f"  Data source: Alpha Vantage API")
        print("================================")
