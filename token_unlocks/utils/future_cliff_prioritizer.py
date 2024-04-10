import pandas as pd
import os

# Define the folder containing the CSV files
folder_path = 'unlocks_data_featurized'

# Initialize a list to hold DataFrames from each file
dfs = []

# Loop over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # Construct the full path to the file
        csv_path = os.path.join(folder_path, filename)
        
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_path)
        
        # Ensure 'Date' is in datetime format and sort by it to ensure correct price lookup
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values(by='Date', inplace=True)
        
        # Filter rows based on 'insider_unlock_type' and date condition
        filtered_df = df[df['insider_unlock_type'].str.contains('first cliff|massive cliff', na=False)]
        filtered_df = filtered_df[filtered_df['Date'] > pd.to_datetime('2024-04-10')]
        
        # Find the 'Insiders' value at the latest date in the DataFrame
        latest_insiders_value = df.loc[df['Date'].idxmax(), 'Insiders']
        
        # Calculate the "percentage_of_fully_diluted_insider_supply"
        filtered_df['percentage_of_fully_diluted_insider_supply'] = filtered_df['insider_supply_growth'] / latest_insiders_value * 100
        
        # Initialize a list to store the calculated 'insider_unlocked_usd_value' for each row
        insider_unlocked_usd_values = []
        
        # Iterate over the filtered DataFrame to calculate 'insider_unlocked_usd_value'
        for index, row in filtered_df.iterrows():
            # Find the most recent 'Price' value from the unfiltered df for the current row's date
            latest_price = df[df['Date'] < row['Date']]['Price'].dropna().iloc[-1] if not df[df['Date'] < row['Date']]['Price'].dropna().empty else 0
            
            # Calculate 'insider_unlocked_usd_value'
            insider_unlocked_usd_value = row['insider_supply_growth'] * latest_price
            
            # Append the calculated value to the list
            insider_unlocked_usd_values.append(insider_unlocked_usd_value)
        
        # Add the 'insider_unlocked_usd_value' list as a new column to the filtered DataFrame
        filtered_df['insider_unlocked_usd_value'] = insider_unlocked_usd_values
        
        # Select only the required columns including the new metrics
        selected_columns_df = filtered_df[['Date', 'Symbol', 'insider_supply_growth', 'insider_unlock_type', 'insider_owned_float_percentage', 'percentage_of_fully_diluted_insider_supply', 'insider_unlocked_usd_value']]
        
        # Append the DataFrame to our list
        dfs.append(selected_columns_df)

# Concatenate all DataFrames in the list into one
final_df = pd.concat(dfs)

# Sort the final DataFrame by 'Date' in ascending order
final_df = final_df.sort_values(by="Date", ascending=True)

# Write the sorted DataFrame to a new CSV file
new_csv_path = 'summary_stats/future_cliffs.csv'
final_df.to_csv(new_csv_path, index=False)

print(f'Filtered data saved to {new_csv_path}.')
