import numpy as np
import pandas as pd
from statsmodels.stats import diagnostic
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.regression.linear_model import RegressionResultsWrapper

def OLS_regression(violence:pd.DataFrame, box_revenues_violent: pd.DataFrame, unemployment_rate: pd.DataFrame) -> RegressionResultsWrapper:

    """
    Creates and returns a statsmodels OLS model.
    
    Parameters:
    - dependent: pandas Series of real-world violence score
    - independent: pandas DataFrame of box office revenues of films classified as violent, pandas DataFrame of unemploymnet rate
    
    Returns:
    - A statsmodels OLS RegressionResultsWrapper object
    """

    # ----------------------- Model definition for auto-regressive distributed lag model ----------------- #

    # Setting the time frame for the auto-regressive part
    timespan_violence = 1   # take into account 1 previous timestep

    # Setting the time span for the distributed lag part
    timespan_films = 4      # take into account 4 previous timesteps

    # Include time-fixed effects
    time_fixed = True

    # Include additional confounding factors
    include_confounding = True


    # ------------------------------------------ Set up the model ---------------------------------------- #

    # Declare the model
    model = smf.ols(formula='time ~ C(diabetes) + C(high_blood_pressure)', data=df)

    # Fit the model
    np.random.seed(2)
    model_fitted = model.fit()

    # Print the summary
    #print(res.summary())

    return model_fitted