import pandas as pd

from historical_weather import load_historical_weather
from electricity import load_electricity_demand
from model import train_model
from plot import create_plot
from prediction import predict_electricity_demand


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

    # ==========================================
    # 将来の電力需要予測
    # ==========================================

    df_forecast = pd.DataFrame({

        "都道府県": [
            "茨城県",
            "栃木県",
            "群馬県",
            "埼玉県",
            "千葉県",
            "東京都",
            "神奈川県"
        ],

        "予測気温": [
            25.0,
            24.5,
            27.0,
            26.0,
            25.5,
            25.0,
            24.5
        ],

        "人口": [
            2810000,
            1900000,
            1900000,
            7300000,
            6300000,
            14100000,
            9200000
        ]

    })

    # 予測処理
    df_prediction = predict_electricity_demand(
        model,
        df_forecast
    )


if __name__ == "__main__":
    main()
