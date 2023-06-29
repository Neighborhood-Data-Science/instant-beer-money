"""
This module will contain code necessary to preprocess and prepare 
offerwall data for ingestion by our database.
"""

import re


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
    for index, row in ayet_dataframe.iterrows():
        if row['offer_description'] in keyword_list:
            row['offer_description'] = row['Additional']

    # Drop unneeded columns from the dataframe.
    ayet_dataframe = ayet_dataframe.drop(
        ['offerLow', 'Additional', 'Difficulty', 'Ignore3'], axis=1)

    # Drop rows containing 'None' values as these rows represent
    # duplicate data.
    ayet_dataframe = ayet_dataframe.dropna()

    # Add a new column to the dataframe containing the name of the offerwall.
    ayet_dataframe['offerwall_name'] = 'Ayet'

    return ayet_dataframe


def clean_revu(revu_dataframe):
    """
    This function cleans and prepares
    the informations retrieve from the
    Revenue Universe offerwall.

    Parameters
    ----------
        revu_dataframe: `pandas.DataFrame`
            A pandas Dataframe containing offer information from the
            Revenue Universe offerwall.

    Returns
    -------
        clean_revu_dataframe: `pandas.DataFrame`
            A pandas DataFrame containing the cleaned and processed
            offer information from the Revenue Universe offerwall.
    """

    # Remove commas from values in offer_amount column
    revu_dataframe.loc[:, 'offer_amount'] = revu_dataframe['offer_amount'].str.replace(
        ',', '')

    # Add a new column to the dataframe containing the name of the offerwall.
    revu_dataframe['offerwall_name'] = 'RevU'

    return revu_dataframe


def clean_adgem(adgem_dataframe):
    """
    This function cleans and prepares
    the informations retrieve from the
    Adgem offerwall.

    Parameters
    ----------
        adgem_dataframe: `pandas.DataFrame`
            A pandas Dataframe containing offer information from the
            Adgem offerwall.

    Returns
    -------
        clean_adgem_dataframe: `pandas.DataFrame`
            A pandas DataFrame containing the cleaned and processed
            offer information from the Adgem offerwall.
    """

    # Drop duplicates from the dataframe
    adgem_dataframe = adgem_dataframe.drop_duplicates()

    # Remove commas from values in offer_amount column
    adgem_dataframe.loc[:, 'offer_amount'] = adgem_dataframe['offer_amount'].str.replace(
        ',', '')

    # Return the numerical values only of the offer_amount column
    adgem_dataframe.loc[:, 'offer_amount'] = adgem_dataframe['offer_amount'].apply(
        lambda x: ''.join(re.findall(r'\d+', str(x))))

    # Add a new column to the dataframe containing the name of the offerwall.
    adgem_dataframe = adgem_dataframe.assign(offerwall_name='Adgem')

    return adgem_dataframe


def clean_offertoro(toro_dataframe):
    """
    This function cleans and prepares
    the informations retrieve from the
    Offertoro offerwall.

    Parameters
    ----------
        toro_dataframe: `pandas.DataFrame`
            A pandas Dataframe containing offer information from the
            Offertoro offerwall.

    Returns
    -------
        clean_toro_dataframe: `pandas.DataFrame`
            A pandas DataFrame containing the cleaned and processed
            offer information from the Offertoro offerwall.
    """

    # Define replacement dictionary
    replace_dict = {'android phone': 'Android',
                    'iphone/ipad': 'iOS', 'device': 'Desktop'}

    # Remove and replace the values ' phone' and 'device' from the offer_device column
    toro_dataframe.loc[:, 'offer_device'] = toro_dataframe['offer_device'].replace(
        replace_dict)

    # Declare the refined title list
    refined_title = []

    for vals in toro_dataframe['offer_title']:
        # Returning first element of the split
        splits_ = vals.strip().split('\n')[0]
        # Check if there is a '-' and keep all text up to the '-' marker
        index = splits_.find('-')
        title_split = splits_[:index]
        # Additional strip of text to remove whitespaces
        title_split = title_split.rstrip()
        # Append the title split to the refined title list
        refined_title.append(title_split)

    # Replace the offer_title column with the refined title list
    toro_dataframe.loc[:, 'offer_title'] = refined_title

    # Add a new column to the dataframe containing the name of the offerwall.
    toro_dataframe['offerwall_name'] = 'Offertoro'

    return toro_dataframe
