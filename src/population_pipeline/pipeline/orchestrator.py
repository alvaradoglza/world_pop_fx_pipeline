"""
Run Module A then Module B

"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd

from population_pipeline.pipeline.module_a import build_population_df
from population_pipeline.pipeline.module_b import cent_mxn
from population_pipeline.utils.logger import init_logging

init_logging()
log = logging.getLogger(__name__)


def run_pipeline(top_n: int | None = None, out_dir: Path | None = None) -> Path:
    """
    Execute the full pipeline.

    Returns the folder where artefacts were written.
    """
    ts = datetime.now().isoformat(timespec="seconds").replace(":", "-")    
    target_dir = out_dir or (Path("data") / ts)
    target_dir.mkdir(parents=True, exist_ok=True)          

    log.info("Stage 1 - fetching population")
    pop_df = build_population_df(top_n)

    log.info("Stage 2 - adding FX & MXN math")
    final_df, grand_total = cent_mxn(pop_df)

    csv_path = target_dir / "population_fx.csv"
    json_path = target_dir / "population_fx.json"

    final_df.to_csv(csv_path, index=False)                 
    final_df.to_json(json_path, orient="records", indent=2) 

    meta = {"generated_at": ts, "grand_total_mxn": grand_total}
    (target_dir / "run_meta.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8"        
    ) 

    log.info("Artefacts written to %s", target_dir)
    return target_dir

    