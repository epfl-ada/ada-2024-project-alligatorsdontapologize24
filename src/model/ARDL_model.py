import pandas as pd
from statsmodels.regression.linear_model import RegressionResultsWrapper
from statsmodels.tsa.ardl import ardl_select_order
from statsmodels.tsa.ardl import ARDL
import os
import warnings

from typing import Tuple


def ARDL_model_func(
    box_revenues_violent: pd.DataFrame,
    real_violence: pd.DataFrame,
    time_fixed_effects: bool = False,
) -> RegressionResultsWrapper:
    
    """
    Creates and returns a fitted statsmodels ARDL model.

    Args:
    - box_revenues_violent: pandas DataFrame of box office revenues of films classified as violent
    - real_violence: pandas DataFrame of real-world violence score
    - time_fixed_effects: include time-fixed effects in the model or not

    Returns:
    - RegressionResultsWrapper: A fitted statsmodels ARDL model
    """
    
    # ---------------------------------- Preprocess the box_revenues_violent data ------------------------------ #

    # Drop all lines containing NaN
    box_revenues_clean = box_revenues_violent.dropna()

    # Sum up the box office revenues of all violent films per week
    weekly_revenues = (
        box_revenues_clean.groupby(["Year", "Week"])["Box office revenue"]
        .sum()
        .reset_index()
    )

    # Count the number of films released per week
    weekly_no_films = (
        box_revenues_clean.groupby(["Year", "Week"])
        .size()
        .reset_index(name="no. films released")
    )

    # Merge both in one dataframe
    weekly_films_revenues = pd.merge(
        weekly_no_films, weekly_revenues, on=["Year", "Week"], how="left"
    )

    # Sort by year and week (from old to young)
    weekly_films_revenues_sorted = weekly_films_revenues.sort_values(
        ["Year", "Week"], ascending=True
    )

    # ------------------------------------- Preprocess the violence data --------------------------------------- #

    # sum up violence counts for all states provided (grouped by year and week) to have one final violence score
    weekly_violence_USA = (
        real_violence.groupby(["Year", "Week"])["Violence_score"].sum().reset_index()
    )

    # Sort by year and week (from old to young)
    weekly_violence_USA = weekly_violence_USA.sort_values(
        ["Year", "Week"], ascending=True
    )

    # -------------------------------- Match the different datasets in size ------------------------------------ #

    # real_violence dataset: find starting and ending year of data
    year_start = weekly_violence_USA["Year"].min()
    year_stop = weekly_violence_USA["Year"].max()

    # box_revenues_violent dataset: we do not have all weeks in 2012 -> find the ending week of data
    df_temp = weekly_films_revenues_sorted[weekly_films_revenues_sorted["Year"] == 2012]
    week_stop_2012 = df_temp["Week"].max()

    # box_revenues_violent dataset: cut time span in years to match real_violence dataset
    weekly_films_revenues_sorted_cut = weekly_films_revenues_sorted[
        (weekly_films_revenues_sorted["Year"] >= year_start)
        & (weekly_films_revenues_sorted["Year"] <= year_stop)
    ]

    # real_violence dataset: cut weekly time span in year 2012 to only contain values until week 42 of 2012 (included)
    weekly_violence_USA_cut = weekly_violence_USA[
        (weekly_violence_USA["Year"] < 2012)
        | (
            (weekly_violence_USA["Year"] == 2012)
            & (weekly_violence_USA["Week"] <= week_stop_2012)
        )
    ]

    # --------------------------------------- Merge the two dataframes ----------------------------------------- #

    merged_violence = pd.merge(
        weekly_violence_USA_cut,
        weekly_films_revenues_sorted_cut,
        on=["Year", "Week"],
        how="left",
    )

    # Non-existing lines in weekly_films_revenues_sorted_cut: no films published, zero box office revenue -> fill with 0
    merged_violence["no. films released"] = (
        merged_violence["no. films released"].fillna(0).astype(int)
    )
    merged_violence["Box office revenue"] = (
        merged_violence["Box office revenue"].fillna(0).astype(int)
    )

    # Assure correct sorting in merged dataframe
    merged_violence = merged_violence.sort_values(["Year", "Week"], ascending=True)

    # --------------------------- Create biweekly time dummies for time-fixed effects -------------------------- #

    # Get Year-Week identifier
    merged_violence["Year-Week"] = (
        merged_violence["Year"].astype(str) + "-" + merged_violence["Week"].astype(str)
    )

    # Compute biweek number (to reduce the number of regressors)
    merged_violence["BiWeek"] = ((merged_violence["Week"] - 1) // 2) + 1

    # Combine year and biweek number into Year-BiWeek identifier
    merged_violence["Year-BiWeek"] = (
        merged_violence["Year"].astype(str)
        + "-B"
        + merged_violence["BiWeek"].astype(str)
    )

    # Create time dummies for biweekly time-fixed effects
    time_dummies = pd.get_dummies(
        merged_violence["Year-BiWeek"], drop_first=True
    ).astype(int)

    # ------------------------ Separate data in ENDOG and EXOG (excluding time dummies) ------------------------ #

    # endogenous (dependent variable)
    ENDOG = merged_violence["Violence_score"]

    # exogenous (independent variables, not including time-fixed effect dummies)
    # EXOG = merged_violence.drop(columns=["Year-Week", "BiWeek", "Year-BiWeek", "Year", "Week", "Violence_score", "no. films released"])
    EXOG = merged_violence.drop(
        columns=["Year-Week", "BiWeek", "Year-BiWeek", "Year", "Week", "Violence_score"]
    )

    # ---------------------------------------- Optimal lag search ---------------------------------------------- #

    # Setting the time frame for the auto-regressive part
    max_auto_lag = 6  # take into account max. 6 previous timesteps (6 previous weeks)

    # Setting the time span for the distributed lag part
    max_distr_lag = 6  # take into account max. 6 previous timesteps (6 previous weeks)

    # find best order for lags
    selected_order = ardl_select_order(
        endog=ENDOG, exog=EXOG, maxlag=max_auto_lag, maxorder=max_distr_lag, ic="aic"
    )

    # ---------------------------------------- Create optimal ARDL model ---------------------------------------- #

    # create ARDL model and fit to data (include biweekly time fixed effects or not according to time_fixed_effects)

    with warnings.catch_warnings():

        warnings.filterwarnings("ignore")

        if time_fixed_effects == True:

            ARDL_model = ARDL(
                endog=ENDOG,
                exog=EXOG,
                lags=selected_order.ar_lags,
                order=selected_order.dl_lags,
                fixed=time_dummies,
                trend="c",
            ).fit()

        else:

            ARDL_model = ARDL(
                endog=ENDOG,
                exog=EXOG,
                lags=selected_order.ar_lags,
                order=selected_order.dl_lags,
                trend="c",
            ).fit()

    return ARDL_model


def ARDL_states_separate(
    directory_path: str,
    box_revenues_violent: pd.DataFrame,
    consecutive_years_per_state: pd.DataFrame,
    ARDL_model_func,
    time_fixed_effects: bool = False,
) -> dict:
    """
    Iterates through the directory where we store the CSV files with state-specific violence scores over years,
    loads every file into a dataframe and fits the optimal ARDL model for this state.

    Args:
    - directory_path: path to the directory where the CSV files are stored
    - box_revenues_violent: box office revenues of all violent films in the US from CMU and Kaggle dataset
    - consecutive_years_per_state: dataframe containing a timespan for each state where we consecutively have data
    - ARDL_model_func: function for optimal ARDL model fitting (see above)
    - time_fixed_effects: include time-fixed effects in the models or not

    Returns:
    - dict: a dictionary of fitted ARDL models, the key is composed of ARDL_"state_name"
    """

    fitted_ARDL_models = {}

    # Iterate through directory
    for filename in os.listdir(directory_path):

        # Check for .csv extension
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)

            # Extract state name (everything before first "_")
            state_name = filename.split("_")[0]
            dict_key = f"ARDL_{state_name}"

            # Load into dataframe
            real_violence_per_state = pd.read_csv(file_path, sep=",")

            # Search for correct state info on the consecutive years
            state_info = consecutive_years_per_state[
                consecutive_years_per_state["state"] == state_name
            ]

            if not state_info.empty:
                # Get consecutive years time span for the current state
                min_year = state_info["minimum_year"].values[0]
                max_year = state_info["maximum_year"].values[0]

                # Filter the dataframe for those values
                real_violence_per_state = real_violence_per_state[
                    (real_violence_per_state["Year"] >= min_year)
                    & (real_violence_per_state["Year"] <= max_year)
                ]

            # Fit optimal ARDL model
            fitted_ARDL_current = ARDL_model_func(
                box_revenues_violent, real_violence_per_state, time_fixed_effects
            )

            # Store ARDL model in the dictionary
            fitted_ARDL_models[dict_key] = fitted_ARDL_current

    return fitted_ARDL_models


