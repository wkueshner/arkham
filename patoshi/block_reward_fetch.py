import requests
import pandas as pd
import time
import os

def fetch_and_append_block_reward_info(block_heights, output_file):
    """
    Fetch the recipient of the block reward and the amount of BTC awarded for each block height,
    then append each row of information to a CSV file.
    
    :param block_heights: A list of block heights.
    :param output_file: The file path to append the data.
    """
    request_count = 0
    start_time = time.time()
    
    # Determine the starting block_height if resuming from a previous run
    if os.path.exists(output_file):
        existing_df = pd.read_csv(output_file)
        last_height = existing_df['block_height'].max()
        block_heights = [height for height in block_heights if height > last_height]
    
    for height in block_heights:
        if request_count >= 6000:  # Check if request count has reached the limit
            elapsed_time = time.time() - start_time
            if elapsed_time < 300:  # If less than 5 minutes have passed
                print(f"Pausing for {300 - elapsed_time} seconds to respect the rate limit.")
                time.sleep(300 - elapsed_time)  # Pause execution
            # Reset counters
            request_count = 0
            start_time = time.time()
        
        url = f'https://blockchain.info/block-height/{height}?format=json'
        try:
            response = requests.get(url, timeout=10)  # Set a timeout of 10 seconds
            request_count += 1
        except requests.exceptions.Timeout:
            print(f"Request timed out for block height {height}.")
            continue  # Skip this iteration
        
        if response.status_code == 200:
            data = response.json()
            coinbase_tx = data['blocks'][0]['tx'][0]
            recipient_hash = coinbase_tx['out'][0]['addr']
            reward_amount = coinbase_tx['out'][0]['value'] / 1e8  # Convert satoshi to BTC
            reward_info = pd.DataFrame([{
                'block_height': height,
                'recipient_hash': recipient_hash,
                'reward_amount': reward_amount
            }])
            # Append to the CSV file
            reward_info.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
            print(f"Fetched and wrote block_height {height}.")
        else:
            print(f"Failed to fetch data for block height {height}")

# Load the CSV file
file_path = 'block_info_patoshi.csv'
output_file = 'block_reward_info.csv'  # Define the output file
block_info_df = pd.read_csv(file_path)

# Extract the block heights
block_heights = block_info_df['block_height'].tolist()

# Fetch the block reward info and append it to the output file
fetch_and_append_block_reward_info(block_heights, output_file)

print("Completed fetching and writing block reward information.")
