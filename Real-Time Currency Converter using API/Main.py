import sys
from datetime import datetime
from currency_api import fetch_rates, convert_currency
from storage import load_history, persist_to_disk

def run_converter():
    # Session buffer holds conversions in memory until the user explicitly saves them
    session_buffer = []
    
    # Common target array for reference rate monitoring boards
    common_dashboard_currencies = ["USD", "EUR", "GBP", "PKR", "CAD", "AUD", "JPY"]

    while True:
        print("\n--- REAL-TIME CURRENCY CONVERTER ---")
        print("1. Convert Currency")
        print("2. View Exchange Rates")
        print("3. View History")
        print("4. Save Data")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ").strip()
        
        if choice == "1":
            from_curr = input("Enter Base Currency Code (e.g., USD): ").strip().upper()
            to_curr = input("Enter Target Currency Code (e.g., PKR): ").strip().upper()
            
            if not from_curr or not to_curr:
                print("Error: Currency codes cannot be blank.")
                continue
                
            amount_str = input("Enter Amount to Convert: ").strip()
            try:
                amount = float(amount_str)
                if amount <= 0:
                    print("Error: Conversion amount must be greater than zero.")
                    continue
            except ValueError:
                print("Error: Invalid numerical input for amount value.")
                continue
                
            result = convert_currency(amount, from_curr, to_curr)
            if result >= 0:
                print("\n" + "="*40)
                print(f" Converted Value: {amount:,} {from_curr} = {result:,} {to_curr}")
                print("="*40)
                
                # Buffer the record internally
                record = {
                    "from_currency": from_curr,
                    "to_currency": to_curr,
                    "amount": amount,
                    "result": result,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                session_buffer.append(record)
                print("Notice: Transaction staged in memory. Use Option 4 to commit to disk.")

        elif choice == "2":
            base_curr = input("Enter Base Currency for Rate Sheet (e.g., USD): ").strip().upper()
            if not base_curr:
                print("Error: Base currency code entry required.")
                continue
                
            rates = fetch_rates(base_curr)
            if rates:
                print(f"\nExchange Rates Dashboard for Base: {base_curr}")
                print("-" * 40)
                print(f"{'Currency':<15} | {'Exchange Rate':<20}")
                print("-" * 40)
                for code in common_dashboard_currencies:
                    if code in rates and code != base_curr:
                        print(f"{code:<15} | {rates[code]:<20,}")
                print("-" * 40)

        elif choice == "3":
            history = load_history()
            # Show both saved history and currently staged session history items items together
            all_records = history + session_buffer
            
            if not all_records:
                print("\nInformation: Conversion history registry is empty.")
                continue
                
            print(f"\n{'Timestamp':<20} | {'Conversion Details':<40}")
            print("-" * 65)
            for item in all_records:
                details = f"{item['amount']:,} {item['from_currency']} -> {item['result']:,} {item['to_currency']}"
                print(f"{item['timestamp']:<20} | {details:<40}")
                
        elif choice == "4":
            if persist_to_disk(session_buffer):
                print("Success: Memory buffer saved securely to local JSON file storage.")
                session_buffer.clear()
                
        elif choice == "5":
            if session_buffer:
                discard_confirm = input("You have unsaved session data. Exit anyway? (y/n): ").strip().lower()
                if discard_confirm != 'y':
                    continue
            print("\nExiting Currency Converter.")
            sys.exit()
        else:
            print("\nInvalid selection. Choose an option between 1 and 5.")

if __name__ == "__main__":
    run_converter()