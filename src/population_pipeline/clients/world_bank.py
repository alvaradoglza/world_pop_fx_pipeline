"""
WorldBankClient, handling of the Indicators API
"""

from __future__ import annotations

from functools import cached_property
from typing import List

import pandas as pd

from population_pipeline import config
from population_pipeline.models.population import PopulationRecord
from population_pipeline.utils.http import get_json


class WorldBankClient:

   
    def latest_population(self, top_n: int | None = None) -> pd.DataFrame:
        """
        Return a DataFrame of countries sorted by descending population.

        Calls to the _fetch_population_rows method to get the latest population data
        for all countries, filters out those with no population value and creates a dataframe with that info result
        """

        raw = self._fetch_population_rows()

        records: List[PopulationRecord] = [
            PopulationRecord(**row)
            for row in raw
            if row["value"] is not None
            and row["countryiso3code"] in self.country_iso3_set
        ]

        df = (
            pd.DataFrame(
                {
                    "iso3": [r.iso3 for r in records],
                    "country": [r.name for r in records],
                    "year": [r.date for r in records],
                    "population": [r.value for r in records],
                }
            )
            .sort_values("population", ascending=False)
            .reset_index(drop=True)
        )

        return df.head(top_n) if top_n else df


    @cached_property
    def country_iso3_set(self) -> set[str]:
        """
        ISO-3 codes for real countries only (excludes aggregates).
        """

        url = f"{config.WORLD_BANK_BASE}/country"
        payload = get_json(url, params={"format": "json", "per_page": 400})


        _, countries = payload
        return {
            row["id"]
            for row in countries
            if row["region"]["id"] != "NA"    
        }

    def _fetch_population_rows(self) -> list[dict]:
        """
        Get the most-recent population value for every entity.
        """

        url = (
            f"{config.WORLD_BANK_BASE}/country/all/indicator/"
            f"{config.POPULATION_INDICATOR}"
        )
        params = {"format": "json", "mrv": 1, "per_page": config.PER_PAGE}

        payload = get_json(url, params=params)
        _, data = payload
        return data
