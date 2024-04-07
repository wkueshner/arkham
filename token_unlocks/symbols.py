import os
import csv

def read_symbols_from_csv(filepath, symbol_key):
    symbols = {}
    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            # Trim whitespace from headers if necessary
            csv_reader.fieldnames = [name.strip() for name in csv_reader.fieldnames]
            for row in csv_reader:
                # Trim leading/trailing whitespace from the symbol and check for its existence
                symbol = row.get(symbol_key, '').strip()
                if symbol:  # Ensure the symbol is not empty
                    symbols[symbol] = filepath
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return symbols

def fetch_unique_symbols(directory, symbol_key):
    symbols_info = {}
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.csv'):
                filepath = os.path.join(root, filename)
                symbols_in_file = read_symbols_from_csv(filepath, symbol_key)
                for symbol, path in symbols_in_file.items():
                    if symbol not in symbols_info:
                        symbols_info[symbol] = path
                        print(f"Found symbol: {symbol} in file: {path}")
    return symbols_info

def write_comparison_csv(unlocks, standardized, output_directory):
    fieldnames = ['symbol', 'unlocks_filepath', 'standardized_filepath']
    rows = []
    symbols_all = set()
    symbols_standardized = set()
    
    for symbol, filepath in unlocks.items():
        standardized_path = standardized.get(symbol, '')
        row = {
            'symbol': symbol,
            'unlocks_filepath': filepath,
            'standardized_filepath': standardized_path
        }
        rows.append(row)
        symbols_all.add(symbol)
        if filepath and standardized_path:  # Check if both paths are non-empty
            symbols_standardized.add(symbol)
    
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    output_filepath = os.path.join(output_directory, 'symbol_filepaths.csv')
    symbols_csv_path = os.path.join(output_directory, 'symbols.csv')
    symbols_standardized_csv_path = os.path.join(output_directory, 'symbols_standardized.csv')

    # Sort rows: rows with all fields non-empty come first
    sorted_rows = sorted(rows, key=lambda x: (x['standardized_filepath'] == '', x['symbol'], x['unlocks_filepath']))
    
    with open(output_filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in sorted_rows:
            writer.writerow(row)
    
    # Writing symbols.csv
    with open(symbols_csv_path, 'w', newline='', encoding='utf-8') as file:
        for symbol in sorted(symbols_all):
            file.write(f"'{symbol}'\n")
    
    # Writing symbols_standardized.csv
    with open(symbols_standardized_csv_path, 'w', newline='', encoding='utf-8') as file:
        for symbol in sorted(symbols_standardized):
            file.write(f"'{symbol}'\n")
    
    print(f"Files written to {output_directory}")

if __name__ == "__main__":
    # Adjust these paths according to your directory structure
    unlocks_directory = 'unlocks'
    unlocks_standardized_directory = 'unlocks_standardized'
    output_directory = 'symbols'  # Output directory for the CSV files

    print("Processing unlocks...")
    unique_symbols_unlocks = fetch_unique_symbols(unlocks_directory, 'Symbol')
    print("Processing unlocks_standardized...")
    unique_symbols_standardized = fetch_unique_symbols(unlocks_standardized_directory, 'Symbol')
    
    print("Writing to output directory...")
    write_comparison_csv(unique_symbols_unlocks, unique_symbols_standardized, output_directory)