def ARDL_model_func_jade(
    box_revenues_violent: pd.DataFrame,
    real_violence: pd.DataFrame,
    time_fixed_effects: bool = False,
) -> RegressionResultsWrapper:
    """
    Creates and returns a statsmodels ARDL model using the normalised box office revenues.

    Args:
    - box_revenues_violent (pd.DataFrame): The input dataset containing box office revenues of violent films.
    - real_violence (pd.DataFrame): The input dataset containing real-world violence scores.
    - time_fixed_effects (bool): Whether to include time-fixed effects in the model.

    Returns:
    - RegressionResultsWrapper: A fitted statsmodels ARDL model.
    """

    # ---------------------------------- Preprocess the box_revenues_violent data ------------------------------ #

    # Drop all lines containing NaN
    # box_revenues_clean = box_revenues_violent.dropna()

    # Sum up the box office revenues of all violent films per week
    # weekly_revenues = box_revenues_clean.groupby(["Year", "Week"])["Box office revenue"].sum().reset_index()

    # Count the number of films released per week
    # weekly_no_films = box_revenues_clean.groupby(["Year", "Week"]).size().reset_index(name="no. films released")

    # Merge both in one dataframe
    # weekly_films_revenues = pd.merge(weekly_no_films, weekly_revenues, on=["Year", "Week"], how="left")

    # Sort by year and week (from old to young)
    weekly_films_revenues_sorted = box_revenues_violent.sort_values(
        ["Year", "Week"], ascending=True
    )

    # ------------------------------------- Preprocess the violence data --------------------------------------- #

    # sum up violence counts for all states provided (grouped by year and week) to have one final violence score
    weekly_violence_USA = (
        real_violence.groupby(["Year", "Week"])["Violence_score"].sum().reset_index()
    )

    # Sort by year and week (from old to young)
    weekly_violence_USA = weekly_violence_USA.sort_values(
        ["Year", "Week"], ascending=True
    )

    # -------------------------------- Match the different datasets in size ------------------------------------ #

    # real_violence dataset: find starting and ending year of data
    year_start = weekly_violence_USA["Year"].min()
    year_stop = weekly_violence_USA["Year"].max()

    # box_revenues_violent dataset: we do not have all weeks in 2012 -> find the ending week of data
    df_temp = weekly_films_revenues_sorted[weekly_films_revenues_sorted["Year"] == 2012]
    week_stop_2012 = df_temp["Week"].max()

    # box_revenues_violent dataset: cut time span in years to match real_violence dataset
    weekly_films_revenues_sorted_cut = weekly_films_revenues_sorted[
        (weekly_films_revenues_sorted["Year"] >= year_start)
        & (weekly_films_revenues_sorted["Year"] <= year_stop)
    ]

    # real_violence dataset: cut weekly time span in year 2012 to only contain values until week 42 of 2012 (included)
    weekly_violence_USA_cut = weekly_violence_USA[
        (weekly_violence_USA["Year"] < 2012)
        | (
            (weekly_violence_USA["Year"] == 2012)
            & (weekly_violence_USA["Week"] <= week_stop_2012)
        )
    ]

    # --------------------------------------- Merge the two dataframes ----------------------------------------- #

    merged_violence = pd.merge(
        weekly_violence_USA_cut,
        weekly_films_revenues_sorted_cut,
        on=["Year", "Week"],
        how="left",
    )

    # Non-existing lines in weekly_films_revenues_sorted_cut: no films published, zero box office revenue -> fill with 0
    # merged_violence["no. films released"] = merged_violence["no. films released"].fillna(0).astype(int)
    merged_violence["Metric"] = merged_violence["Metric"].fillna(0).astype(int)

    # Assure correct sorting in merged dataframe
    merged_violence = merged_violence.sort_values(["Year", "Week"], ascending=True)

    # --------------------------- Create biweekly time dummies for time-fixed effects -------------------------- #

    # Get Year-Week identifier
    merged_violence["Year-Week"] = (
        merged_violence["Year"].astype(str) + "-" + merged_violence["Week"].astype(str)
    )

    # Compute biweek number (to reduce the number of regressors)
    merged_violence["BiWeek"] = ((merged_violence["Week"] - 1) // 2) + 1

    # Combine year and biweek number into Year-BiWeek identifier
    merged_violence["Year-BiWeek"] = (
        merged_violence["Year"].astype(str)
        + "-B"
        + merged_violence["BiWeek"].astype(str)
    )

    # Create time dummies for biweekly time-fixed effects
    time_dummies = pd.get_dummies(
        merged_violence["Year-BiWeek"], drop_first=True
    ).astype(int)

    # ------------------------ Separate data in ENDOG and EXOG (excluding time dummies) ------------------------ #

    # endogenous (dependent variable)
    ENDOG = merged_violence["Violence_score"]

    # exogenous (independent variables, not including time-fixed effect dummies)
    # EXOG = merged_violence.drop(columns=["Year-Week", "BiWeek", "Year-BiWeek", "Year", "Week", "Violence_score", "no. films released"])
    EXOG = merged_violence.drop(
        columns=["Year-Week", "BiWeek", "Year-BiWeek", "Year", "Week", "Violence_score"]
    )

    # ---------------------------------------- Optimal lag search ---------------------------------------------- #

    # Setting the time frame for the auto-regressive part
    max_auto_lag = 20  # take into account max. 6 previous timesteps (6 previous weeks)

    # Setting the time span for the distributed lag part
    max_distr_lag = 20  # take into account max. 6 previous timesteps (6 previous weeks)

    # find best order for lags
    selected_order = ardl_select_order(
        endog=ENDOG, exog=EXOG, maxlag=max_auto_lag, maxorder=max_distr_lag, ic="aic"
    )

    # ---------------------------------------- Create optimal ARDL model ---------------------------------------- #

    # create ARDL model and fit to data (include biweekly time fixed effects or not according to time_fixed_effects)

    with warnings.catch_warnings():

        warnings.filterwarnings("ignore")

        if time_fixed_effects == True:

            ARDL_model = ARDL(
                endog=ENDOG,
                exog=EXOG,
                lags=selected_order.ar_lags,
                order=selected_order.dl_lags,
                fixed=time_dummies,
                trend="c",
            ).fit()

        else:

            ARDL_model = ARDL(
                endog=ENDOG,
                exog=EXOG,
                lags=selected_order.ar_lags,
                order=1,
                # order=selected_order.dl_lags,
                trend="c",
            ).fit()

    return ARDL_model


def extraction_violence_data(
    data,
    year,
    start_week,
    stop_week,
    window_size=6,
    offenses=[
        "Assault Offenses",
        "Larceny/Theft Offenses",
        "Robbery",
        "Sex Offenses",
        "Kidnapping/Abduction",
        "Arson",
        "Homicide Offenses",
    ],
):
    """
     Extracts and summarizes violence-related data for specified offenses over a defined time period.

    Args:
     data (pd.DataFrame): The input dataset containing offense information.
     year (int): The year for which to extract data.
     start_week (int): The starting week number for the period of interest.
     stop_week (int): The ending week number for the period of interest.
     window_size (int): The number of weeks to consider for the moving average, default correspond to the maxiumum autolag of the ARDL model.
     offenses (list of str, optional): A list of offense categories to consider.

    Returns:
     pd.DataFrame: A DataFrame summarizing the extracted data between the specified year and weeks of interest.

    """
    extracted_data = data[
        (data.year == year) & (data.week >= start_week) & (data.week <= stop_week)
    ]
    category_size = extracted_data.groupby(
        ["year", "week", "offense_category_name"]
    ).size()
    result_df = category_size.reset_index(name="count_of_offenses")
    return result_df


def normalise_violent_category(extracted_data, offense, window_size=6):
    """
    Computes rolling z-score normalization for a specific offense category.
    Args:
        extracted_data (pd.DataFrame): A DataFrame containing offense data
        offense (str): The name of the offense category to normalize
        window_size (int, optional): The size of the rolling window for calculating the mean and standard deviation, correspond to maximum autolag of ARLD model.
    Returns:
        pd.DataFrame: A DataFrame containing the normalized data for the specified offense category.
    """

    if offense in extracted_data["offense_category_name"].values:
        extracted_category = extracted_data[
            extracted_data.offense_category_name == offense
        ].copy()
        rolling_mean = extracted_category.count_of_offenses.rolling(
            window=window_size, min_periods=1
        ).mean()
        rolling_std = (
            extracted_category.count_of_offenses.rolling(
                window=window_size, min_periods=1
            )
            .std()
            .fillna(1)
        )  # avoid division by 0 and enable to have 0 as z-score since z-score not applicable in that case
        extracted_category.loc[:, "z_score"] = (
            extracted_category.count_of_offenses - rolling_mean
        ) / rolling_std
    else:
        extracted_category = pd.DataFrame()
    return extracted_category


def real_life_violence_score_z_score(
    data,
    year,
    start_week,
    stop_week,
    window_size=6,
    offenses=[
        "Assault Offenses",
        "Robbery",
        "Sex Offenses",
        "Kidnapping/Abduction",
        "Arson",
        "Homicide Offenses",
    ],
):
    """
    Computes the z-score normalized violence score for specific offense categories over a time window.

    This function extracts data within a specified range of weeks and years, normalizes the offense counts
    by calculating their z-scores for each category, and returns the processed dataset.

     Args:
        data (pd.DataFrame): The input dataset containing offense information.
        year (int): The year for which to calculate the violence scores.
        start_week (int): The starting week of the period for analysis.
        stop_week (int): The ending week of the period for analysis.
        window_size (int, optional): The rolling window size for normalization, must correspond to the maximum autolag of the ARDL model.
        offenses (list[str], optional): The list of offense categories to consider for analysis.


    Returns:
        pd.DataFrame: A DataFrame containing the z-score normalized data

    """
    extracted_data = extraction_violence_data(
        data, year, start_week, stop_week, window_size
    )
    data_with_z_score = pd.DataFrame(
        columns=[
            "year",
            "week",
            "offense_category_name",
            "count_of_offenses",
            "z_score",
        ]
    )
    for offense in offenses:
        z_score_category = normalise_violent_category(
            extracted_data, offense, window_size
        )
        if not z_score_category.empty:  # check if the category is not empty
            data_with_z_score = pd.concat([data_with_z_score, z_score_category], axis=0)

    return data_with_z_score


def violence_score_z_score_aggregated(
    data,
    year,
    start_week,
    stop_week,
    window_size=6,
    offenses=[
        "Assault Offenses",
        "Robbery",
        "Sex Offenses",
        "Kidnapping/Abduction",
        "Arson",
        "Homicide Offenses",
    ],
):
    """
     Computes the aggregated z-score for violence across multiple offense categories over a specified time range.
     Args:
         data (pd.DataFrame): A DataFrame containing offense data
          year (int): The year for which to compute the aggregated z-scores.
         start_week (int): The starting week of the analysis period.
         stop_week (int): The ending week of the analysis period.
         window_size (int, optional): The rolling window size for calculating z-scores.
          offenses (list of str, optional): A list of offense categories to consider.
    Returns:
         pd.DataFrame: A DataFrame containing the aggregated z-scores
    """
    z_score_per_category = real_life_violence_score_z_score(
        data, year, start_week, stop_week, window_size, offenses
    )
    z_score_aggregated = z_score_per_category.groupby(["year", "week"]).z_score.sum()
    result_df = z_score_aggregated.reset_index(name="z_score_aggregated")
    return result_df


def z_score_all_states_merged(
    directory_path: str,
    start_year: int,
    end_year: int,
    start_week: int,
    stop_week: int,
    window_size: int = 6,
    offenses: list = [
        "Assault Offenses",
        "Robbery",
        "Sex Offenses",
        "Kidnapping/Abduction",
        "Arson",
        "Homicide Offenses",
    ],
) -> dict:
    
    """
    Iterates through the directory where we store the CSV files with state-specific violence scores (counts),
    loads every file into a dataframe and computes the z-score for the aggregated violence score for each state.
    
    Args:
    - directory_path (str): The path to the directory where the CSV files are stored.
    - start_year (int): The starting year for the analysis.
    - end_year (int): The ending year for the analysis.
    - start_week (int): The starting week of the analysis period.
    - stop_week (int): The ending week of the analysis period.
    - window_size (int, optional): The rolling window size for calculating z-scores (set as 6 to be identical to max. AR lag).
    - offenses (list of str, optional): A list of offense categories to consider.

    Returns:
    - dict: A dictionary containing the z-scores for the aggregated violence scores for all states merged.

    """

    z_scores_per_state = {}

    # Iterate through directory
    for filename in os.listdir(directory_path):

        state_z_list_years = []

        # Check for .csv extension
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)

            # Extract state name (everything before first "_")
            state_name = filename.split("_")[0]
            dict_key = f"ARDL_{state_name}"

            # Load into dataframe
            real_violence_per_state = pd.read_csv(file_path, sep=",")

            with warnings.catch_warnings():

                warnings.filterwarnings("ignore")

                for year in range(start_year, end_year + 1):

                    # z-score for this state for this year
                    df_z = violence_score_z_score_aggregated(
                        real_violence_per_state, year, start_week, stop_week
                    )

                    state_z_list_years.append(df_z)

                # store in dict
                z_scores_per_state[dict_key] = pd.concat(
                    state_z_list_years, axis=0, ignore_index=True
                )

    # Concatenate all dataframes for all states
    z_scores_concat = pd.concat(z_scores_per_state.values(), ignore_index=True)

    # Group by "Year" and "Week", sum up the z-scores
    z_scores_merged = z_scores_concat.groupby(["year", "week"], as_index=False).agg(
        {"z_score_aggregated": "sum"}
    )

    # Renaming the columns for consistency
    z_scores_merged.columns.values[0] = "Year"
    z_scores_merged.columns.values[1] = "Week"
    z_scores_merged.columns.values[2] = "Violence_score"

    return z_scores_merged


