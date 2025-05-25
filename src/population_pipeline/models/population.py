"""

Pydantic model for a single population record (one countr1y, one year).

"""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field

class CountryInfo(BaseModel):
    """
    Information about a country.

    Attributes:
        id: ISO-3 code of the country eg "USA".
        value: Full country name eg "United States of America".
    """

    id: str 
    value: str 

class PopulationRecord(BaseModel):
    """
    A single population record for a country in a specific year.

    Attributes:
        country: Metadata of previous class, iso and name.
        date: Year of the population record.
        value: Population count; None if data is missing.

    """

    country: CountryInfo
    date: int = Field(..., description="Year of the population record")
    value: Optional[int]

    @property
    def iso3(self) -> str:
        """
        Get the ISO-3 code of the country.

        Returns:
            str: The three-letter ISO-3 code.
        """

        return self.country.id
    
    @property
    def name(self) -> str:
        """
        Get the full name of the country.

        Returns:
            str: Countrys full name
        """

        return self.country.value