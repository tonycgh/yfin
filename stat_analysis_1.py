# Created by Tony Cowling using ChatGPT 4
# Read the licence page
# 2024

import mysql.connector
import pandas as pd
import numpy as np

# Function to connect to the MySQL database
def mysql_connection():
    try:
        connection = mysql.connector.connect(user='username', 
                                             password='password',
                                             host='localhost',
                                             database='finance_nifty50')
        return connection
    except mysql.connector.Error as e:
        print("Error while connecting to MySQL", e)
        return None

# Fetch Adjusted Close Prices for all tickers
def fetch_stock_prices(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT Symbol, Date, Adj_Close FROM StockPrices ORDER BY Symbol, Date;"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        # Creating a DataFrame
        df = pd.DataFrame(data, columns=['Symbol', 'Date', 'Adj_Close'])
        return df.pivot(index='Date', columns='Symbol', values='Adj_Close')
    except mysql.connector.Error as e:
        print("Error fetching stock prices", e)
        return pd.DataFrame()

# Calculate daily returns
def calculate_daily_returns(prices_df):
    return prices_df.pct_change()

# Calculate pairwise correlations
def calculate_correlations(daily_returns_df):
    return daily_returns_df.corr()

# Main script
if __name__ == "__main__":
    connection = mysql_connection()
    if connection is not None and connection.is_connected():
        prices_df = fetch_stock_prices(connection)
        if not prices_df.empty:
            daily_returns_df = calculate_daily_returns(prices_df)
            correlations_df = calculate_correlations(daily_returns_df)
            
            # Display or process the correlations
            print(correlations_df)
            
            connection.close()
        else:
            print("No stock prices found.")
    else:
        print("Failed to connect to MySQL.")
