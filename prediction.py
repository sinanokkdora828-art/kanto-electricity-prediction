import pandas as pd


# ==========================================
# ① JMA予報期間の平均気温を計算
# ==========================================

def calculate_forecast_average(df_forecast):

    print("\n==========================================")
    print("予報期間の平均気温を計算します")
    print("==========================================")

    # 都道府県ごとに予報気温の平均を計算
    df_average = (
        df_forecast
        .groupby("都道府県")
        .agg(
            予測気温=("気温", "mean")
        )
        .reset_index()
    )

    print("\n予報期間の平均気温")

    print(df_average.to_string(index=False))

    return df_average


# ==========================================
# ② 機械学習モデルで電力需要を予測
# ==========================================

def predict_electricity_demand(
    model,
    df_forecast
):

    print("\n==========================================")
    print("将来の電力需要を予測します")
    print("==========================================")

    # 機械学習モデルに入力するデータを作成
    #
    # 学習時と同じ3つの説明変数
    # ・気温
    # ・気温²
    # ・人口
    #

    X_future = pd.DataFrame({

        "気温": df_forecast["予測気温"],

        "気温²": (
            df_forecast["予測気温"] ** 2
        ),

        "人口": df_forecast["人口"]

    })

    print("\n機械学習モデルへの入力データ")

    print(
        X_future.to_string(index=False)
    )

    # ==========================================
    # 電力需要を予測
    # ==========================================

    predicted_demand = model.predict(
        X_future
    )

    # 元のDataFrameをコピー
    df_result = df_forecast.copy()

    # 予測電力需要を追加
    df_result["予測電力需要_Wh"] = (
        predicted_demand
    )

    # 兆Whに変換
    df_result["予測電力需要_兆Wh"] = (
        df_result["予測電力需要_Wh"] / 1e12
    )

    # ==========================================
    # 結果を表示
    # ==========================================

    print("\n==========================================")
    print("予測結果")
    print("==========================================")

    print(
        df_result[
            [
                "都道府県",
                "予測気温",
                "人口",
                "予測電力需要_Wh",
                "予測電力需要_兆Wh"
            ]
        ].to_string(index=False)
    )

    return df_result
