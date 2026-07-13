import sys
from weather_api import get_current_weather
from storage import load_history, save_record
from analyzer import filter_by_city, calculate_analytics

def display_weather_card(data: dict):
    """Outputs a clean console display of current weather values."""
    print("\n" + "="*40)
    print(f" CURRENT WEATHER: {data['city'].upper()}")
    print("="*40)
    print(f" Temperature : {data['temperature']} C")
    print(f" Condition   : {data['condition']}")
    print(f" Humidity    : {data['humidity']}%")
    print(f" Wind Speed  : {data['wind_speed']} m/s")
    print("="*40)

def run_dashboard():
    while True:
        print("\n--- WEATHER TRACKING DASHBOARD ---")
        print("1. Get Current Weather")
        print("2. View History Log")
        print("3. Analyze City Trends")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == "1":
            city = input("Enter city name: ").strip()
            if not city:
                print("Error: City name cannot be empty.")
                continue
                
            weather = get_current_weather(city)
            if weather:
                display_weather_card(weather)
                save_option = input("Save this data snapshot to history? (y/n): ").strip().lower()
                if save_option == 'y':
                    if save_record(weather):
                        print("Success: Weather data saved locally.")
                        
        elif choice == "2":
            history = load_history()
            if not history:
                print("\nInformation: History log is empty.")
                continue
                
            print(f"\n{'Timestamp':<20} | {'City':<15} | {'Temp':<6} | {'Condition':<15}")
            print("-" * 65)
            for record in history:
                print(f"{record['timestamp']:<20} | {record['city']:<15} | {record['temperature']:>4} C | {record['condition']:<15}")
                
        elif choice == "3":
            city = input("Enter city name to analyze: ").strip()
            history = load_history()
            city_data = filter_by_city(history, city)
            
            if not city_data:
                print(f"\nNo records found for city: '{city}'")
                continue
                
            stats = calculate_analytics(city_data)
            print("\n" + "-"*40)
            print(f" ANALYTICS REPORT: {city.upper()}")
            print("-"*40)
            print(f" Total Snapshots Logged : {stats['count']}")
            print(f" Average Temperature     : {stats['avg_temp']} C")
            print(f" Maximum Temperature     : {stats['max_temp']} C")
            print(f" Minimum Temperature     : {stats['min_temp']} C")
            print(f" Average Humidity        : {stats['avg_humidity']}%")
            print("-"*40)
            
        elif choice == "4":
            print("\nExiting dashboard.")
            sys.exit()
        else:
            print("\nInvalid selection. Choose an option between 1 and 4.")

if __name__ == "__main__":
    run_dashboard()