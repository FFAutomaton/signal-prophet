from datetime import date, timedelta, datetime
import pandas as pd
from config import *
from main import TurkishGekkoProphetService
from utils import *


if __name__ == '__main__':
    coin = 'ETHUSDT'
    config = {'API_KEY': API_KEY, 'API_SECRET': API_SECRET}

    prophet_service = TurkishGekkoProphetService(config)
    today = date.today()
    file_name = gune_ait_dosya_adi_olustur(coin, datetime.strftime('%Y_%m_%d'))
    i = 0
    df_list = []
    while i < 14:
        df_list.append(prophet_service.get_prophet_row(coin, today))
        print(f'{today} icin satir hazirlandi!!')
        today = today - timedelta(days=1)
        i = i + 1
    df = pd.concat(df_list)
    # tempnameB = './coindata/example.csv'
    df.to_csv(file_name, index=False)
    print(df)