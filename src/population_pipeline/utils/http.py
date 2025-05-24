"""
Small wrapper around httpx to handle common tasks like retries and timeouts.
"""

from __future__ import annotations

import time
from typing import Any, Dict

import httpx

def get_json(url: str, params: Dict[str, Any] | None = None) -> list[Any]:
    """
    Get 'url' and return the parsed JSON.
    
    Also includes the back-off on HTTP 5xx or 429 errors.
    """
    backoff_seconds = 1
    max_attempts = 5
    
    for attempt in range(1, max_attempts + 1):
        try:
            response = httpx.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code in {429, 500, 502, 503, 504} and attempt < max_attempts:
                time.sleep(backoff_seconds)
                backoff_seconds *= 2
                continue
            raise


    