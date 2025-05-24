"""

Pydantic model for a single population record (one countr1y, one year).

"""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field

class CountryInfo(BaseModel):
    """
    Information about a country.
    """
    id: str # 'USA"
    value: str # 'United States of America'

class PopulationRecord(BaseModel):
    """
    A single population record for a country in a specific year.
    """
    country: CountryInfo
    date: int = Field(..., description="Year of the population record")
    value: Optional[int]

    @property
    def iso3(self) -> str:
        """
        Return the ISO3 code of the country.
        """
        return self.country.id
    
    @property
    def name(self) -> str:
        """
        Return the name of the country.
        """
        return self.country.value