import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('block_info_patoshi.csv', header=None)
df.columns = ['block_height', 'ExtraNonce', 'entity']

# Prepare the data
df['color'] = df['entity'].apply(lambda x: 'blue' if x == 'Patoshi' else 'green')

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(df['block_height'], df['ExtraNonce'], c=df['color'], alpha=0.5)
plt.title('Block Height vs ExtraNonce')
plt.xlabel('Block Height')
plt.ylabel('ExtraNonce')
plt.show()
