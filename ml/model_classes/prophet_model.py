from prophet import Prophet
import numpy as np
import pandas as pd
from ml.model_utils.supressor import suppress_stdout_stderr


class ProphetModel:
    def __init__(self, train, horizon, additional_features=None, growth="linear",
                 seasonality_mode="multiplicative", changepoint_range=0.9, changepoint_prior_scale=0.01,
                 seasonality_prior_scale=10, holidays_prior_scale=10, outlier_remove_window=0
                 ):
        self.train = train
        self.additional_features = additional_features

        # Get 99th and 20th percentile of historical data to determine cap and floor.
        self.max_y = self.train["y"].quantile(0.99)
        self.min_y = self.train["y"].quantile(0.3)

        self.growth = growth

        # If we have more than 1 year data, use yearly seasonality.
        if self.train.shape[0] < 730:
            ys = False
        else:
            ys = True

        # Create model prophet model object.
        self.prophet = Prophet(
            growth=growth,
            # seasonality_mode=seasonality_mode,
            # seasonality_prior_scale=seasonality_prior_scale,
            # changepoint_range=changepoint_range,
            # changepoint_prior_scale=changepoint_prior_scale,
            yearly_seasonality=ys,
            weekly_seasonality=False,
            daily_seasonality=False,
            # holidays_prior_scale=holidays_prior_scale,
        )

        # self.prophet.add_seasonality(period=24, fourier_order=10, name="daily")
        # self.prophet.add_seasonality(period=24*7, fourier_order=6, name="weekly")
        # self.prophet.add_seasonality(period=24*30, fourier_order=3, name="monthly")

        # Add country specific holidays.
        # self.prophet.add_country_holidays(country_name="US")
        self.horizon = horizon
        self.outlier_remove_window = outlier_remove_window

        if self.additional_features is not None:
            for col in self.additional_features:
                self.prophet.add_regressor(col, prior_scale=10, standardize=False, mode="additive")

    def fit(self):
        """Fit prophet model."""
        if self.outlier_remove_window != 0:
            self.train = self.median_filter(df=self.train, window=self.outlier_remove_window, col_name="y").copy()

        if self.growth == "logistic":
            self.train["cap"] = self.max_y * 2
            self.train["floor"] = self.min_y

        with suppress_stdout_stderr():  # To eliminate write outputs to terminal.
            self.prophet.fit(self.train)

    def predict(self):
        """Do prediction with trained model.

        :return: Forecasted data.
        :rtype: Pandas.DataFrame
        """
        # Create future data to do prediction for these dates.
        future = self.prophet.make_future_dataframe(periods=self.horizon, include_history=False)

        # If logistic model is used with cap and floor, it also needs to be added to the future data.
        if self.growth == "logistic":
            future["cap"] = self.max_y * 1.2
            future["floor"] = self.max_y * 0.8
        if self.additional_features is not None:
            future = pd.concat([future, self.additional_features], axis=1)
        forecast = self.prophet.predict(future)
        return forecast

    @staticmethod
    def median_filter(df, window=7, col_name=None):
        # TODO: Create a better outlier filter. Right now, we are not using any outlier removal technique.
        """
        A simple median filter, removes (i.e. replace by np.nan) observations that exceed N (default = 3)
        standard deviation from the median over window of length P (default = 24) centered around
        each observation.
        Parameters
        ----------
        df : pandas.DataFrame
            The pandas.DataFrame containing the column to filter.
        col_name : string
            Column to filter in the pandas.DataFrame. No default.
        window : integer
            Size of the window around each observation for the calculation
            of the median and std. Default is 7 (time-steps).
        Returns
        -------
        dfc : pandas.Dataframe
            A copy of the pandas.DataFrame `df` with filtered column.
        """

        dfc = df.loc[:, [col_name]].copy()
        dfc["median"] = dfc[col_name].rolling(window, center=True).median()
        dfc["std"] = dfc[col_name].rolling(window, center=True).std()
        median_std = dfc["std"].median()
        dfc.loc[dfc.loc[:, col_name] >= dfc["median"] + median_std, col_name] = np.nan
        dfc.loc[dfc.loc[:, col_name] <= dfc["median"] - median_std, col_name] = np.nan
        df_n = df.copy()
        df_n[col_name] = dfc.loc[:, col_name]
        return df_n
