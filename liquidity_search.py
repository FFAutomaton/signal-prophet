from datetime import datetime
import pandas as pd
from config import *


def dosya_yukle(coin, baslangic_gunu, bitis_gunu):
    tum_data_dosya_adi = f'./coindata/{coin}/{coin}_1H_all.csv'
    main_dataframe = pd.read_csv(tum_data_dosya_adi)

    main_dataframe['Open Time'] = main_dataframe[["Open Time"]].apply(pd.to_datetime)
    main_dataframe = main_dataframe[main_dataframe['Open Time'] < bitis_gunu].reset_index(drop=True)
    main_dataframe = main_dataframe[main_dataframe['Open Time'] > baslangic_gunu].reset_index(drop=True)
    print('maindataframe hazir!')
    return main_dataframe


def search_liquidity(_config, baslangic_gunu, bitis_gunu):
    coin = _config.get('coin')
    pencere = _config.get('pencere')
    df = dosya_yukle(coin, baslangic_gunu, bitis_gunu)
    df = df.sort_values(by='Open Time', ascending=True, ignore_index=True)
    liquidated = {}
    takeprofit = {}
    for index, row in df.iterrows():
        count = 0
        open = row["Open"]
        future = df.iloc[index:]
        for idx, candle in future.iterrows():
            high = candle["High"]
            low = candle["Low"]
            if high > open * 1.01:
                liquidated[str(count)] = liquidated.get(str(count)) + 1 if liquidated.get(str(count)) else 1
                break
            if low < open * 0.98:
                takeprofit[str(count)] = takeprofit.get(str(count)) + 1 if takeprofit.get(str(count)) else 1
                break
            count += 1
    import json

    liquidated = json.dumps(liquidated)
    takeprofit = json.dumps(takeprofit)
    print(liquidated)
    print(takeprofit)

    print(df.head())


if __name__ == '__main__':
    _config = {
        "API_KEY": API_KEY, "API_SECRET": API_SECRET, "coin": 'ETHUSDT', "pencere": "1d", "arttir": 24,
        "wallet": {"ETH": 0, "USDT": 1000}
    }
    baslangic_gunu = datetime.strptime('2021-09-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    bitis_gunu = datetime.strptime('2021-12-20 00:00:00', '%Y-%m-%d %H:%M:%S')

    search_liquidity(_config, baslangic_gunu, bitis_gunu)
    # TODO:: Backtest kodunu yaz tahminlere ekle kar zarar durumunu
    # TODO:: 4h 1d karsilastir

