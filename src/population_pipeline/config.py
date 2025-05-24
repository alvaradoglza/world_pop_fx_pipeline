""""
Settings for the pipeline.

"""

from pathlib import Path

WORLD_BANK_BASE = "https://api.worldbank.org/v2"
POPULATION_INDICATOR = "SP.POP.TOTL"

# Small exageration to avoid issues
PER_PAGE = 20000

# Cache folder for streamlit possibly neededd
DATA_DIR = Path(__file__).parent.parents[2] / "data"
DATA_DIR.mkdir(exist_ok=True)