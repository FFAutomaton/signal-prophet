from datetime import datetime, timedelta
import time
from config import *
from src.prophet_service import TurkishGekkoProphetService
from swing_utils import *
from swing_trend.swing_data import CandleLinkList
from utils import tahmin_getir, tahminlere_ekle, export_all_data


def propheti_calistir(_config, baslangic_gunu, bitis_gunu):
    arttir = _config.get('arttir')
    coin = _config.get('coin')
    pencere = _config.get('pencere')
    prophet_service = TurkishGekkoProphetService(_config)

    # export_all_data(prophet_service, _config, baslangic_gunu, bitis_gunu)
    while baslangic_gunu <= bitis_gunu:
        tahmin = []
        tahmin = [datetime.strftime(baslangic_gunu, '%Y-%m-%d %H:%M:%S')]
        start = time.time()
        series = dosya_yukle(coin, baslangic_gunu, bitis_gunu, pencere)
        high_tahmin, _close = tahmin_getir(_config, baslangic_gunu, 'High')
        low_tahmin, _close = tahmin_getir(_config, baslangic_gunu, 'Low')
        tahmin.extend([high_tahmin["yhat_upper"].values[0], high_tahmin["yhat_lower"].values[0],
                       low_tahmin["yhat_upper"].values[0], low_tahmin["yhat_lower"].values[0]])
        tahmin.append(_close)

        swing_data = CandleLinkList(series)
        swing_data.al_sat_mod_hesapla(tahmin)
        print(f'egitim bitti sure: {time.time() - start}')
        tahmin, _config = islem_hesapla_swing(_config, tahmin, swing_data)
        tahminlere_ekle(_config, tahmin)
        print(f'{baslangic_gunu} icin bitti!')
        baslangic_gunu = baslangic_gunu + timedelta(hours=arttir)

    return tahmin


if __name__ == '__main__':
    _config = {
        "API_KEY": API_KEY, "API_SECRET": API_SECRET, "coin": 'ETHUSDT', "pencere": "4h", "arttir": 4,
        "wallet": {"ETH": 0, "USDT": 1000}
    }
    baslangic_gunu = datetime.strptime('2021-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    bitis_gunu = datetime.strptime('2021-12-21 00:00:00', '%Y-%m-%d %H:%M:%S')

    propheti_calistir(_config, baslangic_gunu, bitis_gunu)
    # TODO:: Backtest kodunu yaz tahminlere ekle kar zarar durumunu
    # TODO:: 4h 1d karsilastir


    tahmin_schema = {
        "ds": '2021-12-16',
        "tahmin": 4678.76,
        "close": 3567,
    }