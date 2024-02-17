# By Tony Cowling & Jack Cowling & ChatGBT
# Get all "Stock Info" python script
# V2 will dump to db.

import yfinance as yf

def fetch_ticker_info(tickers):
    """
    Fetch and print info for a list of ticker symbols.
    
    :param tickers: List of ticker symbols as strings.
    """
    for ticker_symbol in tickers:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        # Define the information you want to fetch
        keys_of_interest = [
            'longName',
            'sector',
            'fullTimeEmployees',
            'marketCap',
            'trailingPE',
            'forwardPE',
            'dividendYield',
            'averageVolume',
            'priceToBook',
            'profitMargins',
            'revenueGrowth',
            'operatingMargins',
            'ebitda',
            'debtToEquity',
            'returnOnAssets',
            'returnOnEquity',
            'totalCash',
            'totalDebt',
            'currentPrice',
            'earningsGrowth',
            'beta'
        ]
        
        print(f"Data for {ticker_symbol}:")
        for key in keys_of_interest:
            # Use .get() to avoid KeyError if a key is missing
            print(f"{key}: {info.get(key, 'N/A')}")
        print("\n" + "-"*50 + "\n")

# Example usage
tickers = ['AAPL', 'MSFT', 'GOOGL']  # Add your tickers here
fetch_ticker_info(tickers)
