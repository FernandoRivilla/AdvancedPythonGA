import os

import pandas as pd

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(DATA_DIR, "hour.csv")


def load_train_data():
    return pd.read_csv(DATA_PATH, parse_dates=["dteday"])
