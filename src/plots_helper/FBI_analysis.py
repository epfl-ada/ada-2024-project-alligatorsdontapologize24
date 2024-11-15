import os
import pandas as pd
import matplotlib.pyplot as plt


def analyze_offenses(data, base_dir, state_prefix, offense_file_name='nibrs_offense_type.csv', top_n=10, verbose=True):
    """
    Visualize offense data from a given state directory and merged dataset.

    Parameters:
    ----------
    data : pd.DataFrame
        The merged dataset containing an 'offense_type_id' column.
    base_dir : str
        Path to the base directory containing year-based state folders (e.g., 'XX-1991', 'YY-1992').
    state_prefix : str
        Prefix used to identify state folders (e.g., 'AL' for Alabama, 'NY' for New York).
    offense_file_name : str, optional
        Name of the CSV file containing offense type data. Default is 'nibrs_offense_type.csv'.
    top_n : int, optional
        Number of top recurring offenses to visualize. Default is 10.
    verbose : bool, optional
        If True, prints additional information during processing. Default is True.

    Returns:
    -------
    None
        Displays two plots:
        1. Number of unique offenses in `final_data`.
        2. Top `top_n` most recurring offense types.
    """
    if 'offense_type_id' not in data.columns:
        print("The 'offense_type_id' column is missing in the provided data.")
        return

    # Initialize a dictionary to map offense IDs to names
    offense_id_to_name = {}

    # Get unique offense IDs in final_data
    unique_offenses_in_final_data = data['offense_type_id'].unique()

    # Loop through each year folder to get offense names for these unique IDs
    for folder in os.listdir(base_dir):
        if folder.startswith(f"{state_prefix}-"):
            folder_path = os.path.join(base_dir, folder)
            offense_type_file = os.path.join(folder_path, offense_file_name)

            # Check if the offense type file exists
            if os.path.exists(offense_type_file):
                offense_data = pd.read_csv(offense_type_file)
                
                # Check for required columns
                if 'offense_type_id' in offense_data.columns and 'offense_name' in offense_data.columns:
                    # Filter only the offenses that are in final_data
                    filtered_data = offense_data[offense_data['offense_type_id'].isin(unique_offenses_in_final_data)]
                    offense_id_to_name.update(filtered_data.set_index('offense_type_id')['offense_name'].to_dict())

                    if verbose:
                        print(f"Processed {len(filtered_data)} offense types from {offense_type_file}")

    # Count the occurrences of each offense type in 'final_data'
    top_offenses = data['offense_type_id'].value_counts().head(top_n)

    # Map the offense names for the top offenses
    top_offenses_names = top_offenses.index.map(lambda x: offense_id_to_name.get(x, 'Unknown')).tolist()

    # Plotting
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    # Plot 1: Number of unique offenses in final_data
    unique_offense_count = len(unique_offenses_in_final_data)
    axes[0].bar(['Unique Offenses in Final Data'], [unique_offense_count], color='salmon')
    axes[0].set_xlabel('Data Source')
    axes[0].set_ylabel('Number of Unique Offenses')
    axes[0].set_title('Number of Unique Offenses in Final Data')

    # Plot 2: Most recurring offense types in final_data
    if not top_offenses.empty:
        top_offenses.plot(kind='bar', ax=axes[1], color='lightgreen')
        axes[1].set_xlabel('Offense Type ID')
        axes[1].set_ylabel('Number of Occurrences')
        axes[1].set_title(f'Top {top_n} Most Recurring Offense Types')
        
        # Set offense names as x-axis labels
        axes[1].set_xticklabels(top_offenses_names, rotation=45, ha='right')

    plt.tight_layout()
    plt.show()



def analyze_incidents_and_missing_values(data, date_column, figsize=(16, 8), verbose=True):
    """
    Analyze and visualize data by incident year and missing values in a dataset.

    Parameters:
    ----------
    data : pd.DataFrame
        The dataset containing the incident data.
    date_column : str
        The name of the column containing incident dates.
    figsize : tuple, optional
        Figure size for the plots. Default is (16, 8).
    verbose : bool, optional
        If True, prints additional information during processing. Default is True.

    Returns:
    -------
    None
        Displays two plots:
        1. Number of records per incident year.
        2. Number of missing values per column.
    """
    if date_column not in data.columns:
        print(f"The specified date column '{date_column}' is not present in the dataset.")
        return

    # Ensure the date column is in datetime format
    data[date_column] = pd.to_datetime(data[date_column], errors='coerce')
    if verbose:
        print(f"Converted '{date_column}' to datetime format.")

    # Extract the year from the date column and create a new 'incident_year' column
    data['incident_year'] = data[date_column].dt.year.astype('Int64')
    if verbose:
        print("Created 'incident_year' column based on the date column.")

    # Set up subplots for two plots side by side
    fig, axes = plt.subplots(1, 2, figsize=figsize)

    # Plot 1: Bar plot of data per year based on 'incident_year'
    year_counts = data['incident_year'].value_counts().sort_index()  # Count entries per incident year and sort by year
    year_counts.plot(kind='bar', color='skyblue', ax=axes[0])
    axes[0].set_xlabel('Year of Incident')
    axes[0].set_ylabel('Number of Records')
    axes[0].set_title('Number of Records per Incident Year in Data')
    axes[0].tick_params(axis='x', rotation=45)  # Rotate x-axis labels for readability

    # Plot 2: Bar plot of number of NaN values for each column
    nan_counts = data.isna().sum()  # Count NaNs for each column
    nan_counts.plot(kind='bar', color='salmon', ax=axes[1])
    axes[1].set_xlabel('Columns')
    axes[1].set_ylabel('Number of NaN Values')
    axes[1].set_title('Number of NaN Values per Column in Data')
    axes[1].tick_params(axis='x', rotation=45)  # Rotate x-axis labels for readability

    # Add value labels on top of each bar in the NaN counts plot
    for index, value in enumerate(nan_counts):
        if value > 0:  # Only label bars with non-zero NaN counts
            axes[1].text(index, value, f'{value}', ha='center', va='bottom', fontsize=10, rotation=45)

    # Adjust layout for better spacing between plots
    plt.tight_layout()
    plt.show()
