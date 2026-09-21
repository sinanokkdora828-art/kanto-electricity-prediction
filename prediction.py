import pandas as pd


def predict_electricity_demand(
    model,
    df_forecast
):

    print("\n==========================================")
    print("将来の電力需要を予測します")
    print("==========================================")

    # 機械学習モデルに入力するデータ
    X_future = pd.DataFrame({

        "気温": df_forecast["予測気温"],

        "気温²": df_forecast["予測気温"] ** 2,

        "人口": df_forecast["人口"]

    })

    # 電力需要を予測
    predicted_demand = model.predict(X_future)

    # 結果を追加
    df_forecast = df_forecast.copy()

    df_forecast["予測電力需要_Wh"] = predicted_demand

    # 兆Whに変換
    df_forecast["予測電力需要_兆Wh"] = (
        df_forecast["予測電力需要_Wh"] / 1e12
    )

    print("\n予測結果")

    print(
        df_forecast[
            [
                "都道府県",
                "予測気温",
                "予測電力需要_兆Wh"
            ]
        ]
    )

    return df_forecast
