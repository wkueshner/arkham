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
        
        # Extract the project name from the filename (assuming the format is "symbol_standardized_unlock_schedule.csv")
        project = filename.split('_')[0]
        
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_path)
        
        # Ensure numeric columns are treated as numeric types for calculations
        numeric_columns = ['Insiders', 'Price', 'Unlocked Supply']
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
        
        # Perform calculations as before...
        # Identify the first day with a non-zero "Insiders" value
        filtered_df = df[df['Insiders'] > 0]
        if not filtered_df.empty:
            first_non_zero_row = filtered_df.iloc[0]

            # Extract the symbol and date from the first_non_zero_row
            symbol = first_non_zero_row['Symbol']
            date = first_non_zero_row['Date']

            tokens_unlocked = first_non_zero_row['Insiders']
            price = first_non_zero_row['Price']
            price_date = date  # Initialize price_date with the current date

            # Check if the price is 0 and adjust accordingly
            if price == 0:
                # Look forward for the next non-zero price
                future_prices = df.loc[first_non_zero_row.name:, 'Price']
                next_non_zero_price_row = future_prices[future_prices != 0].first_valid_index()
                
                # If not found, look backward for the last non-zero price
                if next_non_zero_price_row is None:
                    past_prices = df.loc[:first_non_zero_row.name, 'Price']
                    last_non_zero_price_row = past_prices[past_prices != 0].last_valid_index()
                    if last_non_zero_price_row is not None:
                        price = df.at[last_non_zero_price_row, 'Price']
                        price_date = df.at[last_non_zero_price_row, 'Date']
                else:
                    price = df.at[next_non_zero_price_row, 'Price']
                    price_date = df.at[next_non_zero_price_row, 'Date']

            unlock_usd_value = tokens_unlocked * price
            insider_owned_float_percentage = (tokens_unlocked / first_non_zero_row['Unlocked Supply']) * 100

            # Find the previous day's "Unlocked Supply" to calculate supply increase percentage
            previous_day_index = df.index[df.index == first_non_zero_row.name] - 1
            if previous_day_index >= 0:
                previous_day_unlocked_supply = df.at[previous_day_index[0], 'Unlocked Supply']
                # Check if previous_day_unlocked_supply is zero to avoid division by zero
                if previous_day_unlocked_supply == 0:
                    supply_increase_percentage = 'inf'  # Set to None (null) if previous day's supply is zero
                else:
                    supply_increase_percentage = ((first_non_zero_row['Unlocked Supply'] - previous_day_unlocked_supply) / previous_day_unlocked_supply) * 100
            else:
                supply_increase_percentage = 'inf'  # Set to None (null) if there is no previous day
            
            # Calculate the difference in days between the Price_date and the Date
            date_diff = (pd.to_datetime(price_date) - pd.to_datetime(date)).days

        else:
            # Handle the case where no rows meet the condition, e.g., by continuing to the next file or setting default values
            continue  # or set default values for the metrics

        # Add a "Date", "Symbol", "Project", "Price_date", and "Price_date_diff" column to the DataFrame
        new_df = pd.DataFrame({
            "Date": [date],
            "Symbol": [symbol],
            "Project": [project],
            "Price_date_diff": [date_diff],  # New column for the difference in days
            "insider_unlock_usd_value": [unlock_usd_value],
            #"insider_tokens_unlocked": [tokens_unlocked],
            "insider_owned_float_percentage": [insider_owned_float_percentage],
            #"supply_increase_percentage": [supply_increase_percentage],
            "Price_date": [price_date]  # New column for the date of the price used
        })
        
        # Append the DataFrame to our list
        dfs.append(new_df)

# Concatenate all DataFrames in the list into one
final_df = pd.concat(dfs)

# Sort the final DataFrame by 'insider_unlock_usd_value' in descending order
final_df = final_df.sort_values(by="insider_unlock_usd_value", ascending=False)

# Write the sorted DataFrame to a new CSV file
new_csv_path = 'summary_stats/combined_cliff_metrics.csv'
final_df.to_csv(new_csv_path, index=False)

print(f'Calculations for all symbols saved to {new_csv_path}.')
