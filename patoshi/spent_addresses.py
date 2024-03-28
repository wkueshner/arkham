import pandas as pd

def fetch_recipient_hashes(block_heights, input_file, output_file):
    """
    Fetch the recipient hashes for the specified block heights from the input CSV file,
    and save these block heights along with their corresponding hashes to a new CSV file.
    
    :param block_heights: A list of block heights.
    :param input_file: The file path of the input CSV containing block rewards information.
    :param output_file: The file path to save the block heights and their corresponding recipient hashes.
    """
    # Load the input CSV file
    df = pd.read_csv(input_file)
    
    # Filter the DataFrame for the specified block heights
    filtered_df = df[df['block_height'].isin(block_heights)]
    
    # Select only the 'block_height' and 'recipient_hash' columns
    result_df = filtered_df[['block_height', 'recipient_hash']]
    
    # Save the result to a new CSV file
    result_df.to_csv(output_file, index=False)
    print(f"Saved recipient hashes for specified block heights to {output_file}")

# Define the block heights to fetch recipient hashes for
block_heights = [9, 286, 688, 877, 1760, 2459, 2485, 3479, 5326, 9443, 9925, 10645, 14450, 15625, 15817, 19093, 23014, 28593, 29097]

# Define the input and output file paths
input_file = 'block_reward_info.csv'
output_file = 'spent_addresses.csv'

# Call the function
fetch_recipient_hashes(block_heights, input_file, output_file)


