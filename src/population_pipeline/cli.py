"""
Enabler of CLI to test

"""

from __future__ import annotations

import typer
from rich import print

from population_pipeline.pipeline.module_a import build_population_df
from population_pipeline.pipeline.module_b import cent_mxn

import pandas as pd
pd.set_option("display.float_format", "{:,.4f}".format)

app = typer.Typer()

@app.command("population")
def population(top: int = typer.Option(None, "--top", "-t", help="Limit to top N countries by population")):
    """
    Fetch and display the latest population data.
    """
    df = build_population_df(top_n=top)
    print(df.to_string(index=False))


@app.command("mxn")
def mxn_total(top: int = typer.Option(None, "--top", "-t", help="Top-N countries to include")):
    """
    Run the full pipeline and show the MXN totals.
    """
    pop_df = build_population_df(top_n=top)
    df = cent_mxn(pop_df)

    fmt = {
        "population":          "{:,.0f}".format,  
        "fx_to_mxn":           "{:,.4f}".format,  
        "mxn_from_one_cent":   "{:,.0f}".format,  
    }

    print(
        df[["country", "population", "currency", "fx_to_mxn", "mxn_from_one_cent"]]
          .to_string(index=False, formatters=fmt)
    )


if __name__ == "__main__":
    app()