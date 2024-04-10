import pandas as pd
import os
from collections import Counter

def calculate_summary_stats():
    # Directory containing the CSV files
    data_dir = "unlocks_data_featurized"
    # Output directory for summary stats
    output_dir = "summary_stats"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    all_projects_summary = []
    
    # Iterate through each file in the data directory
    for file in os.listdir(data_dir):
        if file.endswith(".csv"):
            file_path = os.path.join(data_dir, file)
            df = pd.read_csv(file_path)
            
            # Extract project name and symbol
            project_name = file.split('.')[0]
            symbol = df.iloc[0]['Symbol'] if not df.empty else 'Unknown'
            
            # Calculate mean, median for insider_unlock_growth column
            mean_value = df['insider_supply_growth'].mean()
            median_value = df['insider_supply_growth'].median()
            
            # Calculate top 5 modes for insider_unlock_growth column
            mode_counts = Counter(df['insider_supply_growth'])
            top_5_modes = mode_counts.most_common(5)
            
            # Prepare data for summary
            summary_data = {
                "project": project_name,
                "symbol": symbol,
                "insider_supply_growth_mean": mean_value,
                "insider_supply_growth_median": median_value,
            }
            for i in range(5):
                summary_data[f"mode_{i+1}"] = top_5_modes[i][0] if i < len(top_5_modes) else "N/A"
            
            all_projects_summary.append(summary_data)
    
    # Convert all projects summary to DataFrame
    all_projects_summary_df = pd.DataFrame(all_projects_summary)
    
    # Write summary to a single CSV
    summary_file_path = os.path.join(output_dir, "all_projects_summary_stats.csv")
    all_projects_summary_df.to_csv(summary_file_path, index=False)
    print(f"All projects summary stats written to {summary_file_path}")

# Execute the function
if __name__ == "__main__":
    calculate_summary_stats()
