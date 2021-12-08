from datetime import date, datetime, timedelta
import pandas as pd
from turkish_gekko_packages.binance_service import TurkishGekkoBinanceService


class TurkishGekkoProphetService:
    def __init__(self, _config):
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

    def write_prophet_data(self, coin):
        day = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year
        filename = 'coindata/preprocessed/prophetdata/' + str(coin) + ' ' + str(month) + '-' + str(day) + '-' + str(
            year) + '.csv'
        # result.to_csv(filename)

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

        return df

    def get_prophet_row(self, coin, today):
        # TODO:: write every row into a file
        daily, fourhour, onehour, fiftmins = self.tg_binance_service.zaman_serisi_fraktali_olustur(coin, today)
        daily, fourhour, onehour, fiftmins = self.dataframe_schemasina_cevir_ana(daily, fourhour, onehour, fiftmins)
        _1g = daily[[self.OPEN_TIME, self.HIGH]]
        _4s = self.apply_windowing(fourhour, '4H', self.WINDOW_4H)
        _1s = self.apply_windowing(onehour, '1H', self.WINDOW_1H)
        _15m = self.apply_windowing(fiftmins, '15M', self.WINDOW_15M)
        result = pd.concat([_1g, _4s, _1s, _15m], axis=1)  # kolon olarak ekliyor
        return result
