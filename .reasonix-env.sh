#!/bin/bash
# Reasonix Python Toolkit — source this before running Python scripts that
# need workspace-installed packages (folium, statsmodels, streamlit, etc.)
export PYTHONPATH="/Users/hunterhughes/.reasonix/global-workspace/.python-packages:$PYTHONPATH"
echo "[reasonix] PYTHONPATH set: $PYTHONPATH"
