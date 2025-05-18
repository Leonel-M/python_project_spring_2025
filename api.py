"""
https://github.com/Kaggle/kaggle-api
"""

import os
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd

dataset = 'bhanupratapbiswas/superstore-sales'
data_dir = 'data'

api = KaggleApi()
api.authenticate()

print(f'Downloading {dataset}... ')
api.dataset_download_files(dataset, path=data_dir,unzip=True)
print(f'Files saved in {data_dir}')