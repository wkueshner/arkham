import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime

# Function to fetch the historical price of bitcoin
def fetch_historical_btc_price():
    response = requests.get("https://api.coindesk.com/v1/bpi/historical/close.json?start=2010-07-17&end=" + datetime.now().strftime('%Y-%m-%d'))
    data = response.json()
    prices = pd.DataFrame(data['bpi'].items(), columns=['Date', 'Price'])
    prices['Date'] = pd.to_datetime(prices['Date'])
    return prices

# Function to simulate fetching the balance of the bitcoin address over time
# Note: This is a placeholder function as the actual historical balance data is not readily available via an API
def fetch_wallet_balance_over_time():
    # Placeholder data: Assuming a constant balance for demonstration purposes
    balance = 50  # Initial balance in BTC
    dates = pd.date_range(start='2008-07-17', end=datetime.now(), freq='M')
    balances = pd.DataFrame({'Date': dates, 'Balance': balance})
    return balances

# Main function to fetch data and plot the chart
def main():
    btc_price = fetch_historical_btc_price()
    btc_balance = fetch_wallet_balance_over_time()

    # Create figure and axis objects with subplots()
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot BTC Price
    ax1.plot(btc_price['Date'], btc_price['Price'], color='tab:red', label='BTC Price ($)')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('BTC Price ($)', color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.set_yscale('log')
    ax1.xaxis.set_major_locator(mdates.YearLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # Create a second y-axis to plot the BTC balance
    ax2 = ax1.twinx()
    ax2.plot(btc_balance['Date'], btc_balance['Balance'], color='tab:blue', label='BTC Balance')
    ax2.set_ylabel('BTC Balance', color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    # Add a title and legend
    plt.title('Genesis Wallet Balance')
    fig.tight_layout()
    fig.legend(loc="upper left", bbox_to_anchor=(0.1,0.9))

    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()


