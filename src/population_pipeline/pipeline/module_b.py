"""
Module B - fill the population dataframe with the currency, fx and cent data
"""


from __future__ import annotations
import pandas as pd

from population_pipeline.clients.fx import FXClient
from population_pipeline.utils.currency import iso3_to_currency

fx_client = FXClient()

def cent_mxn(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a column with the cent value in MXN for each country.
    """
    
    df = df.copy()
    df["currency"] = df["iso3"].apply(iso3_to_currency)

    def _rate(row):
        code = row["currency"]
        if code is None:
            return None
        try:
            return fx_client.to_mxn(code)
        except KeyError:
            return None
        
    df["fx_to_mxn"] = df.apply(_rate, axis=1)
    df["mxn_from_one_cent"] = df["population"] * 0.01 * df["fx_to_mxn"]

    grand_total = df['mxn_from_one_cent'].sum(skipna=True)


    return df, grand_total