def real_life_violence_score_count(
        data: pd.DataFrame, 
        year: int, 
        start_week: int, 
        stop_week: int, 
        ratio: bool = False
        ) -> pd.DataFrame:
    
    """
    Extracts the count or ratio of real-world violence offenses from the provided dataset for a specific time period.

    Args:
    - data (pd.DataFrame): The input dataset containing real-world violence offenses.
    - year (int): The year for which to extract the data.
    - start_week (int): The starting week of the period for analysis.
    - stop_week (int): The ending week of the period for analysis.
    - ratio (bool): Whether to return the ratio of violence score to total counts.

    Returns:
    - pd.DataFrame: A DataFrame containing the extracted real-life violence scores for the specified year and time period.
    """

    extracted_data = data[(data.year==year) & (data.week >=start_week) & (data.week <=stop_week)]
    weekly_score = extracted_data.groupby("week").size()
    if ratio: 
        weekly_score/=len(extracted_data)

    return weekly_score


def violence_score_all_states_count(
    directory_path: str, 
    start_year: int, 
    end_year: int, 
    start_week: int, 
    stop_week: int, 
    ratio: bool = False, 
    offenses: list = ['Assault Offenses', 'Robbery', 'Sex Offenses', 'Kidnapping/Abduction', 'Arson', 'Homicide Offenses']
    ) -> pd.DataFrame:
   
    """
    Iterates through the directory where we store the CSV files with state-specific violence scores (counts),
    loads every file into a dataframe and computes the real-life violence score for each state.

    Args:
    - directory_path (str): The path to the directory where the CSV files are stored.
    - start_year (int): The starting year for the analysis.
    - end_year (int): The ending year for the analysis.
    - start_week (int): The starting week of the analysis period.
    - stop_week (int): The ending week of the analysis period.
    - ratio (bool, optional): Whether to return the ratio of violence score to total counts.
    - offenses (list of str, optional): A list of offense categories to consider.

    Returns:
    - pd.Dataframe: A dataframe containing the real-life violence scores for all states merged.
    """

    violence_scores_per_state = {}

    # Iterate through directory
    for filename in os.listdir(directory_path):

        state_scores_years = []

        # Check for .csv extension
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)

            # Extract state name (everything before first "_")
            state_name = filename.split("_")[0]
            dict_key = f"ARDL_{state_name}"

            # Load into dataframe
            real_violence_per_state = pd.read_csv(file_path, sep=",")

            with warnings.catch_warnings():

                warnings.filterwarnings("ignore")

                for year in range(start_year, end_year + 1):

                    # Compute real-life violence score for this state and year
                    weekly_score = real_life_violence_score_count(real_violence_per_state, year, start_week, stop_week, ratio)

                    # Convert to DataFrame
                    weekly_score_df = weekly_score.reset_index(name='violence_score')
                    weekly_score_df['year'] = year
                    state_scores_years.append(weekly_score_df)

                # Store in dict
                violence_scores_per_state[dict_key] = pd.concat(state_scores_years, axis=0, ignore_index=True)

    # Concatenate all dataframes for all states
    violence_scores_concat = pd.concat(violence_scores_per_state.values(), ignore_index=True)

    # Group by "Year" and "Week", sum up the violence scores
    violence_scores_merged = violence_scores_concat.groupby(["year", "week"], as_index=False).agg({"violence_score": "sum"})

    # Renaming the columns for consistency
    violence_scores_merged.columns.values[0] = "Year"
    violence_scores_merged.columns.values[1] = "Week"
    violence_scores_merged.columns.values[2] = "Violence_score"

    return violence_scores_merged



