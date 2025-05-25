"""
GUI for final join of the pipeline
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from population_pipeline.pipeline.orchestrator import run_pipeline

st.set_page_config(
    page_title="El Centavo - Large Coding Test",
    layout="wide",
)



st.title("El Centavo - Large Coding Test")
st.markdown("Use the controls below to run the pipeline and explore the results.")

# A three‑column trick to centre widgets: empty › controls › empty
left_pad, centre_col, right_pad = st.columns([1, 2, 1])

with centre_col:
    top_n = st.number_input(
        "Top-N countries by population",
        min_value=1,
        max_value=250,
        value=10,
        step=1,
        key="top_n_input",
    )

    run_btn = st.button("Run pipeline", use_container_width=True, key="run_btn")

if run_btn:
    artefact_dir: Path = run_pipeline(top_n=int(top_n))
    st.success(f"Artefacts written to **{artefact_dir}**", icon="✅")

    df = pd.read_csv(artefact_dir / "population_fx.csv")
    meta = json.loads((artefact_dir / "run_meta.json").read_text())

    st.metric(
        label="Grand total (MXN if every resident gives 1 cent)",
        value=f"{meta['grand_total_mxn']:,.0f} MXN",
    )

    st.dataframe(
        df[
            [
                "country",
                "population",
                "currency",
                "fx_to_mxn",
                "mxn_from_one_cent",
            ]
        ],
        use_container_width=True,
    )

    csv_bytes = (artefact_dir / "population_fx.csv").read_bytes()
    json_bytes = (artefact_dir / "population_fx.json").read_bytes()

    dcol1, dcol2, _ = st.columns([1, 1, 3])
    with dcol1:
        st.download_button(
            "Download CSV",
            data=csv_bytes,
            file_name="population_fx.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with dcol2:
        st.download_button(
            "Download JSON",
            data=json_bytes,
            file_name="population_fx.json",
            mime="application/json",
            use_container_width=True,
        )
else:
    st.info("Select a *Top‑N* value and press **Run pipeline** to start.")
