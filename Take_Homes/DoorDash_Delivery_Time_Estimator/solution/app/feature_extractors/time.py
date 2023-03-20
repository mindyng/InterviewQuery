import pandas as pd

from app.features_extractors.numerical import make_harmonic_features


def extract_time_features(data: pd.DataFrame) -> pd.DataFrame:
    minute_of_day_cos, minute_of_day_sin = make_harmonic_features(
        data.created_at.dt.hour * 60 + data.created_at.dt.minute,
        24 * 60)

    return pd.DataFrame({
        'minute_of_day_cos': minute_of_day_cos,
        'minute_of_day_sin': minute_of_day_sin,
    }, index=data.index)
