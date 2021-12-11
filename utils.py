import pandas as pd
import glob


def butun_dosyalari_yukle(coin, bugun):
    folder_path = f'./coindata/{coin}/daily/'
    tum_data_dosya_adi = f'./coindata/{coin}/all.csv'
    main_dataframe = None
    try:
        df_all = pd.read_csv(tum_data_dosya_adi)
        main_dataframe = df_all
        if bugun not in main_dataframe['Open Time'].values:
            bugunun_datasi = pd.read_csv(f'{folder_path}{coin}_{bugun}.csv')
            main_dataframe = pd.concat([main_dataframe, bugunun_datasi])
    except:
        # load all files
        file_list = glob.glob(folder_path + "*.csv")
        main_dataframe = pd.DataFrame(pd.read_csv(file_list[0]))
        for i in range(1, len(file_list)):
            data = pd.read_csv(file_list[i])
            # df = pd.DataFrame(data)
            main_dataframe = pd.concat([main_dataframe, data])
    main_dataframe[["Open Time"]].apply(pd.to_datetime)
    main_dataframe = main_dataframe.sort_values(by='Open Time', ascending=False, ignore_index=True)
    main_dataframe = main_dataframe.interpolate()
    main_dataframe.to_csv(tum_data_dosya_adi, index=False)
    return main_dataframe


def train_kirp_yeniden_adlandir(df):
    train = df.iloc[:, :2]
    train = train.rename(columns={"Open Time": "ds"})
    train = train.rename(columns={"High": "y"})
    return train


def addit_kirp(df):
    return df.iloc[:, 2:]


def kaydir_birlestir(train, additional_data):
    train = train.iloc[:-1, :]
    future_add_data = additional_data.iloc[:1, :]
    additional_data = additional_data.iloc[1:, :].reset_index(drop=True)
    train = pd.concat([train, additional_data], axis=1)
    return train, future_add_data


def model_verisini_getir(coin, bugun):
    # TODO:: elimizdeki butun datayi df olarak al
    # TODO:: train ve additional data framelerini hazirla
    df = butun_dosyalari_yukle(coin, bugun)
    train = train_kirp_yeniden_adlandir(df)
    additional_data = addit_kirp(df)
    train, future_add_data = kaydir_birlestir(train, additional_data)
    return train, future_add_data


if __name__ == '__main__':
    bugun = '2021-12-06'
    model_verisini_getir('ETHUSDT', bugun)