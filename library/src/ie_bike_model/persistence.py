import os

import joblib

MODEL_DIR = os.path.join(os.path.expanduser("~"), ".ie_bike_model")
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")


def persist_model(model):
    if not os.path.isdir(MODEL_DIR):
        os.mkdir(MODEL_DIR)
    joblib.dump(model, MODEL_PATH)


def load_model():
    return joblib.load(MODEL_PATH)
