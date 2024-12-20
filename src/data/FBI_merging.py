import os
import pandas as pd

def load_csv(file_path, usecols=None):
    """
    Load a CSV file and select specific columns if they exist.
    
    Parameters:
    ----------
    file_path : str
        The path to the CSV file to load.
    usecols : list of str, optional
        A list of column names to select if they exist in the file.
    
    Returns:
    -------
    pd.DataFrame
        A DataFrame containing the selected columns or an empty DataFrame if the file doesn't exist.
    """
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        if usecols:
            usecols = [col.lower() for col in usecols]  # Ensure usecols are lowercase
            # Select only the columns that exist in the DataFrame
            usecols = [col for col in usecols if col in df.columns]
            df = df[usecols]
        return df
    return pd.DataFrame()  # Return an empty DataFrame if the file doesn't exist

def process_state_data(base_dir, output_file, violent_categories):
    """
    Process data for each state folder by loading, merging, filtering by violent offenses,
    and saving the result.

    Parameters:
    ----------
    base_dir : str
        The path to the base directory containing year-based folders (e.g., 'XX-1991', 'YY-1992').
    output_file : str
        The path where the final filtered dataset will be saved.
    violent_categories : list
        List of offense categories considered violent.

    Returns:
    -------
    pd.DataFrame
        A DataFrame containing the filtered data from all years for one state.
    """
    all_data = []  # Initialize a list to collect data from each year

    # Loop through each folder in the base directory
    for folder in os.listdir(base_dir):
        # Check if the folder name matches the "XX-YYYY" pattern
        if len(folder) > 2 and folder[2] == '-':
            year = folder.split("-")[1]  # Extract the year
            folder_path = os.path.join(base_dir, folder)

            # Define file paths
            incident_file = os.path.join(folder_path, 'nibrs_incident.csv')
            offense_file = os.path.join(folder_path, 'nibrs_offense.csv')
            offense_type_file = os.path.join(folder_path, 'nibrs_offense_type.csv')

            # Load and process each CSV file
            incidents = load_csv(incident_file, usecols=['incident_id', 'incident_date'])
            if incidents.empty:
                continue  # Skip this year if the essential file is missing

            offenses = load_csv(offense_file)
            offense_types = load_csv(offense_type_file, usecols=['offense_type_id', 'offense_code', 'offense_category_name'])

            # Determine which column to use for merging offenses with offense types
            if not offenses.empty and not offense_types.empty:
                if 'offense_type_id' in offenses.columns and 'offense_type_id' in offense_types.columns:
                    # Merge on offense_type_id
                    offenses = offenses.merge(offense_types[['offense_type_id', 'offense_category_name']], on='offense_type_id', how='left')
                elif 'offense_code' in offenses.columns and 'offense_code' in offense_types.columns:
                    # Merge on offense_code
                    offenses = offenses.merge(offense_types[['offense_code', 'offense_category_name']], on='offense_code', how='left')
                else:
                    offenses = pd.DataFrame()  # Skip if neither column is available
            else:
                offenses = pd.DataFrame()  # Skip if either file is missing

            # Merge incidents with offenses
            if not offenses.empty:
                merged_data = incidents.merge(offenses[['incident_id', 'offense_category_name']], on='incident_id', how='left')
                merged_data['year'] = year
                all_data.append(merged_data)

    # Concatenate all yearly data into a single DataFrame
    if all_data:
        final_data = pd.concat(all_data, ignore_index=True)

        # Filter for violent offenses
        if 'offense_category_name' in final_data.columns:
            filtered_data = final_data[final_data['offense_category_name'].isin(violent_categories)]
            print(f"Dropped {len(final_data) - len(filtered_data)} non-violent rows. Remaining rows: {len(filtered_data)}")

            # Save the filtered data
            filtered_data.to_csv(output_file, index=False)
            print(f"Filtered data saved to {output_file}")
        else:
            print(f"'offense_category_name' column not found in the data. Skipping filtering.")
            return pd.DataFrame()  # Return an empty DataFrame if filtering cannot be applied
    else:
        print("No data was processed. Check the input directory.")
        return pd.DataFrame()

    return filtered_data

def process_all_states(main_dir, output_base_dir, violent_categories):
    """
    Process data for all state folders in the main directory.

    Parameters:
    ----------
    main_dir : str
        The path to the main directory containing all state folders.
    output_base_dir : str
        The base directory where processed data for each state will be saved.

    Returns:
    -------
    None
    """
    # Ensure the output directory exists
    if not os.path.exists(output_base_dir):
        os.makedirs(output_base_dir)

    # Loop through each folder in the main directory
    for state_folder in os.listdir(main_dir):
        state_path = os.path.join(main_dir, state_folder)

        # Check if it is a directory
        if os.path.isdir(state_path):
            # Construct the output file path for the state
            output_file = os.path.join(output_base_dir, f"{state_folder}_violence.csv")

            print(f"Processing state: {state_folder}...")
            try:
                # Call the process_state_data function for this state
                process_state_data(state_path, output_file, violent_categories)
            except Exception as e:
                print(f"Error processing {state_folder}: {e}")

    print("Processing complete for all states.")



