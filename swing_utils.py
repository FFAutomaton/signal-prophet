import pandas as pd


def swing_verisini_getir(_config, suan, cesit):
    coin = _config.get('coin')
    pencere = _config.get('pencere')
    df = dosya_yukle(coin, suan, pencere)
    return df


def islem_hesapla_swing(_config, tahmin, swing_data):
    wallet = _config.get("wallet")
    suanki_fiyat = tahmin[5]

    if wallet["USDT"] != 0:
        if swing_data.karar == 'al':
            wallet["ETH"] = wallet["USDT"] / suanki_fiyat
            wallet["USDT"] = 0
    elif wallet["ETH"] != 0:
        if swing_data.karar == 'sat':
            wallet["USDT"] = wallet["ETH"] * suanki_fiyat
            wallet["ETH"] = 0

    _config["wallet"] = wallet
    tahmin.append(wallet["ETH"])
    tahmin.append(wallet["USDT"])
    return tahmin, _config


def dosya_yukle(coin, baslangic, bitis, pencere):
    tum_data_dosya_adi = f'./coindata/{coin}/{coin}_{pencere}_all.csv'
    main_dataframe = pd.read_csv(tum_data_dosya_adi)

    main_dataframe['Open Time'] = main_dataframe[["Open Time"]].apply(pd.to_datetime)
    main_dataframe = main_dataframe.sort_values(by='Open Time', ascending=False, ignore_index=True)
    main_dataframe = main_dataframe[main_dataframe['Open Time'] < baslangic].reset_index(drop=True)
    main_dataframe = main_dataframe.iloc[0:400]
    print('maindataframe hazir!')
    return main_dataframe