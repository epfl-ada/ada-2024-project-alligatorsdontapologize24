import pandas as pd

def filter_violent_offenses(data, offense_type_data, verbose=True):
    """
    Filter the final merged dataset to retain only violent offenses.
    Based on violent target et violent offense categories.

    Parameters:
    ----------
    data : pd.DataFrame
        The final dataset containing incident details.
    offense_type_data : pd.DataFrame
        The offense type table containing details about each offense type.
    verbose : bool, optional
        If True, prints the number of rows dropped. Default is True.

    Returns:
    -------
    pd.DataFrame
        A filtered DataFrame containing only violent offenses.
    """
    # Define criteria for violent offenses
    violent_categories = [
        "Assault Offenses", "Homicide Offenses", "Sex Offenses", "Kidnapping/Abduction", "Animal Cruelty"
    ]
    violent_targets = ["Person"]  # Offenses against a person

    # Filter offense types to identify violent offenses
    violent_offenses = offense_type_data[
        (offense_type_data['crime_against'].isin(violent_targets)) |
        (offense_type_data['offense_category_name'].isin(violent_categories))
    ]['offense_type_id']

    if verbose:
        print(f"Identified {len(violent_offenses)} violent offense types.")

    # Filter the Washington dataset to include only violent offenses
    filtered_data = data[data['offense_type_id'].isin(violent_offenses)]

    if verbose:
        print(f"Dropped {len(data) - len(filtered_data)} non-violent rows. Remaining rows: {len(filtered_data)}")

    return filtered_data