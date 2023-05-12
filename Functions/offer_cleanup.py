"""
This module will contain code necessary to preprocess and prepare 
offerwall data for ingestion by our database.
"""

import pandas as pd
import numpy as np

def clean_ayet(ayet_dataframe):
    """
    This function cleans and prepares
    the informations retrieve from the
    Ayet offerwall.

    Parameters
    ----------
        ayet_dataframe: `pandas.DataFrame`
            A pandas Dataframe containing offer information from the
            Ayet offerwall.

    Returns
    -------
        clean_ayet_dataframe: `pandas.DataFrame`
            A pandas DataFrame containing the cleaned and processed
            offer information from the Ayet offerwall.
    """

    keyword_list = ['Multiple rewards']
    # Add proper description from the 'Additonal' column instead of
    # a generic 'Mulitple rewards' description.
    for index,row in ayet_dataframe.iterrows():
        if row['Description'] in keyword_list:
            row['Description'] = row['Additional']

    # Drop unneeded columns from the dataframe.
    ayet_dataframe = ayet_dataframe.drop(['offerLow','Additional','Difficulty','Ignore3'], axis=1)

    # Drop rows containing 'None' values as these rows represent
    # duplicate data.
    ayet_dataframe = ayet_dataframe.dropna()

    return ayet_dataframe