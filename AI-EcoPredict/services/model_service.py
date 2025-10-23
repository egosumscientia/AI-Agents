import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

def train_and_predict(df: pd.DataFrame, retrain=False):
    X = df[["temperature_2m", "relative_humidity_2m", "pressure_msl", "precipitation"]]
    y = df["wind_speed_10m"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    lr = LinearRegression()
    rf = RandomForestRegressor(n_estimators=100, random_state=42)

    lr.fit(X_train, y_train)
    rf.fit(X_train, y_train)

    preds_lr = lr.predict(X_test)
    preds_rf = rf.predict(X_test)
    blended = (preds_lr + preds_rf) / 2

    mae = mean_absolute_error(y_test, blended)
    print(f"MAE: {mae:.3f}")

    return blended.tolist()
