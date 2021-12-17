from prophet.diagnostics import cross_validation
from datetime import datetime, timedelta
from prophet.diagnostics import performance_metrics

from config import *
from src.prophet_service import TurkishGekkoProphetService
from utils import *

_config = {
    "API_KEY": API_KEY, "API_SECRET": API_SECRET, "coin": 'ETHUSDT', "pencere": "1d", "arttir": 24,
    "wallet": {"ETH": 0, "USDT": 1000}
}
baslangic_gunu = datetime.strptime('2021-12-16 00:00:00', '%Y-%m-%d %H:%M:%S')
train = model_verisini_getir(_config, baslangic_gunu, 'Low')


import itertools
import numpy as np
import pandas as pd

param_grid = {
    "seasonality_mode": ['additive', 'multiplicative'],
    'changepoint_prior_scale': [0.001, 0.01, 0.1, 0.5],
    'seasonality_prior_scale': [0.01, 0.1, 1.0, 10.0],
    'changepoint_range': [0.8, 0.95, 0.05],
}

# Generate all combinations of parameters
all_params = [dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())]
rmses = []  # Store the RMSEs for each params here

# Use cross validation to evaluate all parameters
for params in all_params:
    m = ProphetModel(
        train=train,
        horizon=1,
        **params
    )
    m.fit()
    df_cv = cross_validation(m.prophet, initial='60 days', horizon='1 days', period='1 days', parallel="threads")
    df_p = performance_metrics(df_cv, rolling_window=1)
    rmses.append(df_p['rmse'].values[0])

# Find the best parameters
tuning_results = pd.DataFrame(all_params)
tuning_results['rmse'] = rmses
print(tuning_results)

best_params = all_params[np.argmin(rmses)]
print(best_params)