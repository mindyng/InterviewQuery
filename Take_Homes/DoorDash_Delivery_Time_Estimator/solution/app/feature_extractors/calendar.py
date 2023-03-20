from datetime import date

import numpy as np
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from app.features_extractors.numerical import make_harmonic_features


def number_of_days_until_true(boolean_values: pd.Series, today: date) -> pd.Series:
    return (boolean_values[today:].idxmax() - today).days if not boolean_values.empty else np.NaN


def number_of_days_after_true(boolean_values: pd.Series, today: date):
    return (today - boolean_values[:today].iloc[::-1].idxmax()).days if not boolean_values.empty else np.NaN


def extract_calendar_features(data: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame(index=data.created_at.dt.normalize().unique())

    df['day_cos'], df['day_sin'] = make_harmonic_features(df.index.day, df.index.days_in_month)
    df['month_cos'], df['month_sin'] = make_harmonic_features(df.index.month, 12)
    df['quarter_cos'], df['quarter_sin'] = make_harmonic_features(df.index.quarter, 4)
    seasons = (df.index.month % 12 + 3) // 3 - 1
    df['season_cos'], df['season_sin'] = make_harmonic_features(seasons, 4)
    df['year'] = df.index.year
    df['dayofyear_cos'], df['dayofyear_sin'] = make_harmonic_features(df.index.year, 365)
    df['dayofweek_cos'], df['dayofweek_sin'] = make_harmonic_features(df.index.dayofweek, 7)
    df['is_weekend'] = df.index.dayofweek >= 5

    dates_with_margin = pd.date_range(
        pd.to_datetime(df.index.min()) - pd.DateOffset(months=4),
        pd.to_datetime(df.index.max()) + pd.DateOffset(months=4))
    holidays = calendar().holidays(
        start=dates_with_margin.min(),
        end=dates_with_margin.max())
    is_holiday = pd.Series(pd.Series(dates_with_margin).isin(holidays).values, index=dates_with_margin)
    df['days_until_holidays'] = pd.Series(df.index)\
        .apply(lambda today: number_of_days_until_true(is_holiday, today)).values
    df['days_after_holidays'] = pd.Series(df.index)\
        .apply(lambda today: number_of_days_after_true(is_holiday, today)).values
    df['is_holiday'] = df.index.isin(holidays)

    return pd.DataFrame({'normalized_date': data.created_at.dt.normalize()}, index=data.index)\
        .merge(df.fillna(0), left_on='normalized_date', right_index=True)\
        .drop(columns=['normalized_date'])
