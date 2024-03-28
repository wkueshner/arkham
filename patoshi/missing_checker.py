import pandas as pd

# Load the datasets
block_info_patoshi = pd.read_csv('block_info_patoshi.csv')
block_reward_info = pd.read_csv('block_reward_info.csv')

# Check the first few rows of each dataframe to understand their structure
block_info_patoshi.head(), block_reward_info.head()

# Identify block heights in block_info_patoshi that are not in block_reward_info
unique_block_heights = set(set(block_reward_info['block_height'] - block_info_patoshi['block_height']))

# Convert to sorted list for better readability
sorted_unique_block_heights = sorted(list(unique_block_heights))

print(sorted_unique_block_heights)
