import os
import pandas as pd
from datetime import datetime

def calculate_date_gaps(file_path):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)
    df['Date_diff'] = df['Date'].diff().dt.days
    avg_gap = df['Date_diff'].mean()
    return avg_gap

def audit_date_gaps(folder_path):
    results = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                avg_gap = calculate_date_gaps(file_path)
                if avg_gap > 1:
                    symbol = pd.read_csv(file_path, nrows=1)['Symbol'].values[0]
                    results.append([file, symbol, avg_gap])
    return results

def save_results(results, output_file):
    df_results = pd.DataFrame(results, columns=['Filename', 'Symbol', 'Average Date Gap'])
    df_results.to_csv(output_file, index=False)

folder_path = 'unlocks_data_featurized'
output_file = 'summary_stats/date_gap_audit.csv'
results = audit_date_gaps(folder_path)
save_results(results, output_file)
