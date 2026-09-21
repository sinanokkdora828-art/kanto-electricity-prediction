from historical_weather import load_historical_weather
from electricity import load_electricity_demand
from model import train_model


def main():

    print("==========================================")
    print("関東電力需要予測システム")
    print("==========================================")

    # ① 過去の気温データを読み込む
    df_temperature = load_historical_weather()

    # ② 電力需要データを読み込む
    df_demand = load_electricity_demand()

    # ③ 機械学習モデルを作成
    model, df_model = train_model(
        df_temperature,
        df_demand
    )

    print("\n==========================================")
    print("機械学習モデルの作成が完了しました")
    print("==========================================")

    print("学習データ件数:", len(df_model))


if __name__ == "__main__":
    main()
