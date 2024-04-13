import os
import pandas as pd
from datetime import datetime

# Folder containing the CSV files
folder_path = 'unlocks_data_featurized'
# Initialize an empty list to store the results
consolidated_data = []

# Function to find the shortest time window for each project
def find_shortest_window(df, final_value):
    shortest_window = None
    for start_index in range(len(df)):
        cumulative_growth = 0
        for end_index in range(start_index, len(df)):
            cumulative_growth += df.iloc[end_index]['insider_supply_growth']
            if cumulative_growth >= final_value / 2:
                # Calculate the number of days in the window
                start_date = datetime.strptime(df.iloc[start_index]['Date'], '%Y-%m-%d')
                end_date = datetime.strptime(df.iloc[end_index]['Date'], '%Y-%m-%d')
                days = (end_date - start_date).days
                # If this window is shorter than the current shortest, update it
                if shortest_window is None or days < shortest_window['days']:
                    shortest_window = {
                        'start_date': df.iloc[start_index]['Date'],
                        'end_date': df.iloc[end_index]['Date'],
                        'days': days,
                        'start_index': start_index,
                        'end_index': end_index
                    }
                break  # Move to the next start index since we found our window
    return shortest_window

# Iterate through each file in the folder
# Iterate through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        df.sort_values(by='Date', inplace=True)
        
        # Filter rows to only those with non-zero 'insider_supply_growth'
        non_zero_growth_df = df[df['insider_supply_growth'] > 0]
        
        if 'Symbol' in df.columns and not df.empty:
            symbol = df.loc[0, 'Symbol']
        else:
            continue
        
        final_value = df['insider_supply_growth'].sum()
        # Pass the filtered DataFrame to the function
        shortest_window = find_shortest_window(non_zero_growth_df, final_value)
        
        if shortest_window:
            # Note: Indexes in shortest_window refer to non_zero_growth_df, need to map back if using original df
            window_df = non_zero_growth_df.iloc[shortest_window['start_index']:shortest_window['end_index']+1]
            
            linear_sum = window_df[window_df['insider_unlock_type'].str.contains('linear', case=False, na=False)]['insider_supply_growth'].sum()
            cliff_sum = window_df[window_df['insider_unlock_type'].str.contains('cliff', case=False, na=False)]['insider_supply_growth'].sum()
            tge_sum = window_df[window_df['insider_unlock_type'].str.contains('token generation', case=False, na=False)]['insider_supply_growth'].sum()
            
            max_type_growth = max(linear_sum, cliff_sum, tge_sum)
            max_type = 'linear' if max_type_growth == linear_sum else 'cliff' if max_type_growth == cliff_sum else 'token generation'
            
            linear_count = (window_df['insider_unlock_type'].str.contains('linear', case=False, na=False)).sum()
            cliff_count = (window_df['insider_unlock_type'].str.contains('cliff', case=False, na=False)).sum()
            tge_count = (window_df['insider_unlock_type'].str.contains('token generation', case=False, na=False)).sum()
            
            consolidated_data.append({
                'Project': filename.replace('.csv', ''),
                'Symbol': symbol,
                'start_date': shortest_window['start_date'],
                'end_date': shortest_window['end_date'],
                'days_between': shortest_window['days'],
                'unlock_type_most_contributed': max_type,
                'linear_count': linear_count,
                'cliff_count': cliff_count,
                'tge_count': tge_count,
            })
        
        print(f'Finished processing {symbol}.')  # Progress update

final_df = pd.DataFrame(consolidated_data)
final_csv_path = 'summary_stats/time_window_insider_distribution.csv'
final_df.to_csv(final_csv_path, index=False)

print('All files have been processed.')