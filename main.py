from historical_weather import load_historical_weather
from electricity import load_electricity_demand
from model import train_model
from plot import create_plot


def main():

    print("==========================================")
    print("関東電力需要予測システム")
    print("==========================================")

    df_temperature = load_historical_weather()
    df_demand = load_electricity_demand()

    model, df_model = train_model(
        df_temperature,
        df_demand
    )

    # 二次回帰グラフを作成
    create_plot(df_model)

    print("\n==========================================")
    print("機械学習モデルの作成が完了しました")
    print("==========================================")

    print("学習データ件数:", len(df_model))


if __name__ == "__main__":
    main()
