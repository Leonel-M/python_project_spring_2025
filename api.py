"""
Script to automatically download and extract the Superstore Sales dataset
from Kaggle using the Kaggle API.

Dataset source:
https://www.kaggle.com/datasets/bhanupratapbiswas/superstore-sales

Requirements:
- kaggle API credentials configured (~/.kaggle/kaggle.json)
- kaggle package installed (`pip install kaggle`)

This script:
- Authenticates with the Kaggle API
- Downloads the dataset as a zip file
- Extracts it into the specified local folder
"""

import os
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd

dataset = "bhanupratapbiswas/superstore-sales"
data_dir = "data"

api = KaggleApi()

try:
    api.authenticate()
    print(f"Success authenticate")
except Exception as e:
    print(f"Error with authenticate Kaggle API: {e}")

try:
    print(f"Downloading {dataset}... ")
    api.dataset_download_files(dataset, path=data_dir, unzip=True)
    print(f"Files saved in {data_dir}")
except Exception as e:
    print(f"Error downloading {dataset}: {e}")
