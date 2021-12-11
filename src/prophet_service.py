from datetime import datetime, timedelta
import os
from turkish_gekko_packages.binance_service import TurkishGekkoBinanceService
from utils import *


class TurkishGekkoProphetService:
    def __init__(self, _config):
        self.coin = _config.get('coin')
        self.OPEN_TIME = 'Open Time'
        self.HIGH = 'High'
        self.TOTAL_DAY_COUNT = 14
        self.WINDOW_DAY = 1
        self.WINDOW_4H = 6 * 7
        self.WINDOW_1H = 4 * 24
        self.WINDOW_15M = 4 * 24 * 2
        self._config = _config
        self.tg_binance_service = TurkishGekkoBinanceService(self._config)

    @staticmethod
    def only_basic_pre_process(tempdata):
        Copentime = []
        Chigh = []
        Clow = []
        Copen = []
        Cclose = []
        Cvolume = []
        i = len(tempdata) - 1
        while i >= 0:
            dd = datetime.utcfromtimestamp(tempdata[i][0] / 1000)
            Copentime.append(dd)
            Copen.append(tempdata[i][1])
            Chigh.append(tempdata[i][2])
            Clow.append(tempdata[i][3])
            Cclose.append(tempdata[i][4])
            Cvolume.append(tempdata[i][5])
            i = i - 1
        data = {
            'Open Time': Copentime,
            'Open': Copen,
            'High': Chigh,
            'Low': Clow,
            'Close': Cclose,
            'Volume': Cvolume
        }
        df = pd.DataFrame(data)

        return df

    def apply_windowing(self, df, _type, _range):
        data = {}
        for i in range(0, _range):
            try:
                data[f'{_type}_{i}'] = df[self.HIGH][i]
            except:
                break
        return pd.DataFrame(data, index=[0])

    def dataframe_schemasina_cevir_ana(self, daily, fourhour, onehour, fiftmins):
        return self.dataframe_schemasina_cevir_isci(daily), self.dataframe_schemasina_cevir_isci(fourhour), \
               self.dataframe_schemasina_cevir_isci(onehour), self.dataframe_schemasina_cevir_isci(fiftmins)

    @staticmethod
    def dataframe_schemasina_cevir_isci(tempdata):
        Copentime = []
        Chigh = []
        Clow = []
        Copen = []
        Cclose = []
        Cvolume = []
        i = len(tempdata) - 1
        while i >= 0:
            dd = datetime.utcfromtimestamp(tempdata[i][0] / 1000)
            Copentime.append(dd)
            Copen.append(tempdata[i][1])
            Chigh.append(tempdata[i][2])
            Clow.append(tempdata[i][3])
            Cclose.append(tempdata[i][4])
            Cvolume.append(tempdata[i][5])
            i = i - 1
        data = {
            'Open Time': Copentime,
            'Open': Copen,
            'High': Chigh,
            'Low': Clow,
            'Close': Cclose,
            'Volume': Cvolume
        }
        df = pd.DataFrame(data)
        df[["Open Time"]].apply(pd.to_datetime)
        df = df.sort_values(by='Open Time', ascending=False, ignore_index=True)
        return df

    @staticmethod
    def gune_ait_dosya_adi_olustur(coin, bugun):
        file_name = f'./coindata/{coin}/daily/{coin}_{bugun}.csv'
        return file_name

    def belli_aralik_icin_input_verisi_olustur(self, baslangic_gunu, bitis_gunu):
        while baslangic_gunu <= bitis_gunu:
            file_name = self.gune_ait_dosya_adi_olustur(self.coin, datetime.strftime(baslangic_gunu, '%Y_%m_%d'))
            if os.path.isfile(file_name):
                return
            df = self.gunluk_satir_olustur(self.coin, baslangic_gunu)
            print(f'{baslangic_gunu} icin satir hazirlandi!!')
            baslangic_gunu = baslangic_gunu + timedelta(days=1)
            df.to_csv(file_name, index=False)

    def gunluk_satir_olustur(self, coin, today):
        daily, fourhour, onehour, fiftmins = self.tg_binance_service.zaman_serisi_fraktali_olustur(coin, today)
        daily, fourhour, onehour, fiftmins = self.dataframe_schemasina_cevir_ana(daily, fourhour, onehour, fiftmins)
        _1g = daily[[self.OPEN_TIME, self.HIGH]]
        _4s = self.apply_windowing(fourhour, '4H', self.WINDOW_4H)
        _1s = self.apply_windowing(onehour, '1H', self.WINDOW_1H)
        _15m = self.apply_windowing(fiftmins, '15M', self.WINDOW_15M)
        result = pd.concat([_1g, _4s, _1s, _15m], axis=1)  # kolon olarak ekliyor
        return result
