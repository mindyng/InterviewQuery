from datetime import date

import numpy as np
import pandas as pd

from app.features_extractors.calendar import number_of_days_after_true


def test_empty():
    days_after_true = number_of_days_after_true(pd.Series([], dtype=bool), date(year=2020, month=1, day=1))
    assert np.isnan(days_after_true)


def test_day_before():
    start_date = date(year=2019, month=12, day=31)
    end_date = date(year=2020, month=1, day=2)
    data = pd.Series([False, False, True], index=pd.date_range(start_date, end_date))
    days_after_true = number_of_days_after_true(data, pd.to_datetime('2020-01-01'))
    assert days_after_true == 0


def test_day_after():
    start_date = date(year=2019, month=12, day=31)
    end_date = date(year=2020, month=1, day=2)
    data = pd.Series([True, False, False], index=pd.date_range(start_date, end_date))
    days_after_true = number_of_days_after_true(data, pd.to_datetime('2020-01-01'))
    assert days_after_true == 1
