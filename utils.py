import pandas as pd
from csv import writer
from ml.model_classes.prophet_model import ProphetModel


def model_egit_tahmin_et(train):
    m_params = {
        "changepoint_prior_scale": 0.1,
        "seasonality_prior_scale": 1,
        "holidays_prior_scale": 1,
        "outlier_remove_window": 0,
    }
    model = ProphetModel(
        train=train,
        changepoint_prior_scale=m_params.get("changepoint_prior_scale"),
        seasonality_prior_scale=m_params.get("seasonality_prior_scale"),
        holidays_prior_scale=m_params.get("holidays_prior_scale"),
        changepoint_range=m_params.get("changepoint_range"),
        outlier_remove_window=m_params.get("outlier_remove_window"),
        horizon=1,
    )
    model.fit()
    return model.predict()


def tahminlere_ekle(_config, tahminler):
    with open(f'./coindata/{_config.get("coin")}/tahminler.csv', 'a', newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(tahminler)
        f_object.close()


def boslari_doldur(main_dataframe):
    if main_dataframe.isnull().any().any():
        for index, row in main_dataframe.isnull().iterrows():
            for i, v in enumerate(row.values):
                if v:
                    main_dataframe.at[index, row.index[i]] = main_dataframe.mean(axis=1)[index]
    return main_dataframe


def dosya_yukle(coin, bugun, cesit, pencere):
    tum_data_dosya_adi = f'./coindata/{coin}/{coin}_{pencere}_all.csv'
    main_dataframe = pd.read_csv(tum_data_dosya_adi)

    main_dataframe['Open Time'] = main_dataframe[["Open Time"]].apply(pd.to_datetime)
    main_dataframe = main_dataframe.sort_values(by='Open Time', ascending=False, ignore_index=True)
    main_dataframe = main_dataframe[main_dataframe['Open Time'] < bugun].reset_index(drop=True)
    main_dataframe = boslari_doldur(main_dataframe)
    print('maindataframe hazir!')
    return main_dataframe


def train_kirp_yeniden_adlandir(df, cesit):
    # df = df.iloc[:, :2]
    train = df.rename(columns={"Open Time": "ds"})
    train = train.rename(columns={cesit: "y"})
    return train


def kaydir_birlestir(train, additional_data):
    train = train.iloc[:-1, :]
    future_add_data = additional_data.iloc[:1, :]
    train = pd.concat([train, additional_data], axis=1)
    return train, future_add_data


def model_verisini_getir(_config, bugun, cesit):
    coin = _config.get('coin')
    pencere = _config.get('pencere')
    df = dosya_yukle(coin, bugun, cesit, pencere)
    train = train_kirp_yeniden_adlandir(df, cesit)
    return train


def export_all_data(prophet_service, _config, baslangic_gunu, bitis_gunu, tip):
    coin = _config.get('coin')

    data = prophet_service.tg_binance_service.get_client().get_historical_klines(
        symbol=coin, interval=tip,
        start_str=str(baslangic_gunu), end_str=str(bitis_gunu), limit=500
    )
    df = prophet_service.dataframe_schemasina_cevir_isci(data)
    df.to_csv(f'./coindata/{coin}/{coin}_{tip}_all.csv', mode='a', index=False, header=False)
    print(f'export tamamlandi {tip}')


if __name__ == '__main__':
    bugun = '2021-12-06'
    model_verisini_getir('ETHUSDT', bugun)