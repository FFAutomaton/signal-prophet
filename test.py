from datetime import date, timedelta, datetime
import pandas as pd
from config import *
from main import TurkishGekkoProphetService
from utils import *


def belli_aralik_icin_input_verisi_olustur(baslangic_gunu, bitis_gunu):
    while baslangic_gunu <= bitis_gunu:
        file_name = gune_ait_dosya_adi_olustur(coin, datetime.strftime(baslangic_gunu, '%Y_%m_%d'))
        df = gunluk_satir_olustur(coin, baslangic_gunu)

        print(f'{baslangic_gunu} icin satir hazirlandi!!')
        baslangic_gunu = baslangic_gunu + timedelta(days=1)
        df.to_csv(file_name, index=False)


def gunluk_satir_olustur(coin, today):
    return prophet_service.get_prophet_row(coin, today)


if __name__ == '__main__':
    coin = 'ETHUSDT'
    config = {'API_KEY': API_KEY, 'API_SECRET': API_SECRET}
    prophet_service = TurkishGekkoProphetService(config)
    baslangic_gunu = datetime.strptime('2021-01-06', '%Y-%m-%d')
    bitis_gunu = datetime.strptime('2021-12-07', '%Y-%m-%d')
    belli_aralik_icin_input_verisi_olustur(baslangic_gunu, bitis_gunu)
