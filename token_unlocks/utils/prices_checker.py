import csv

def check_symbols():
    # Load symbols from crypto_prices.csv
    crypto_prices_symbols = set()
    with open('token_price_data/crypto_prices.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            crypto_prices_symbols.add(row['symbol'])

    # Load symbols from symbols_standardized.csv
    standardized_symbols = set()
    with open('symbols/symbol_filepaths.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            standardized_symbols.add(row['symbol'])

    # Check which symbols in symbols_standardized.csv do not appear in crypto_prices.csv
    missing_symbols = standardized_symbols - crypto_prices_symbols

    if missing_symbols:
        print("Symbols in symbols_standardized.csv that do NOT appear in crypto_prices.csv:")
        for symbol in missing_symbols:
            print(symbol)
    else:
        print("All symbols in symbols_standardized.csv appear in crypto_prices.csv.")

# Call the function to perform the check
check_symbols()
