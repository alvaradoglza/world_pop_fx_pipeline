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
    """
    Client/class to retrieve the population data from the WBI API

    """
   
    def latest_population(self, top_n: int | None = None) -> pd.DataFrame:
        """
        Fetch data and return a DataFrame of countries sorted by descending population.

        Args:
            top_n: If provided, limit to the top N countries by population.
                   Otherwise, return all countries.

        Returns:
            pd.DataFrame with columns:
                - iso3:  Three-letter country code (ISO-3)
                - country: Full country name
                - year: The year of the population data
                - population: Population count as an integer

            Sorted by `population` in descending order.

        Raises:
            RuntimeError: If the underlying HTTP call fails.
            KeyError:     If expected fields are missing from the API response.
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
        Get ISO-3 codes for countries.

        Calls the '/country' endpoint once and caches the result.

        Returns:
            A set of ISO-3 codes (e.g. "USA", "MEX") for all entities
            whose 'region.id' ≠ "NA".

        Raises:
            RuntimeError: If the HTTP call fails or returns an unexpected shape.
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
        Fetch the most-recent population value for every entity.

        Returns:
            A list of dicts, each matching the shape required by
            `PopulationRecord`.

        Raises:
            RuntimeError: If the HTTP call reports failure.
            KeyError:     If the returned JSON doesn’t match the expected format.
        """

        url = (
            f"{config.WORLD_BANK_BASE}/country/all/indicator/"
            f"{config.POPULATION_INDICATOR}"
        )
        params = {"format": "json", "mrv": 1, "per_page": config.PER_PAGE}

        payload = get_json(url, params=params)
        _, data = payload
        return data