def merge_offense_type_from_all_states(base_dir, output_file):
    """
    Merge all `nibrs_offense_type.csv` files from all states and years
    and keep only `offense_type_id` and `offense_category_name` or
    `offense_code` and `offense_category_name` if `offense_type_id` is not available.
    
    Parameters:
    ----------
    base_dir : str
        The base directory containing state subdirectories with year-based subfolders.
    output_file : str
        The path to save the merged CSV file.
    
    Returns:
    -------
    pd.DataFrame
        A DataFrame containing the merged offense type data.
    """
    all_offense_types = []

    # Loop through all state directories in the base directory
    for state_folder in os.listdir(base_dir):
        state_path = os.path.join(base_dir, state_folder)

        # Check if it's a directory
        if os.path.isdir(state_path):
            # Loop through STATE-year subdirectories
            for year_folder in os.listdir(state_path):
                year_path = os.path.join(state_path, year_folder)

                # Check if it's a directory and matches the STATE-year pattern
                if os.path.isdir(year_path) and len(year_folder) > 2 and year_folder[2] == '-':
                    offense_file_path = os.path.join(year_path, 'nibrs_offense_type.csv')

                    # Check if the offense file exists
                    if os.path.exists(offense_file_path):
                        # Load the offense type file
                        df = pd.read_csv(offense_file_path)

                        # Determine which columns to keep
                        if 'offense_type_id' in df.columns:
                            df = df[['offense_type_id', 'offense_category_name']].rename(
                                columns={'offense_type_id': 'offense_key'}
                            )
                        elif 'offense_code' in df.columns:
                            df = df[['offense_code', 'offense_category_name']].rename(
                                columns={'offense_code': 'offense_key'}
                            )
                        else:
                            # Skip this file if neither column exists
                            continue
                        
                        # Add a column to indicate the state and year
                        df['state'] = state_folder
                        df['year'] = year_folder.split('-')[1] if '-' in year_folder else 'Unknown'

                        # Add the data to the list
                        all_offense_types.append(df)

    # Concatenate all offense type data into a single DataFrame
    if all_offense_types:
        merged_offense_types = pd.concat(all_offense_types, ignore_index=True)

        # Save the merged dataset to the output file
        merged_offense_types.to_csv(output_file, index=False)
        print(f"Offense type data merged and saved to: {output_file}")
    else:
        print("No offense type data was found.")

    return merged_offense_types if all_offense_types else pd.DataFrame()

def process_state_data_with_prefix(base_dir, output_file):
    """
    Process data for each state folder to take specific columns and add state prefix.

    Parameters:
    ----------
    base_dir : str
        The path to the base directory containing year-based folders (ex: 'XX-1991').
    output_file : str
        The path where the final dataset will be saved.

    Returns:
    -------
    pd.DataFrame
        A DataFrame that has the processed data from all years for one state.
    """
    all_data = []  # Initialize a list to collect data from each year

    # Loop through each folder in the base directory
    for folder in os.listdir(base_dir):
        # Check if the folder name matches the "XX-YYYY" pattern
        if len(folder) > 2 and folder[2] == '-':
            state_prefix = folder.split('-')[0]  # Extract the state prefix
            year = folder.split('-')[1]  # Extract the year
            folder_path = os.path.join(base_dir, folder)

            # Define file paths
            incident_file = os.path.join(folder_path, 'nibrs_incident.csv')
            offense_file = os.path.join(folder_path, 'nibrs_offense.csv')
            offense_type_file = os.path.join(folder_path, 'nibrs_offense_type.csv')

            # Load and process each CSV file
            incidents = load_csv(incident_file, usecols=['incident_id', 'incident_date'])
            if incidents.empty:
                continue  # Skip this year if the essential file is missing

            offenses = load_csv(offense_file)
            offense_types = load_csv(offense_type_file, usecols=['offense_type_id', 'offense_category_name'])

            # Determine which column to use for merging offenses with offense types
            if not offenses.empty and not offense_types.empty:
                if 'offense_type_id' in offenses.columns and 'offense_type_id' in offense_types.columns:
                    offenses = offenses.merge(offense_types[['offense_type_id', 'offense_category_name']], on='offense_type_id', how='left')
                elif 'offense_code' in offenses.columns and 'offense_code' in offense_types.columns:
                    offenses = offenses.merge(offense_types[['offense_code', 'offense_category_name']], on='offense_code', how='left')
                else:
                    offenses = pd.DataFrame()  # Skip if neither column is available
            else:
                offenses = pd.DataFrame()  # Skip if either file is missing

            # Merge incidents with offenses
            if not offenses.empty:
                merged_data = incidents.merge(offenses[['incident_id', 'offense_category_name']], on='incident_id', how='left')
                merged_data['state_prefix'] = state_prefix  # Add the state prefix column
                all_data.append(merged_data)

    # Concatenate all yearly data into a single DataFrame
    if all_data:
        final_data = pd.concat(all_data, ignore_index=True)

        # Select the desired columns
        final_data = final_data[['incident_date', 'offense_category_name', 'state_prefix']].rename(
            columns={'offense_category_name': 'offense_type'}
        )

        # Save the final dataset
        final_data.to_csv(output_file, index=False)
        print(f"Processed data saved to {output_file}")
    else:
        print("No data was processed. Check the input directory.")
        return pd.DataFrame()

    return final_data
