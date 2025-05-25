"""
Enabler of CLI to test

"""

from __future__ import annotations

import typer
import json
from rich import print
from rich.table import Table
from rich.console import Console

from population_pipeline.pipeline.module_a import build_population_df
from population_pipeline.pipeline.module_b import cent_mxn
from population_pipeline.pipeline.orchestrator import run_pipeline
from population_pipeline.utils.logger import init_logging



import pandas as pd
pd.set_option("display.float_format", "{:,.4f}".format)

app = typer.Typer()



@app.command("run")
def run(
    top: int = typer.Option(None, "--top", "-t", help="Limit to N most-populous countries"),
    ):
    """
    Run of the pipeline
    """

    init_logging("INFO")
    artefact_dir = run_pipeline(top_n=top)

    df = pd.read_csv(artefact_dir / "population_fx.csv")    
    tbl = Table(show_header=True, header_style="bold magenta")
    for col in ["country_code", "country_name", "year", "population", "currency", "fx_to_mxn", "mxn_from_one_cent"]:
        tbl.add_column(col)
    for _, row in df.head(10).iterrows():
        tbl.add_row(*map(str, row))
    Console().print(tbl)

    with open(artefact_dir / "run_meta.json", encoding="utf-8") as fh:
        meta = json.load(fh)
    Console().print(f"[bold yellow]\nGrand total:[/] {meta['grand_total_mxn']:,.0f} MXN")


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
    df, grand_total = cent_mxn(pop_df)

    print(df[["country", "population", "currency", "fx_to_mxn", "mxn_from_one_cent"]])
    print(f"\n[grand total] {grand_total:,.0f} MXN")



if __name__ == "__main__":
    app()