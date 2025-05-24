"""
Enabler of CLI to test

Run 'pop-pipeline pop --top 10'

"""

from __future__ import annotations

import typer
from rich import print

from population_pipeline.pipeline.module_a import build_population_df

app = typer.Typer()

@app.command("population")
def population(top: int = typer.Option(None, "--top", "-t", help="Limit to top N countries by population")):
    """
    Fetch and display the latest population data.
    """
    df = build_population_df(top_n=top)
    print(df.to_string(index=False))

if __name__ == "__main__":
    app()