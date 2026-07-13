import requests
from config import BASE_URL

# In-memory cache to prevent redundant API calls during the session
_exchange_rate_cache = {}

def fetch_rates(base_currency: str) -> dict:
    """
    Fetches latest exchange rates for the specified base currency.
    Implements local caching to optimize API usage efficiency.
    """
    base_currency = base_currency.upper()
    
    # Check cache first to avoid unnecessary API consumption
    if base_currency in _exchange_rate_cache:
        return _exchange_rate_cache[base_currency]
        
    url = f"{BASE_URL}/{base_currency}"
    try:
        response = requests.get(url, timeout=10)
        
        # The endpoint returns a 200 even for invalid currencies but marks result as 'error'
        data = response.json()
        if data.get("result") == "error":
            print(f"\nError: Unsupported or invalid currency code '{base_currency}'.")
            return {}
            
        response.raise_for_status()
        
        # Cache the rates registry payload
        _exchange_rate_cache[base_currency] = data.get("rates", {})
        return _exchange_rate_cache[base_currency]

    except requests.exceptions.ConnectionError:
        print("\nNetwork Error: Unable to reach the exchange rate service. Check your internet connection.")
    except requests.exceptions.Timeout:
        print("\nTimeout Error: The server request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"\nUnexpected Error: {e}")
        
    return {}

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """
    Calculates the conversion value between two specified currencies.
    """
    rates = fetch_rates(from_currency)
    if not rates:
        return -1.0
        
    target_code = to_currency.upper()
    if target_code not in rates:
        print(f"\nError: Target currency '{to_currency}' not found in exchange registries.")
        return -1.0
        
    conversion_rate = rates[target_code]
    return round(amount * conversion_rate, 2)