import pandas as pd

df = pd.read_csv('block_reward_info.csv')

#print(df.info())
print(sum(df['reward_amount']))

