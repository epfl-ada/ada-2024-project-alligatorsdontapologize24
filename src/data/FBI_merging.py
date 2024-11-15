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

def process_state_data(base_dir, output_file):
    """
    Process data for each state folder by loading, merging, and saving data from different yearly CSV files.
    
    Parameters:
    ----------
    base_dir : str
        The path to the base directory containing year-based folders (e.g., 'XX-1991', 'YY-1992').
    output_file : str
        The path where the final merged CSV file will be saved.
    
    Returns:
    -------
    pd.DataFrame
        A DataFrame containing the merged data from all years for one state.
    """
    all_data = []  # Initialize a list to collect data from each year

    # Loop through each folder in the base directory
    for folder in os.listdir(base_dir):
        # Check if the folder name matches the "XX-YYYY" pattern
        if len(folder) > 2 and folder[2] == '-':
            year = folder.split("-")[1]  # Extract the year
            folder_path = os.path.join(base_dir, folder)

            # Define file paths in lowercase
            incident_file = os.path.join(folder_path, 'nibrs_incident.csv')
            offense_file = os.path.join(folder_path, 'nibrs_offense.csv')
            arrestee_file = os.path.join(folder_path, 'nibrs_arrestee.csv')
            weapon_file = os.path.join(folder_path, 'nibrs_arrestee_weapon.csv')
            victim_file = os.path.join(folder_path, 'nibrs_victim.csv')
            injury_file = os.path.join(folder_path, 'nibrs_victim_injury.csv')
            circumstances_file = os.path.join(folder_path, 'nibrs_victim_circumstances.csv')

            # Load and process each CSV file
            incidents = load_csv(incident_file, usecols=['incident_id', 'incident_date'])
            if incidents.empty:
                continue  # Skip this year if the essential file is missing

            offenses = load_csv(offense_file, usecols=['incident_id', 'offense_type_id'])
            arrestees = load_csv(arrestee_file, usecols=['incident_id', 'arrestee_id'])
            weapons = load_csv(weapon_file, usecols=['arrestee_id', 'weapon_id'])
            victims = load_csv(victim_file, usecols=['incident_id', 'victim_id'])
            injuries = load_csv(injury_file, usecols=['victim_id', 'injury_id'])
            circumstances = load_csv(circumstances_file, usecols=['victim_id', 'circumstances_id'])

            # Start merging data based on the specified keys
            merged_data = incidents
            if not offenses.empty:
                merged_data = merged_data.merge(offenses, on='incident_id', how='left')
            if not arrestees.empty:
                merged_data = merged_data.merge(arrestees, on='incident_id', how='left')
            if not weapons.empty:
                merged_data = merged_data.merge(weapons, on='arrestee_id', how='left')
            if not victims.empty:
                merged_data = merged_data.merge(victims, on='incident_id', how='left')
            if not injuries.empty:
                merged_data = merged_data.merge(injuries, on='victim_id', how='left')
            if not circumstances.empty:
                merged_data = merged_data.merge(circumstances, on='victim_id', how='left')

            # Add a column for the year and append to the list
            merged_data['year'] = year
            all_data.append(merged_data)

    # Concatenate all yearly data into a single DataFrame
    if all_data:
        final_data = pd.concat(all_data, ignore_index=True)

        # Save the final merged dataset to a CSV file
        final_data.to_csv(output_file, index=False)
        print(f"Data processed and saved to {output_file}")
    else:
        print("No data was processed. Check the input directory.")

    return final_data if all_data else pd.DataFrame()

def merge_offense_types(base_dir, state_prefix, offense_file_name="nibrs_offense_type.csv", verbose=True):
    """
    Combine offense type data across years into a single DataFrame.

    Parameters:
    ----------
    base_dir : str
        Path to the base directory containing year-based folders.
    state_prefix : str
        Prefix used to identify state folders (e.g., "WA" for Washington).
    offense_file_name : str, optional
        Name of the CSV file containing offense type data. Default is "nibrs_offense_type.csv".
    verbose : bool, optional
        If True, prints additional information. Default is True.

    Returns:
    -------
    pd.DataFrame
        A combined DataFrame containing all offense type data.
    """
    all_offense_data = []

    for folder in os.listdir(base_dir):
        if folder.startswith(f"{state_prefix}-"):
            folder_path = os.path.join(base_dir, folder)
            offense_file_path = os.path.join(folder_path, offense_file_name)

            if os.path.exists(offense_file_path):
                offense_data = pd.read_csv(offense_file_path)
                all_offense_data.append(offense_data)

                if verbose:
                    print(f"Loaded offense type data from: {offense_file_path}")

    if not all_offense_data:
        raise ValueError("No offense type data found in the specified directory.")

    combined_offense_data = pd.concat(all_offense_data, ignore_index=True)

    if verbose:
        print(f"Combined offense type data contains {len(combined_offense_data)} rows.")

    return combined_offense_data