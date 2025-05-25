"""
Definition of the FXclint to get currency exchante rates.

"""

from __future__ import annotations
import functools
from typing import Dict

from population_pipeline import config
from population_pipeline.utils.http import get_json


class FXClient:
    def __init__(self) -> None:
        if not config.FIXER_KEY:
            raise RuntimeError(
                "FIXER_API_KEY missing, add it to your .env file"
            )
        
    @functools.cached_property
    def _rates_eur(self) -> Dict[str, float]:
        """
        Get the latest exchange rates against EUR.
        Cached function to save the dictionary and avoid re-calling.
        """

        payload = get_json(
            config.FIXER_URL,
            params={
                "access_key": config.FIXER_KEY,
            }
        )
        if not payload.get("success"):
            raise RuntimeError(f"Fixer error: {payload}")
        return payload["rates"]
    
    def to_mxn(self, currency: str) -> float:
        """
        Convert a currency to MXN due to restrictions in the Fixer API.
        
        """

        rates = self._rates_eur
        try:
            eur_to_mxn = rates["MXN"]
            eur_to_cur = rates[currency]
        except KeyError:
            raise KeyError(f"Currency {currency} not found in Fixr paylog")
        return eur_to_mxn / eur_to_cur