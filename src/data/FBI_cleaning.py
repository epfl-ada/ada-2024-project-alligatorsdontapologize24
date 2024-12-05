import pandas as pd
import os

def filter_violent_offenses(merged_dir, violence_dir, violent_categories):
    """
    Filters files in CLEAN/FBI_merged to keep only violent offenses and saves the result to CLEAN/FBI_violence.

    Parameters:
    ----------
    merged_dir : str
        Path to the directory containing merged files.
    violence_dir : str
        Path to the directory where filtered files will be saved.
    violent_categories : list
        List of offense categories considered violent.

    Returns:
    -------
    None
    """
    # Ensure the output directory exists
    if not os.path.exists(violence_dir):
        os.makedirs(violence_dir)

    # Iterate through each file in the merged directory
    for file_name in os.listdir(merged_dir):
        file_path = os.path.join(merged_dir, file_name)

        # Check if it's a CSV file
        if os.path.isfile(file_path) and file_name.endswith('.csv'):
            print(f"Processing file: {file_name}...")

            # Read the data
            try:
                data = pd.read_csv(file_path)

                # Filter for violent offenses
                if 'offense_category_name' in data.columns:
                    filtered_data = data[data['offense_category_name'].isin(violent_categories)]

                    # Save the filtered data
                    output_file_path = os.path.join(violence_dir, file_name)
                    filtered_data.to_csv(output_file_path, index=False)

                    print(f"Dropped {len(data) - len(filtered_data)} non-violent rows. Remaining rows: {len(filtered_data)}")
                else:
                    print(f"'offense_category_name' column not found in {file_name}. Skipping.")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    print("Filtering complete for all files.")


