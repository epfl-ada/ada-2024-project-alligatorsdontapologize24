import os
import pandas as pd

def preprocess_files_in_directory(base_dir, verbose=True):
    """
    Preprocess files in a specified directory by renaming each file to lowercase
    and standardizing all column names in CSV files to lowercase. This function
    is useful for normalizing file and column formats to simplify data processing.

    Parameters:
    ----------
    base_dir : str
        The path to the base directory containing year-based folders (e.g., 'AL-1991', 'AL-1992').
        Each folder is expected to contain CSV files with potentially inconsistent naming conventions.
    
    Returns:
    -------
    None
        The function modifies files in place. Renamed files and standardized column names
        are saved back to the original files.

    Example:
    -------
    preprocess_files_in_directory('../../data/RAW/Alabama')
    """
    # Iterate through each folder in the base directory
    # Each folder corresponds to a specific year, such as 'AL-1991'
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        
        # Check if the current item is a directory and starts with "AL-"
        if os.path.isdir(folder_path) and folder.startswith("AL-"):
            # Process each file within the folder
            for filename in os.listdir(folder_path):
                # Define the full path of the original file
                original_file_path = os.path.join(folder_path, filename)
                
                # Convert the filename to lowercase to normalize naming conventions
                new_filename = filename.lower()
                new_file_path = os.path.join(folder_path, new_filename)
                
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
