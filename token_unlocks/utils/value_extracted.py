import pandas as pd
import os

# Define the folder containing the CSV files
folder_path = 'unlocks_data_featurized'

# Initialize a list to hold the sum of 'unlock_usd_value' for each project
project_sums = []

# Define the cutoff date
cutoff_date = pd.Timestamp('2024-04-03')

# Loop over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # Construct the full path to the file
        csv_path = os.path.join(folder_path, filename)
        
        # Extract the project name from the filename (assuming the format is "symbol_standardized_unlock_schedule.csv")
        project = filename.split('_')[0]
        
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_path)
        
        # Convert 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        #print(df['Date'].head())
        
        # Filter rows where 'Date' is less than or equal to the cutoff date
        df_filtered = df[df['Date'] <= cutoff_date]
        
        # Ensure 'unlock_usd_value' column is treated as numeric type for calculations
        #df_filtered.loc[:, 'unlock_usd_value'] = pd.to_numeric(df_filtered['unlock_usd_value'], errors='coerce')
        
        # Before calculating 'total_unlock_usd_value', add logic to handle zero prices
        df_filtered['Adjusted_Price'] = df_filtered['Price']  # Create a new column to store adjusted prices

        for index, row in df_filtered.iterrows():
            if row['Price'] == 0:
                # Look forward for the next non-zero price
                future_prices = df_filtered.loc[index:, 'Price']
                next_non_zero_price_row = future_prices[future_prices != 0].first_valid_index()
                
                # If not found, look backward for the last non-zero price
                if next_non_zero_price_row is None:
                    past_prices = df_filtered.loc[:index, 'Price']
                    last_non_zero_price_row = past_prices[past_prices != 0].last_valid_index()
                    if last_non_zero_price_row is not None:
                        df_filtered.at[index, 'Adjusted_Price'] = df_filtered.at[last_non_zero_price_row, 'Price']
                else:
                    df_filtered.at[index, 'Adjusted_Price'] = df_filtered.at[next_non_zero_price_row, 'Price']

        # Now calculate 'total_unlock_usd_value' using 'Adjusted_Price' instead of 'Price'
        total_unlock_usd_value = (df_filtered['insider_supply_growth'] * df_filtered['Adjusted_Price']).sum()
        
        # Extract the symbol from the first row (assuming all rows have the same symbol for a given file)
        symbol = df_filtered.iloc[0]['Symbol'] if not df_filtered.empty else 'Unknown'
        
        # Append the project, symbol, and sum to our list without formatting as string
        project_sums.append({
            "Project": project,
            "Symbol": symbol,
            "total_insider_unlocked_usd_value": total_unlock_usd_value
        })

# Convert the list of sums into a DataFrame
summary_df = pd.DataFrame(project_sums)

# Sort the DataFrame by 'total_insider_unlocked_usd_value' in descending order
summary_df = summary_df.sort_values(by="total_insider_unlocked_usd_value", ascending=False)

# Optional: Format 'total_insider_unlocked_usd_value' as a string for display purposes
summary_df['total_insider_unlocked_usd_value'] = summary_df['total_insider_unlocked_usd_value'].map("{:.2f}".format)

# Write the sorted DataFrame to a new CSV file
new_csv_path = 'summary_stats/total_value_extracted.csv'
summary_df.to_csv(new_csv_path, index=False)

print(f'Summary of total insider unlocked USD value saved to {new_csv_path}.')

