"""
Definition of the FXclint to get currency exchante rates.

"""

from __future__ import annotations
import functools
from typing import Dict

from population_pipeline import config
from population_pipeline.utils.http import get_json


class FXClient:
    """
    Client/class to interact with the Fixer API.

    """

    def __init__(self) -> None:
        """
        Initialize the FXClient.

        Raises:
            RuntimeError: If the FIXER_API_KEY is not set in config.
        """
    
        if not config.FIXER_KEY:
            raise RuntimeError(
                "FIXER_API_KEY missing, add it to your .env file"
            )
        
    @functools.cached_property
    def _rates_eur(self) -> Dict[str, float]:
        """
        Fetch and save (cache) the latest exchange rates with EUR as the base.

        Raises:
            RuntimeError: If the API response indicates failure.

        Returns:
            A dict of fx pair rates
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
        Convert 1 unit of the given currency into Mexican Pesos (MXN).
        (EUR to MXN rate) / (EUR to some other)
        
        Args:
            currency: The three-letter ISO code of the currency to convert eg "USD".

        Raises:
            KeyError: If either the requested currency or "MXN" is
                      missing from the fetched rates.

        Returns:
            The amount of MXN you get for 1 unit of 'currency'.
        """

        rates = self._rates_eur
        try:
            eur_to_mxn = rates["MXN"]
            eur_to_cur = rates[currency]
        except KeyError:
            raise KeyError(f"Currency {currency} not found in Fixr paylog")
        return eur_to_mxn / eur_to_cur