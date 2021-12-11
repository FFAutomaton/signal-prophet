from datetime import timedelta, datetime
from config import *
from src.prophet_service import TurkishGekkoProphetService
from utils import *



if __name__ == '__main__':
    coin = 'ETHUSDT'
    config = {'API_KEY': API_KEY, 'API_SECRET': API_SECRET}
    prophet_service = TurkishGekkoProphetService(config)
    baslangic_gunu = datetime.strptime('2021-01-06', '%Y-%m-%d')
    bitis_gunu = datetime.strptime('2021-12-07', '%Y-%m-%d')
    belli_aralik_icin_input_verisi_olustur(baslangic_gunu, bitis_gunu)
