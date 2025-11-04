from pathlib import Path

# Project root = .../alt-alpha
ROOT = Path(__file__).resolve().parents[2]

# Standard data/plots folders
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
PLOTS = ROOT / "plots"

# Make sure the folders exist
for p in (DATA_RAW, DATA_PROCESSED, PLOTS):
    p.mkdir(parents=True, exist_ok=True)
