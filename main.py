import pandas as pd
import yfinance as yf


def fetch_price_data(ticker, start_date, end_date):
    return yf.download(tickers=ticker, start=start_date, end=end_date)


def calculate_returns(df, periods):
    close = df["Close"]

    latest_date = close.index.max()
    latest_price = close.loc[latest_date]
    earliest_date = close.dropna().index.min()

    returns = {}

    for label, offset in periods.items():
        past_date = latest_date - offset

        if past_date < earliest_date:
            returns[label] = float("nan")
            continue

        past_price = close.asof(past_date)
        returns[label] = (latest_price / past_price - 1) * 100

    return pd.DataFrame(returns)


def main():
    ticker = "005930.KS"
    start_date = "2025-01-01"
    end_date = "2026-02-03"

    periods = {
        "1m": pd.DateOffset(months=1),
        "3m": pd.DateOffset(months=3),
        "6m": pd.DateOffset(months=6),
        "12m": pd.DateOffset(months=12),
    }

    df = fetch_price_data(ticker, start_date, end_date)
    returns_df = calculate_returns(df, periods)

    print("\n📈 Period Returns (%)")
    print("-" * 30)
    print(returns_df.round(2).to_string())
    print("-" * 30)


if __name__ == "__main__":
    main()
