import os
import pandas as pd

# Folder containing the CSV files
folder_path = 'unlocks_data_featurized'
# Initialize an empty list to store the results
consolidated_data = []

# Iterate through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)
        # Load the CSV into a DataFrame
        df = pd.read_csv(file_path)
        
        # Ensure there is a 'Symbol' column and at least one row
        if 'Symbol' in df.columns and not df.empty:
            # Extract the symbol from the first non-header row
            symbol = df.loc[0, 'Symbol']
        else:
            # If 'Symbol' column or data is missing, skip this file
            continue
        
        # Sum insider_supply_growth where insider_unlock_type contains 'linear'
        linear_amount = df[df['insider_unlock_type'].str.contains('linear', case=False, na=False)]['insider_supply_growth'].sum()
        
        # Sum insider_supply_growth where insider_unlock_type contains 'cliff'
        cliff_amount = df[df['insider_unlock_type'].str.contains('cliff', case=False, na=False)]['insider_supply_growth'].sum()

        # Sum insider_supply_growth where insider_unlock_type contains 'token generation'
        tge_amount = df[df['insider_unlock_type'].str.contains('token generation', case=False, na=False)]['insider_supply_growth'].sum()
        
        # Add the results to the consolidated data list
        consolidated_data.append({
            'Project': filename.replace('.csv', ''),
            'Symbol': symbol,
            'linear_amount': linear_amount,
            'cliff_amount': cliff_amount,
            'tge_amount': tge_amount,
            'total_amount': linear_amount + cliff_amount + tge_amount
        })

# Convert the consolidated data into a DataFrame
final_df = pd.DataFrame(consolidated_data)

# Save the final DataFrame to a new CSV file
final_csv_path = 'summary_stats/cliff_vs_linear_vs_tge.csv'
final_df.to_csv(final_csv_path, index=False)

print(f'Done! Consolidated data saved to {final_csv_path}')
