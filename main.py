from datetime import datetime, timedelta
import os
import time
from config import *
from src.prophet_service import TurkishGekkoProphetService
from utils import *


if __name__ == '__main__':
    _config = {'API_KEY': API_KEY, 'API_SECRET': API_SECRET, "coin": 'ETHUSDT'}

    prophet_service = TurkishGekkoProphetService(_config)
    basl_str = '2021-02-13'
    bit_str = '2021-03-01'
    baslangic_gunu = datetime.strptime(basl_str, '%Y-%m-%d')
    bitis_gunu = datetime.strptime(bit_str, '%Y-%m-%d')

    while baslangic_gunu <= bitis_gunu:
        tahminler = []

        tahminler = [datetime.strftime(baslangic_gunu, '%Y-%m-%d')]
        for cesit in ['Low']:
        # for cesit in ['High', 'Low']:
            file_name = prophet_service.dosya_adi_olustur(datetime.strftime(baslangic_gunu, '%Y_%m_%d'), cesit)
            if not os.path.isfile(file_name):
                prophet_service.belli_aralik_icin_input_verisi_olustur(file_name, baslangic_gunu, cesit)
            train, additional_feature_data = model_verisini_getir(
                _config.get('coin'), datetime.strftime(baslangic_gunu - timedelta(days=1), '%Y-%m-%d'), cesit
            )
            start = time.time()
            print('egitim baslasin...')
            forecast = model_egit_tahmin_et(train, additional_feature_data)
            print(f'egitim bitti sure: {time.time() - start}')
            tahminler.append(forecast.get('yhat').values[0])

        tahminlere_ekle(_config, tahminler)

        print(f'{baslangic_gunu} icin bitti!')
        baslangic_gunu = baslangic_gunu + timedelta(days=1)
