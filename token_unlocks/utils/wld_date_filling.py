import pandas as pd

def identify_two_day_gaps(file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    # Sort the DataFrame by the 'Date' column
    df.sort_values(by='Date', inplace=True)
    # Calculate the difference between each date and the previous date
    df['Date_diff'] = df['Date'].diff().dt.days
    # Identify rows where the difference is exactly 2 days
    two_day_gaps = df[df['Date_diff'] == 2]
    # Print the dates with 2-day gaps
    for index, row in two_day_gaps.iterrows():
        print(f"2-day gap found before: {row['Date'].strftime('%Y-%m-%d')}")

# Specify the path to the CSV file
file_path = 'unlocks_data_featurized/worldcoin-wld_featurized.csv'
# Call the function with the specified file path
identify_two_day_gaps(file_path)
