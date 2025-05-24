"""
Module A - transform the World Bank data into a streamlit-ready DataFrame
"""

from __future__ import annotations

import pandas as pd

from population_pipeline.clients.world_bank import WorldBankClient

def build_population_df(top_n: int | None = None) -> pd.DataFrame:
    """
    Wrapper to call by streamlit or CLI
    """
    client = WorldBankClient()
    return client.latest_population(top_n=top_n)