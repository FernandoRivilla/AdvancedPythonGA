import os

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import (
    ColumnTransformer,
    make_column_selector,
    make_column_transformer,
)
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.pipeline import FeatureUnion, Pipeline, make_pipeline, make_union
from sklearn.preprocessing import FunctionTransformer, OrdinalEncoder

from ie_bike_model.data import load_train_data
from ie_bike_model.persistence import load_model, persist_model


def ffill_missing(ser):
    return ser.fillna(method="ffill")


def is_weekend(df):
    return df["dteday"].dt.day_name().isin(["Saturday", "Sunday"]).to_frame()


def train_and_persist():
    df = load_train_data()
    df_train = df.loc[df["dteday"] < "2012-10"]

    ffiller = FunctionTransformer(ffill_missing)
    weather_enc = make_pipeline(ffiller, OrdinalEncoder())
    ct = make_column_transformer(
        (ffiller, make_column_selector(dtype_include=np.number)),
        (weather_enc, ["weathersit"]),
    )
    preprocessing = FeatureUnion(
        [("is_weekend", FunctionTransformer(is_weekend)), ("column_transform", ct)]
    )

    reg = Pipeline(
        [("preprocessing", preprocessing), ("model", RandomForestRegressor())]
    )

    X_train = df_train.drop(columns=["instant", "cnt", "casual", "registered"])
    y_train = df_train["cnt"]

    reg.fit(X_train, y_train)

    persist_model(reg)


def predict(dteday, hr, weathersit, temp, atemp, hum, windspeed):
    reg = load_model()

    X_input = pd.DataFrame(
        [
            {
                "dteday": pd.to_datetime(dteday),
                "hr": hr,
                "weathersit": weathersit,
                "temp": temp,
                "atemp": atemp,
                "hum": hum,
                "windspeed": windspeed,
            }
        ]
    )

    y_pred = reg.predict(X_input)
    assert len(y_pred) == 1

    return round(y_pred[0])


if __name__ == "__main__":
    print(
        predict(
            dteday="2012-11-10",
            hr=10,
            weathersit="Clear, Few clouds, Partly cloudy, Partly cloudy",
            temp=0.3,
            atemp=0.31,
            hum=0.8,
            windspeed=0.0,
        )
    )
