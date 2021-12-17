from datetime import datetime, timedelta
import os
import time
from config import *
from src.prophet_service import TurkishGekkoProphetService
from utils import *


def propheti_calistir(_config, baslangic_gunu, bitis_gunu):
    arttir = _config.get('arttir')
    prophet_service = TurkishGekkoProphetService(_config)

    # export_all_data(prophet_service, _config, baslangic_gunu, bitis_gunu)
    while baslangic_gunu <= bitis_gunu:
        tahmin = []
        tahmin = [datetime.strftime(baslangic_gunu, '%Y-%m-%d %H:%M:%S')]
        start = time.time()
        open_tahmin, _close = tahmin_getir(_config, baslangic_gunu, 'Open')
        high_tahmin, _close = tahmin_getir(_config, baslangic_gunu, 'High')
        low_tahmin, _close = tahmin_getir(_config, baslangic_gunu, 'Low')
        close_tahmin, _close = tahmin_getir(_config, baslangic_gunu, 'Close')
        print(f'egitim bitti sure: {time.time() - start}')
        tahmin.extend([open_tahmin, high_tahmin,low_tahmin, close_tahmin])
        tahmin.append(_close)
        # tahmin, _config = islem_hesapla_low(_config, tahmin)
        tahmin, _config = islem_hesapla_open_close(_config, tahmin)
        tahminlere_ekle(_config, tahmin)
        print(f'{baslangic_gunu} icin bitti!')
        baslangic_gunu = baslangic_gunu + timedelta(hours=arttir)

    return tahmin


if __name__ == '__main__':
    _config = {
        "API_KEY": API_KEY, "API_SECRET": API_SECRET, "coin": 'ETHUSDT', "pencere": "1d", "arttir": 24,
        "wallet": {"ETH": 0, "USDT": 1000}
    }
    baslangic_gunu = datetime.strptime('2021-09-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    bitis_gunu = datetime.strptime('2021-12-17 00:00:00', '%Y-%m-%d %H:%M:%S')

    propheti_calistir(_config, baslangic_gunu, bitis_gunu)
    # TODO:: Backtest kodunu yaz tahminlere ekle kar zarar durumunu
    # TODO:: 4h 1d karsilastir


    tahmin_schema = {
        "ds": '2021-12-16',
        "tahmin": 4678.76,
        "close": 3567,
    }