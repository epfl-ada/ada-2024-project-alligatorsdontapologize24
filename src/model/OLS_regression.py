import numpy as np
import pandas as pd
from statsmodels.stats import diagnostic
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.regression.linear_model import RegressionResultsWrapper

from statsmodels.tsa.ardl import select_order



def OLS_regression(violence:pd.DataFrame, box_revenues_violent: pd.DataFrame, unemployment_rate: pd.DataFrame) -> RegressionResultsWrapper:

    """
    Creates and returns a statsmodels ARDL model.
    
    Parameters:
    - dependent: pandas Series of real-world violence score
    - independent: pandas DataFrame of box office revenues of films classified as violent, pandas DataFrame of unemploymnet rate
    
    Returns:
    - A statsmodels OLS RegressionResultsWrapper object
    """

    # Sum up the box office revenues of all violent films per week
    weekly_revenues = box_revenues_violent.groupby(["Year", "Week"])["box_office_revenue"].sum()

    # PREPROCESSING OF UNEMPLOYMENT RATE DATAFRAME? -> MUST ALSO BE IN WEEKLY NUMBERS IN THE SAME TIMESPAN

    # PREPROCESSING OF VIOLENCE DATAFRAME? -> MUST ALSO BE IN WEEKLY NUMBERS IN THE SAME TIMESPAN

    # Concatenate the two exogenous variables
    EXOG = pd.concat([weekly_revenues, weekly_unemployment], axis=1)


    # ----------------------- Model definition for auto-regressive distributed lag model ----------------- #

    # Setting the time frame for the auto-regressive part
    max_auto_lag = 4            # take into account max. 4 previous timesteps

    # Setting the time span for the distributed lag part
    max_film_lag = 4            # take into account max. 4 previous timesteps
    max_unemployment_lag = 1    # take into account max 1 previous timestep

    # Include time-fixed effects
    time_fixed = True

    # Include additional confounding factors
    include_confounding = True

    # INCLUDE TIME DUMMY VARIABLES FOR TIME FIXED EFFECTS?

    # Get indicator variables for the year-week
    EXOG["Year-Week"] = EXOG["Year"] + "-" + EXOG["Week"]

    # Create time dummies for weekly time-fixed effects
    time_dummies = pd.get_dummies(EXOG["Year-Week"], drop_first=True)
    EXOG_with_dummies = pd.concat([EXOG, time_dummies], axis=1)

    # --------------------------------------- Set up select_order --------------------------------------- #

    # Automatically select lag order based on AIC
    selected_order = select_order(violence['violence_score'], EXOG_with_dummies, maxlag=max_auto_lag, maxorder={'box_office_revenue':max_film_lag,'unemployment_rate':max_unemployment_lag}, ic='aic')

    # Fit ARDL model with the selected order
    model = selected_order.model
    

    return model