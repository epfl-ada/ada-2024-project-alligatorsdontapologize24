import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_coefficients_with_confidence_intervals(
        results_df: pd.DataFrame
        ) -> None:
    """
    Plot the coefficients and 95% confidence intervals for all variables, excluding 'const'.
    
    Args:
    - results_df (pd.DataFrame): A DataFrame with coefficient, standard error, and confidence interval values.

    Returns:
    - None
    """
    # Do not incldue const coefficient (due to highly different scales)
    results_df = results_df[results_df['variable'] != 'const']
    
    # Create the plot
    plt.figure(figsize=(10, 6))

    # Plotting the coefficients with their 95% confidence intervals
    for i, row in results_df.iterrows():
        plt.plot([row['lower_ci'], row['upper_ci']], [i, i], color='blue', lw=2)  # CI line
        plt.scatter(row['coefficient'], i, color='red', zorder=5)  # Coefficient dot

    # Set y-ticks and labels
    plt.yticks(np.arange(1,len(results_df)+1), results_df['variable'])
    plt.xlabel('Coefficient Estimate')
    plt.title('Coefficients and 95% Confidence Intervals (Excluding "const")')
    
    # Add gridlines for better readability
    plt.grid(True)
    plt.show()