def extract_model_results(
    model: ARDL, 
    model_name: str, 
    file_path: str
    ) -> pd.DataFrame:

    """
    Extracts the coefficients, standard errors, p-values, and confidence intervals from a statsmodels ARDL model.
    Excludes variables whose names start with a number (to avoid including the time-fixed effects in the coefficient table)

    Args:
    - model (ARDL): The fitted ARDL model.
    - model_name (str): The name of the model for saving the file.
    - file_path (str): The path where the result is saved.

    Returns:
    - pd.DataFrame: A DataFrame containing the variables, coefficients, standard errors, p-values, and confidence intervals.
    """

    # Extract the model summary data
    summary_data = model.summary().tables[1].data 
    columns = summary_data[0]
    rows = summary_data[1:]
    
    # Convert summary data into a pandas DataFrame
    raw_results = pd.DataFrame(rows, columns=columns)
    raw_results = raw_results.rename(columns={raw_results.columns[0]: "Variable"})
    
    # Exclude rows where the "Variable" starts with a number (== drop all time-fixed effect coefficients, since we are not interested in them)
    raw_results = raw_results[~raw_results["Variable"].str.match(r'^\d')]
    
    # Extract only the relevant columns for the analysis
    results = raw_results[["Variable", "coef", "std err", "P>|z|"]].copy()
    results.columns = ["variable", "coefficient", "std_err", "p_value"]

    # Convert numerical columns to proper numeric types for further analysis
    results[["coefficient", "std_err", "p_value"]] = results[["coefficient", "std_err", "p_value"]].apply(pd.to_numeric, errors="coerce")

    # Calculate 95% confidence intervals
    results["lower_ci"] = results["coefficient"] - 1.96 * results["std_err"]
    results["upper_ci"] = results["coefficient"] + 1.96 * results["std_err"]

    # Define path to save HTML file
    save_path = file_path + model_name.replace(' ', '_') + ".html"

    # Save the dataframe as an HTML table
    html_table = results.to_html(classes='table table-striped table-bordered', index=False)

    # Write the HTML table to the file
    with open(save_path, 'w') as file:
        file.write(html_table)

    return results