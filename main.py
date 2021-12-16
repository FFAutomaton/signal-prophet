from datetime import datetime, timedelta
import os
import time
from config import *
from src.prophet_service import TurkishGekkoProphetService
from utils import *


def propheti_calistir(_config, baslangic_gunu, bitis_gunu):
    prophet_service = TurkishGekkoProphetService(_config)

    # export_all_data(prophet_service, _config, baslangic_gunu, bitis_gunu, '1d')
    # export_all_data(prophet_service, _config, baslangic_gunu, bitis_gunu, '4h')
    # export_all_data(prophet_service, _config, baslangic_gunu, bitis_gunu, '1h')
    while baslangic_gunu <= bitis_gunu + timedelta(seconds=1):
        tahmin = []
        tahmin = [datetime.strftime(baslangic_gunu, '%Y-%m-%d')]
        for cesit in ['Low']:
            train = model_verisini_getir(
                _config , baslangic_gunu, cesit
            )
            start = time.time()
            print('egitim baslasin...')
            forecast = model_egit_tahmin_et(train)
            print(f'egitim bitti sure: {time.time() - start}')
            tahmin.append(forecast.get('yhat').values[0])
            tahminlere_ekle(_config, tahmin)
        print(f'{baslangic_gunu} icin bitti!')
        baslangic_gunu = baslangic_gunu + timedelta(days=1)

    return tahmin


if __name__ == '__main__':
    _config = {'API_KEY': API_KEY, 'API_SECRET': API_SECRET, "coin": 'ETHUSDT', "pencere": "1d"}
    baslangic_gunu = datetime.strptime('2021-12-16', '%Y-%m-%d')
    bitis_gunu = datetime.strptime('2021-12-16', '%Y-%m-%d')
    bitis_gunu = bitis_gunu - timedelta(seconds=1)

    propheti_calistir(_config, baslangic_gunu, bitis_gunu)
    # TODO:: Fix file append issue, prepare finish ts for historical klines
    # TODO:: Daily sinyal
    # TODO:: 4H sinyal
    # TODO:: 1H sinyal
    # TODO:: Sadece fiyat kullan regressorlari kaldir


    tahmin_schema = {
        "ds": '2021-12-16',
        "tahmin": 4678.76,
        "close": 3567,
    }