import yfinance as yf
import mysql.connector
from mysql.connector import Error
import datetime

# Function to connect to the MySQL database
def mysql_connection():
    try:
        connection = mysql.connector.connect(user='username', 
                                             password='password',
                                             host='localhost',
                                             database='finance_nifty50')
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

# Fetching the list of company symbols from the Companies table
def fetch_company_symbols(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT Symbol FROM Companies;"
        cursor.execute(query)
        symbols = [item[0] for item in cursor.fetchall()]
        cursor.close()
        return symbols
    except Error as e:
        print("Error fetching company symbols", e)
        return []

# Update the Companies table with fetch status and date
def update_fetch_status(connection, symbol, status):
    try:
        cursor = connection.cursor()
        current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        update_query = f"""UPDATE Companies SET FetchStatus = '{status}', LastFetchDate = '{current_date}' 
                           WHERE Symbol = '{symbol}';"""
        cursor.execute(update_query)
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error updating fetch status for {symbol}", e)

# Main script
if __name__ == "__main__":
    connection = mysql_connection()
    if connection and connection.is_connected():
        print("Successfully connected to MySQL")
        
        # Fetching company symbols from the database
        company_symbols = fetch_company_symbols(connection)
        
        if company_symbols:
            for symbol in company_symbols:
                try:
                    data = yf.download(symbol, start='2022-01-01', end='2023-01-01')
                    if not data.empty:
                        cursor = connection.cursor()
                        for index, row in data.iterrows():
                            insert_query = f"""INSERT INTO StockPrices (Date, Open, High, Low, Close, Adj_Close, Volume, Symbol) 
                                               VALUES ('{index.strftime('%Y-%m-%d')}', {row['Open']}, {row['High']}, {row['Low']}, {row['Close']}, {row['Adj Close']}, {row['Volume']}, '{symbol}');"""
                            cursor.execute(insert_query)
                        connection.commit()
                        cursor.close()
                        update_fetch_status(connection, symbol, 'success')
                    else:
                        update_fetch_status(connection, symbol, 'fail')
                except Exception as e:
                    print(f"Failed to fetch data for {symbol}: {e}")
                    update_fetch_status(connection, symbol, 'fail')
            print("Stock data fetched and status updated successfully.")
        else:
            print("No company symbols found.")
    else:
        print("Failed to connect to MySQL.")
