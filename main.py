from datetime import datetime, timedelta
from config import *
from src.prophet_service import TurkishGekkoProphetService
from utils import *
from ml.model_classes.prophet_model import ProphetModel


if __name__ == '__main__':
    _config = {'API_KEY': API_KEY, 'API_SECRET': API_SECRET, "coin": 'ETHUSDT'}

    # TODO:: 2021-12-11 gunu bitince yani 2021-12-12 saat 00:00:01'de
    # TODO:: 2021-12-11 input satiri hazirla
    prophet_service = TurkishGekkoProphetService(_config)
    baslangic_gunu = datetime.strptime('2021-12-09', '%Y-%m-%d')
    bitis_gunu = datetime.strptime('2021-12-10', '%Y-%m-%d')
    prophet_service.belli_aralik_icin_input_verisi_olustur(baslangic_gunu, bitis_gunu)


    # TODO:: modeli egit
    m_params = {
            "changepoint_prior_scale": 0.01,
            "seasonality_prior_scale": 5,
            "holidays_prior_scale": 5,
            "changepoint_range": 0.9,
            "outlier_remove_window": 0,
    }
    train, additional_future_data = model_verisini_getir(
        _config.get('coin'), datetime.strftime(baslangic_gunu - timedelta(days=1), '%Y-%m-%d')
    )
    model = ProphetModel(
        train=train,
        additional_features=additional_future_data,
        changepoint_prior_scale=m_params.get("changepoint_prior_scale"),
        seasonality_prior_scale=m_params.get("seasonality_prior_scale"),
        holidays_prior_scale=m_params.get("holidays_prior_scale"),
        changepoint_range=m_params.get("changepoint_range"),
        outlier_remove_window=m_params.get("outlier_remove_window"),
        horizon=1,
    )
    model.fit()
    # trained_model = model.prophet
    forecast = model.predict()
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())
    model.plot(forecast)
    # TODO:: tahminde bulun

