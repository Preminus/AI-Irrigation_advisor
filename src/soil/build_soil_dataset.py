from pathlib import Path

# Create output directory if it doesn't exist
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

import pandas as pd
from soils import SoilDownloader

points = pd.DataFrame({
    "latitude": [
        -1.215,
        -1.213,
        -1.211,
        -1.209,
        -1.207
    ],
    "longitude": [
        36.650,
        36.652,
        36.654,
        36.656,
        36.658
    ]
})

soil = SoilDownloader()

dataset = soil.build_dataset(points)

dataset.to_csv(
    "muguga_soil.csv",
    index=False
)

print(dataset)