import pandas as pd

from historical_weather import load_historical_weather
from electricity import load_electricity_demand
from model import train_model
from plot import create_plot

from weather_forecast import load_weather_forecast

from prediction import (
    calculate_forecast_average,
    predict_electricity_demand
)


# ==========================================
# メイン処理
# ==========================================

def main():

    print("==========================================")
    print("関東電力需要予測システム")
    print("==========================================")


    # ==========================================
    # ① 過去の気温データを読み込む
    # ==========================================

    print("\n【STEP 1】")
    print("過去の気温データを読み込みます")

    df_temperature = load_historical_weather()


    # ==========================================
    # ② 過去の電力需要データを読み込む
    # ==========================================

    print("\n【STEP 2】")
    print("過去の電力需要データを読み込みます")

    df_demand = load_electricity_demand()


    # ==========================================
    # ③ 機械学習モデルを作成
    # ==========================================

    print("\n【STEP 3】")
    print("機械学習モデルを作成します")

    model, df_model = train_model(
        df_temperature,
        df_demand
    )


    # ==========================================
    # ④ 学習結果のグラフを作成
    # ==========================================

    print("\n【STEP 4】")
    print("学習結果のグラフを作成します")

    create_plot(df_model)


    # ==========================================
    # ⑤ 気象庁から最新の予報気温を取得
    # ==========================================

    print("\n【STEP 5】")
    print("気象庁から最新の予報気温を取得します")

    df_forecast_raw = load_weather_forecast()


    print("\nJMAから取得した予報データ")

    print(
        df_forecast_raw.to_string(index=False)
    )


    # ==========================================
    # ⑥ 予報期間の平均気温を計算
    #    ＋人口を追加
    # ==========================================

    print("\n【STEP 6】")
    print("予報期間の平均気温を計算します")

    df_forecast = calculate_forecast_average(
        df_forecast_raw
    )


    # ==========================================
    # ⑦ 機械学習モデルで電力需要を予測
    # ==========================================

    print("\n【STEP 7】")
    print("将来の電力需要を予測します")

    df_prediction = predict_electricity_demand(
        model,
        df_forecast
    )


    # ==========================================
    # ⑧ 最終結果を表示
    # ==========================================

    print("\n==========================================")
    print("最終予測結果")
    print("==========================================")

    print(
        df_prediction[
            [
                "都道府県",
                "予測気温",
                "人口",
                "予測電力需要_Wh",
                "予測電力需要_兆Wh"
            ]
        ].to_string(index=False)
    )


    # ==========================================
    # ⑨ 予測結果をCSVに保存
    # ==========================================

    df_prediction.to_csv(
        "prediction.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\n予測結果を prediction.csv に保存しました")


# ==========================================
# プログラム開始
# ==========================================

if __name__ == "__main__":
    main()
