import os
import time
import csv
from datetime import datetime
import requests
from tabulate import tabulate
#import matplotlib.pyplot as plt

# Configuration
API_URL = "https://api.coingecko.com/api/v3/coins/markets"
CSV_FILE = "crypto_history.csv"

class CryptoTracker:
    def __init__(self):
        # Default tracked coins (stored by Coingecko IDs)
        self.tracked_coins = {
            "bitcoin": "Bitcoin",
            "ethereum": "Ethereum",
            "solana": "Solana"
        }
        self.vs_currency = "usd"
        self._initialize_csv()

    def _initialize_csv(self):
        """Initializes the CSV file with headers if it doesn't exist."""
        if not os.path.exists(CSV_FILE):
            with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Coin ID", "Name", "Price (USD)", "24h Change (%)"])

    def fetch_prices(self):
        """Fetches real-time data from CoinGecko API."""
        ids = ",".join(self.tracked_coins.keys())
        params = {
            "vs_currency": self.vs_currency,
            "ids": ids,
            "order": "market_cap_desc",
            "sparkline": "false",
            "price_change_percentage": "24h"
        }
        
        try:
            response = requests.get(API_URL, params=params, timeout=10)
            
            # Handle rate limiting or API downtime
            if response.status_code == 429:
                print("\nRate limit exceeded. Please wait a moment before trying again.")
                return None
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"\nNetwork error fetching crypto data: {e}")
            return None

    def display_prices(self, log_to_file=False):
        """Formats and displays live prices in a clean table structure."""
        data = self.fetch_prices()
        if not data:
            return

        table_data = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for coin in data:
            name = coin.get("name", "N/A")
            coin_id = coin.get("id", "N/A")
            price = coin.get("current_price", 0.0)
            change_24h = coin.get("price_change_percentage_24h", 0.0)
            
            # Format numbers safely
            formatted_price = f"${price:,.2f}" if price else "N/A"
            formatted_change = f"{change_24h:+.2f}%" if change_24h is not None else "N/A"

            table_data.append([name, formatted_price, formatted_change])

            if log_to_file:
                with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([timestamp, coin_id, name, price, change_24h])

        print(f"\n--- Live Crypto Prices ({timestamp}) ---")
        print(tabulate(table_data, headers=["Cryptocurrency", "Price (USD)", "24h Change"], tablefmt="grid"))

    def add_coin(self):
        """Adds a new cryptocurrency to the tracker by validating against API."""
        new_coin = input("Enter the CoinGecko ID of the coin (e.g., 'cardano', 'dogecoin'): ").strip().lower()
        if not new_coin:
            print("Input cannot be empty.")
            return

        if new_coin in self.tracked_coins:
            print(f"'{new_coin}' is already being tracked.")
            return

        print(f"Validating '{new_coin}' with API...")
        # Check validity by performing a quick lightweight test request
        test_params = {"vs_currency": "usd", "ids": new_coin}
        try:
            res = requests.get(API_URL, params=test_params, timeout=5)
            if res.status_code == 200 and len(res.json()) > 0:
                coin_data = res.json()[0]
                self.tracked_coins[new_coin] = coin_data['name']
                print(f"Successfully added {coin_data['name']}!")
            else:
                print("Invalid Coin ID. Make sure it matches the CoinGecko API standard id naming.")
        except requests.exceptions.RequestException:
            print("Validation failed due to connection error.")

    def auto_refresh_loop(self):
        """Runs an automated refresh loop at specified intervals."""
        try:
            interval = int(input("Enter refresh interval in seconds (min 10s): "))
            if interval < 10:
                print("Setting to absolute minimum safety threshold of 10s to prevent API ban.")
                interval = 10
        except ValueError:
            print("Invalid number. Defaulting to 30 seconds.")
            interval = 30

        print(f"\nStarting auto-refresh tracking every {interval}s. Press Ctrl+C to stop.")
        try:
            while True:
                self.display_prices(log_to_file=True)
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nAuto-refresh stopped. Returning to Main Menu.")

    def plot_trends(self):
        """Bonus Feature: Plots a quick trend visualization using the history logged in CSV."""
        if not os.path.exists(CSV_FILE):
            print("No historical tracking data found. Try running Auto-Refresh first.")
            return

        history = {}
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if not row: continue
                timestamp, _, name, price, _ = row
                if name not in history:
                    history[name] = {'times': [], 'prices': []}
                # Parse timestamp for clean display plotting
                dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                history[name]['times'].append(dt)
                history[name]['prices'].append(float(price))

        if not history:
            print("History file is empty.")
            return

        plt.figure(figsize=(10, 5))
        for name, data in history.items():
            plt.plot(data['times'], data['prices'], marker='o', label=name)

        plt.title("Cryptocurrency Price Trends (Logged Sessions)")
        plt.xlabel("Time")
        plt.ylabel("Price (USD)")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        print("Generating Trend Graph window... (Close the window to return to app)")
        plt.show()

def main_menu():
    tracker = CryptoTracker()
    
    while True:
        print("\n=== Live Cryptocurrency Price Tracker ===")
        print("1. View Prices Now")
        print("2. Add New Cryptocurrency")
        print("3. Start Auto-Refresh Mode (Logs to CSV)")
        print("4. View Price Trend Graph (Bonus)")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            tracker.display_prices(log_to_file=False)
        elif choice == '2':
            tracker.add_coin()
        elif choice == '3':
            tracker.auto_refresh_loop()
        elif choice == '4':
            tracker.plot_trends()
        elif choice == '5':
            print("Exiting Crypto Tracker. Goodbye!")
            break
        else:
            print("Invalid Choice. Please pick between 1 and 5.")

if __name__ == "__main__":
    main_menu()