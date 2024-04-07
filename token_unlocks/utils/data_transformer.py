import pandas as pd
import os
import numpy as np

def clean_and_format_data(df):
    df_cleaned = df.drop_duplicates().copy()

    # Remove specific columns if they exist
    columns_to_remove = ['Reserved', 'Community & Other', 'Available Supply']
    df_cleaned = df_cleaned.drop(columns=[col for col in columns_to_remove if col in df_cleaned.columns], errors='ignore')
    
    # Enhanced cleaning for 'Price' column
    if 'Price' in df.columns:
        # Ensure 'Price' column is treated as string
        df_cleaned['Price'] = df_cleaned['Price'].astype(str)
        # Remove dollar signs and any other non-numeric characters except the decimal point
        df_cleaned['Price'] = df_cleaned['Price'].str.replace('[^\d.]', '', regex=True)
        # Handle cases with multiple numbers by selecting the first one
        df_cleaned['Price'] = df_cleaned['Price'].str.split().str[0]
        # Convert to float
        df_cleaned['Price'] = df_cleaned['Price'].astype(float)
        
    if 'Date' in df.columns:
        # Convert 'Date' column to datetime, specifying the format
        df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'], format='%b %d %Y').dt.strftime('%Y-%m-%d')
        df_cleaned.sort_values(by='Date', inplace=True)
    
    # Reset index to avoid indexing issues in later operations
    df_cleaned.reset_index(drop=True, inplace=True)
    
    return df_cleaned

def add_insiders_column(df):
    df['Insiders'] = 0
    for column in ['Founder / Team', 'Private Investors']:
        if column in df.columns:
            df['Insiders'] += df[column].fillna(0)
    return df

def calculate_insider_metrics(df):
    df['insider_supply_growth'] = 0.0  # This will now represent the growth amount
    df['insider_supply_growth_percentage'] = 0.0  # New column for growth percentage
    df['insider_unlock_type'] = 'no unlock'
    
    for i in range(1, len(df)):
        current_insiders = df.at[i, 'Insiders']
        previous_insiders = df.at[i-1, 'Insiders']
        
        # Calculate growth amount
        growth_amount = current_insiders - previous_insiders
        df.at[i, 'insider_supply_growth'] = growth_amount
        
        # Calculate growth percentage if previous_insiders > 0, else set to np.inf
        if previous_insiders > 0:
            df.at[i, 'insider_supply_growth_percentage'] = (growth_amount / previous_insiders) * 100
        elif current_insiders > 0:
            df.at[i, 'insider_supply_growth_percentage'] = np.inf
            
    for i in range(len(df)):
        growth_percentage = df.at[i, 'insider_supply_growth_percentage']
        growth_amount = df.at[i, 'insider_supply_growth']
        classify_growth(df, i, growth_percentage, growth_amount)
    
    return df

def classify_growth(df, i, growth_percentage, growth_amount):
    # Initialize previous and subsequent growth amounts
    previous_growth_amount = df.at[i-1, 'insider_supply_growth'] if i > 0 else None
    subsequent_growth_amount = df.at[i+1, 'insider_supply_growth'] if i < len(df) - 1 else None
    previous_insiders = df.at[i-1, 'Insiders'] if i > 0 else None

    # Check for 'first cliff unlock'
    if previous_insiders == 0 and subsequent_growth_amount == 0:
        df.at[i, 'insider_unlock_type'] = 'first cliff unlock'
    # Check for 'no unlock' scenario
    elif growth_percentage == 0:
        df.at[i, 'insider_unlock_type'] = 'no unlock'
    # Check for 'first linear unlock'
    elif previous_insiders == 0 and subsequent_growth_amount is not None and abs(growth_amount - subsequent_growth_amount) < 10:
        df.at[i, 'insider_unlock_type'] = 'first linear unlock'
    # Check for 'linear unlock' which depends on the previous growth amount
    elif previous_growth_amount is not None and abs(growth_amount - previous_growth_amount) < 10:
        df.at[i, 'insider_unlock_type'] = 'linear unlock'
    # Classify based on growth percentage
    elif growth_percentage < 20:
        df.at[i, 'insider_unlock_type'] = 'small cliff unlock'
    elif 20 <= growth_percentage < 50:
        df.at[i, 'insider_unlock_type'] = 'medium cliff unlock'
    elif growth_percentage >= 50:
        df.at[i, 'insider_unlock_type'] = 'large cliff unlock'

def calculate_additional_metrics(df):
    """
    Computes daily metrics and adds them as new columns to the DataFrame.
    The metrics are calculated for each day.
    """
    # Ensure numeric columns are treated as numeric types for calculations
    numeric_columns = ['Insiders', 'Price', 'Unlocked Supply']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
    
    # Initialize new columns
    df['tokens_unlocked'] = df['Insiders'].diff().fillna(0)
    df['unlock_usd_value'] = (df['Insiders'] * df['Price']).diff().fillna(0)
    df['insider_owned_float_percentage'] = (df['Insiders'] / df['Unlocked Supply']) * 100

    # Calculate daily supply increase percentage
    df['daily_supply_increase_percentage'] = (df['Unlocked Supply'].diff() / df['Unlocked Supply'].shift(1)) * 100

    # Reset index to ensure consistent indexing
    df.reset_index(drop=True, inplace=True)
    # Avoid direct slice modification to prevent SettingWithCopyWarning
    if not df.empty:
        df.at[0, 'daily_supply_increase_percentage'] = float('nan')

    return df

def round_numeric_columns(df):
    """
    Rounds all numeric columns in the DataFrame to remove decimal values,
    excluding specific columns that are computed later in the process.
    """
    # List of columns to exclude from rounding
    exclude_columns = ['insider_supply_growth', 'insider_supply_growth_percentage', 'tokens_unlocked', 'unlock_usd_value', 'insider_owned_float_percentage', 'daily_supply_increase_percentage']
    
    # Identify numeric columns that are not in the exclude list
    numeric_cols = df.select_dtypes(include=[np.number]).columns.difference(exclude_columns)
    
    # Round these numeric columns
    df[numeric_cols] = df[numeric_cols].round(0).astype(int)
    
    return df

def process_and_save_csv(csv_path, new_folder):
    df = pd.read_csv(csv_path)
    df = clean_and_format_data(df)
    df = add_insiders_column(df)
    df = round_numeric_columns(df)  # Call the new rounding function here
    df = calculate_insider_metrics(df)
    df = calculate_additional_metrics(df)
    
    base_name = os.path.basename(csv_path).split('_', 1)[0]
    new_file_path = os.path.join(new_folder, f'{base_name}_featurized.csv')
    
    os.makedirs(new_folder, exist_ok=True)
    df.to_csv(new_file_path, index=False)
    
    print(f'Data processed and saved to {new_file_path}.')

'''
csv_path = 'unlocks_standardized1/aevo-exchange_standardized_unlock_schedule.csv'
process_and_save_csv(csv_path)
'''

# Define the source and destination folder paths
source_folder = 'unlocks_standardized1'
new_folder = 'unlocks_data_featurized'

# Iterate over all CSV files in the source folder
for filename in os.listdir(source_folder):
    if filename.endswith('.csv'):
        csv_path = os.path.join(source_folder, filename)
        process_and_save_csv(csv_path, new_folder)