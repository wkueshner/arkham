import os
import pandas as pd
from datetime import datetime

def calculate_date_gaps_and_large_gaps(df):
    # Assuming df is already a DataFrame with 'Date' column in the correct format
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)
    df['Date_diff'] = df['Date'].diff().dt.days
    avg_gap = df['Date_diff'].mean()
    large_gaps = df.loc[df['Date_diff'] > 1, 'Date_diff'][:10].astype(str).str.cat(sep=';')
    df.drop(columns=['Date_diff'], inplace=True)
    return avg_gap, large_gaps

def audit_date_gaps(folder_path):
    results = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)
                avg_gap, large_gaps = calculate_date_gaps_and_large_gaps(df)
                if avg_gap > 1:
                    symbol = df.iloc[0]['Symbol']
                    results.append([file, symbol, avg_gap, large_gaps])
    return results

def save_results(results, output_file):
    df_results = pd.DataFrame(results, columns=['Filename', 'Symbol', 'Average Date Gap', 'First 10 Large Gaps'])
    df_results.to_csv(output_file, index=False)

folder_path = 'unlocks_data_featurized'
output_file = 'summary_stats/date_gap_audit.csv'
results = audit_date_gaps(folder_path)
save_results(results, output_file)
