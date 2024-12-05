import os
import pandas as pd

def preprocess_files_in_directory(base_dir, verbose=True):
    """
    Preprocess files in a specified directory by renaming each file to lowercase
    and standardizing all column names in CSV files to lowercase. This function
    is useful for normalizing file and column formats to simplify data processing (e.g., merging).

    Parameters:
    ----------
    base_dir : str
        The path to the base directory containing state-year folders (e.g., 'AL-2000', 'CA-1995').
        Each folder is expected to contain CSV files with potentially inconsistent naming conventions.
    
    Returns:
    -------
    None
        The function modifies files in place. Renamed files and standardized column names
        are saved back to the original files.

    Example:
    -------
    preprocess_files_in_directory('../../data/RAW')
    """
    # Iterate through each folder in the base directory
    for state_folder in os.listdir(base_dir):
        state_folder_path = os.path.join(base_dir, state_folder)
        
        # Check if the current item is a directory
        if os.path.isdir(state_folder_path):
            # Iterate through subdirectories (e.g., 'AL-2000')
            for year_folder in os.listdir(state_folder_path):
                year_folder_path = os.path.join(state_folder_path, year_folder)
                
                # Process only directories matching the pattern 'XX-YYYY'
                if os.path.isdir(year_folder_path) and len(year_folder) > 3 and year_folder[2] == '-':
                    # Process each file within the folder
                    for filename in os.listdir(year_folder_path):
                        original_file_path = os.path.join(year_folder_path, filename)
                        new_filename = filename.lower()
                        new_file_path = os.path.join(year_folder_path, new_filename)
                        
                        # Rename the file to lowercase if it is not already in lowercase
                        if original_file_path != new_file_path:
                            os.rename(original_file_path, new_file_path)
                            if verbose:
                                print(f"Renamed file: {original_file_path} -> {new_file_path}")
                        
                        # If the file is a CSV, process it to convert column names to lowercase
                        if new_file_path.endswith('.csv'):
                            try:
                                # Read the CSV file into a DataFrame
                                df = pd.read_csv(new_file_path)
                                
                                # Convert all column names to lowercase for consistency
                                df.columns = df.columns.str.lower()
                                
                                # Save the modified DataFrame back to the CSV file
                                df.to_csv(new_file_path, index=False)
                                if verbose:
                                    print(f"Processed columns in file: {new_file_path}")
                            
                            except Exception as e:
                                # Catch and report any errors encountered while processing the file
                                if verbose:
                                    print(f"Error processing file {new_file_path}: {e}")
