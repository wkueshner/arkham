import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

folder_path = 'unlocks_data_featurized'
results = []

# Loop through each file
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        csv_path = os.path.join(folder_path, filename)
        df = pd.read_csv(csv_path)

        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values(by='Date', inplace=True)

        # Filter for dates before 2024-04-03 and non-zero prices
        df = df[(df['Date'] < pd.to_datetime('2024-04-03')) & (df['Price'] > 0)]

        # Identify rows with 'first cliff' or 'massive cliff'
        cliff_df = df[df['insider_unlock_type'].str.contains('first cliff', case=False, na=False)]
        
        # Only proceed if cliff rows are found
        if not cliff_df.empty:
            # Get the date of the first 'cliff' event
            first_cliff_date = cliff_df['Date'].min()
            
            # Calculate returns from T-365 to T-1
            for days_before in range(1, 366):
                past_date = first_cliff_date - pd.Timedelta(days=days_before)
                # Find the closest past date with a valid (non-zero) price
                past_price_row = df[(df['Date'] <= past_date) & (df['Price'] > 0)].iloc[-1] if not df[(df['Date'] <= past_date) & (df['Price'] > 0)].empty else None
                if past_price_row is not None:
                    return_percentage = ((cliff_df.iloc[0]['Price'] - past_price_row['Price']) / past_price_row['Price']) * 100
                    results.append((days_before, return_percentage, filename.replace('.csv', '')))

# Prepare the data for plotting
results_df = pd.DataFrame(results, columns=['Days Before Unlock', 'Return Percentage', 'Symbol'])

# Remove outliers where 'Return Percentage' > 2000
filtered_results_df = results_df[results_df['Return Percentage'] <= 2000]
"""
# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
for symbol, group in filtered_results_df.groupby('Symbol'):
    ax.scatter(group['Days Before Unlock'], group['Return Percentage'], label=symbol, alpha=0.7)

# Plot the slope of the distribution if necessary
x = filtered_results_df['Days Before Unlock']
y = filtered_results_df['Return Percentage']
slope, intercept = np.polyfit(x, y, 1)
ax.plot(x, slope*x + intercept, color='red', label=f'Slope: {slope:.2f}')

ax.set_xlabel('Number of Days Before Unlock')
ax.set_ylabel('Return from Buying at T-X and Selling at T (%)')
ax.set_title('Price Return Before First Cliff/Massive Cliff Event (Outliers Removed)')
#ax.legend()

plt.show()
"""

# Using Plotly for an interactive scatter plot
fig = px.scatter(filtered_results_df, x='Days Before Unlock', y='Return Percentage', color='Symbol',
                 hover_data=['Symbol'], title='Price Return Before First Cliff Event (Outliers Removed)')

# Fit a linear model to the data and add the regression line to the plot
x = filtered_results_df['Days Before Unlock']
y = filtered_results_df['Return Percentage']
slope, intercept = np.polyfit(x, y, 1)
fig.add_traces(go.Scatter(x=x, y=slope*x + intercept, mode='lines', name=f'Slope: {slope:.2f}', line=dict(color='red')))


# Get the coefficients of the quadratic polynomial
coefficients = np.polyfit(x, y, 2)

# Use the coefficients to calculate y-values for the quadratic line of best fit
x_line = np.linspace(x.min(), x.max(), 400)  # Generating x-values for plotting the curve
y_line = np.polyval(coefficients, x_line)  # Calculate y-values based on the quadratic coefficients

# Add the quadratic line of best fit to the plot
fig.add_traces(go.Scatter(x=x_line, y=y_line, mode='lines', name='Quadratic Fit', line=dict(color='orange')))


# Calculate the standard deviation of the y-values (Return Percentage)
std_dev = np.std(y)

# Add standard deviation lines to the plot
fig.add_traces(go.Scatter(x=x, y=slope*x + intercept + std_dev, mode='lines', name='1 Std Dev Above', line=dict(color='green', dash='dash')))
fig.add_traces(go.Scatter(x=x, y=slope*x + intercept - std_dev, mode='lines', name='1 Std Dev Below', line=dict(color='green', dash='dash')))

# Optionally, for 2 standard deviations, uncomment the following lines:
fig.add_traces(go.Scatter(x=x, y=slope*x + intercept + 2*std_dev, mode='lines', name='2 Std Dev Above', line=dict(color='purple', dash='dot')))
fig.add_traces(go.Scatter(x=x, y=slope*x + intercept - 2*std_dev, mode='lines', name='2 Std Dev Below', line=dict(color='purple', dash='dot')))

fig.update_layout(xaxis_title='Number of Days Before Unlock', yaxis_title='Return from Buying at T-X and Selling at T (%)')
fig.show()