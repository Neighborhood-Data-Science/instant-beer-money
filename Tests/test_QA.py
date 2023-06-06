"""
Main Testing Framework to confirm Data Quality
"""

import pandas as pd
import pytest
import os
from dotenv import load_dotenv
import sys
sys.path.append('./Functions')
import adgem_info
import ayet_info
import offertoro_info
import revu_info
import offer_cleanup

#Load environment variables
load_dotenv()
#The environment variables should be present in your CI/CD pipeline
#and/or server side as well.

@pytest.mark.usefixtures("qa_ayet")
class Test_QA_AYET:
    """
    Test suite for the Ayet offerwall.

    This test suite is designed to test the data quality resulting from the `ayet_info.py` file.
    """
    def test_parsed_dataframe_not_empty_ayet(self, qa_ayet):
        """
        Tests if resultant dataframe is not empty.
        """
        assert len(qa_ayet) > 0


    def test_description_replacement(self, qa_ayet):
        """
        Tests if the description is replaced with the title when the value
        is 'Multiple rewards'
        """
        assert qa_ayet.loc[2, 'Description'] == 'Additional 2'

    def test_columns_dropped(self, qa_ayet):
        """
        Tests that unneeded columns were dropped and are not present in the dataframe.
        """
        assert 'offerLow' not in qa_ayet.columns
        assert 'Additional' not in qa_ayet.columns
        assert 'Difficulty' not in qa_ayet.columns
        assert 'Ignore3' not in qa_ayet.columns