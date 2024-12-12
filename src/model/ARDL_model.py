import pandas as pd
from statsmodels.regression.linear_model import RegressionResultsWrapper
from statsmodels.tsa.ardl import ardl_select_order
from statsmodels.tsa.ardl import ARDL


def ARDL_model_func(box_revenues_violent: pd.DataFrame, real_violence:pd.DataFrame,  time_fixed_effects=False) -> RegressionResultsWrapper:

    """
    Creates and returns a statsmodels ARDL model.
    
    Parameters:
    - dependent: pandas Series of real-world violence score
    - independent: pandas DataFrame of box office revenues of films classified as violent
    
    Returns:
    - A statsmodels OLS RegressionResultsWrapper object
    """

    # ---------------------------------- Preprocess the box_revenues_violent data ------------------------------ #

    # Drop all lines containing NaN
    box_revenues_clean = box_revenues_violent.dropna()

    # Sum up the box office revenues of all violent films per week
    weekly_revenues = box_revenues_clean.groupby(["Year", "Week"])["Box office revenue"].sum().reset_index()

    # Count the number of films released per week
    weekly_no_films = box_revenues_clean.groupby(["Year", "Week"]).size().reset_index(name="no. films released")

    # Merge both in one dataframe
    weekly_films_revenues = pd.merge(weekly_no_films, weekly_revenues, on=["Year", "Week"], how="left")

    # Sort by year and week (from old to young)
    weekly_films_revenues_sorted = weekly_films_revenues.sort_values(["Year", "Week"], ascending=True)


    # ---------------------------------- Preprocess the unemployment data -------------------------------------- #

    # To Do
    # PREPROCESSING OF UNEMPLOYMENT RATE DATAFRAME? -> MUST ALSO BE IN WEEKLY NUMBERS IN THE SAME TIMESPAN


    # ------------------------------------- Preprocess the violence data --------------------------------------- #

    # sum up violence counts for all states provided (grouped by year and week) to have one final violence score
    weekly_violence_USA = real_violence.groupby(["Year", "Week"])["Violence_score"].sum().reset_index()

    # Sort by year and week (from old to young)
    weekly_violence_USA = weekly_violence_USA.sort_values(["Year", "Week"], ascending=True)


    # -------------------------------- Match the different datasets in size ------------------------------------ #

    # real_violence dataset: find starting and ending year of data
    year_start = weekly_violence_USA["Year"].min()
    year_stop = weekly_violence_USA["Year"].max()

    # box_revenues_violent dataset: we do not have all weeks in 2012 -> find the ending week of data
    df_temp = weekly_films_revenues_sorted[weekly_films_revenues_sorted['Year'] == 2012]
    week_stop_2012 = df_temp['Week'].max()

    # box_revenues_violent dataset: cut time span in years to match real_violence dataset
    weekly_films_revenues_sorted_cut = weekly_films_revenues_sorted[(weekly_films_revenues_sorted["Year"] >= year_start) & (weekly_films_revenues_sorted["Year"] <= year_stop)]

    # real_violence dataset: cut weekly time span in year 2012 to only contain values until week 42 of 2012 (included)
    weekly_violence_USA_cut = weekly_violence_USA[(weekly_violence_USA["Year"] < 2012) | ((weekly_violence_USA["Year"] == 2012) & (weekly_violence_USA["Week"] <= week_stop_2012))]


    # --------------------------------------- Merge the two dataframes ----------------------------------------- #

    merged_violence = pd.merge(weekly_violence_USA_cut, weekly_films_revenues_sorted_cut, on=['Year', 'Week'], how='left')
    
    # Non-existing lines in weekly_films_revenues_sorted_cut: no films published, zero box office revenue -> fill with 0
    merged_violence["no. films released"] = merged_violence["no. films released"].fillna(0).astype(int)
    merged_violence["Box office revenue"] = merged_violence["Box office revenue"].fillna(0).astype(int)

    # Assure correct sorting in merged dataframe
    merged_violence = merged_violence.sort_values(["Year", "Week"], ascending=True)

    # --------------------------- Create biweekly time dummies for time-fixed effects -------------------------- #

    # Get Year-Week identifier
    merged_violence["Year-Week"] = merged_violence["Year"].astype(str) + "-" + merged_violence["Week"].astype(str)

    # Compute biweek number (to reduce the number of regressors)
    merged_violence["BiWeek"] = ((merged_violence["Week"] - 1) // 2) + 1

    # Combine year and biweek number into Year-BiWeek identifier
    merged_violence["Year-BiWeek"] = merged_violence["Year"].astype(str) + "-B" + merged_violence["BiWeek"].astype(str)

    # Create time dummies for biweekly time-fixed effects
    time_dummies = pd.get_dummies(merged_violence["Year-BiWeek"], drop_first=True).astype(int)
    
    # ------------------------ Separate data in ENDOG and EXOG (including time dummies) ------------------------ #

    # endogenous (dependent variable)
    ENDOG = merged_violence["Violence_score"]

    # exogenous (indepent variables, including time-fixed effect dummies)
    EXOG = pd.concat([merged_violence.drop(columns=["Year-Week", "BiWeek", "Year-BiWeek", "Year", "Week", "Violence_score", "no. films released"]), time_dummies], axis=1)


    # ---------------------------------------- Optimal lag search ---------------------------------------------- #

    # Setting the time frame for the auto-regressive part
    max_auto_lag = 6            # take into account max. 6 previous timesteps (6 previous weeks)

    # Setting the time span for the distributed lag part
    max_distr_lag = 6            # take into account max. 6 previous timesteps (6 previous weeks)

    # find best order for lags
    selected_order = ardl_select_order(
        endog=ENDOG, 
        exog=EXOG, 
        maxlag=max_auto_lag, 
        maxorder={"Box office revenue": max_distr_lag}, 
        ic='aic'
    )

    # ---------------------------------------- Create optimal ARDL model ---------------------------------------- #

    # create ARDL model and fit to data (include biweekly time fixed effects or not according to time_fixed_effects)

    if time_fixed_effects == True: 

        ARDL_model = ARDL(
            endog=ENDOG,
            exog=EXOG,
            lags=selected_order.ar_lags,
            order=selected_order.dl_lags,
            fixed=time_dummies,
            trend="ct"
        ).fit()

    else: 

        ARDL_model = ARDL(
            endog=ENDOG,
            exog=EXOG,
            lags=selected_order.ar_lags,
            order=selected_order.dl_lags,
            trend="ct"
        ).fit()
    


    return ARDL_model