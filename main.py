import os
import shutil
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

from map_plot import create_prediction_map


def main():

    print("==========================================")
    print("関東電力需要予測システム")
    print("==========================================")


    # ==========================================
    # STEP 1
    # 過去の気温データを読み込む
    # ==========================================

    print("\n【STEP 1】")
    print("過去の気温データを読み込みます")

    df_temperature = load_historical_weather()


    # ==========================================
    # STEP 2
    # 過去の電力需要データを読み込む
    # ==========================================

    print("\n【STEP 2】")
    print("過去の電力需要データを読み込みます")

    df_demand = load_electricity_demand()


    # ==========================================
    # STEP 3
    # 機械学習モデルを作成
    # ==========================================

    print("\n【STEP 3】")
    print("機械学習モデルを作成します")

    model, df_model = train_model(
        df_temperature,
        df_demand
    )


    # ==========================================
    # STEP 4
    # 学習結果のグラフを作成
    # ==========================================

    print("\n【STEP 4】")
    print("学習結果のグラフを作成します")

    create_plot(df_model)


    # ==========================================
    # STEP 5
    # 気象庁から最新の予報気温を取得
    # ==========================================

    print("\n【STEP 5】")
    print("気象庁から最新の予報気温を取得します")

    df_forecast_raw = load_weather_forecast()


    print("\nJMAから取得した予報データ")

    print(
        df_forecast_raw.to_string(index=False)
    )


    # ==========================================
    # STEP 6
    # 予報期間の平均気温を計算
    # ==========================================

    print("\n【STEP 6】")
    print("予報期間の平均気温を計算します")

    df_forecast = calculate_forecast_average(
        df_forecast_raw
    )


    # ==========================================
    # STEP 7
    # 将来の電力需要を予測
    # ==========================================

    print("\n【STEP 7】")
    print("将来の電力需要を予測します")

    df_prediction = predict_electricity_demand(
        model,
        df_forecast
    )


    # ==========================================
    # STEP 8
    # 電力需要予測マップを作成
    # ==========================================

    print("\n【STEP 8】")
    print("予測結果の地図を作成します")

    create_prediction_map(
        df_prediction
    )


    # ==========================================
    # STEP 9
    # GitHub Pages用に画像をコピー
    # ==========================================

    print("\n【STEP 9】")
    print("GitHub Pages用の画像を準備します")

    # docs/results フォルダを作成
    os.makedirs(
        "docs/results",
        exist_ok=True
    )


    # 予測マップをGitHub Pages用フォルダへコピー
    shutil.copy(
        "results/kanto_electricity_prediction.png",
        "docs/results/kanto_electricity_prediction.png"
    )


    print(
        "GitHub Pages用の画像をコピーしました"
    )


    # ==========================================
    # STEP 10
    # 予測結果CSVを保存
    # ==========================================

    print("\n【STEP 10】")
    print("予測結果をCSVとして保存します")

    df_prediction.to_csv(
        "prediction.csv",
        index=False,
        encoding="utf-8-sig"
    )


    print(
        "予測結果を prediction.csv に保存しました"
    )


    # ==========================================
    # 最終結果
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
    # 生成されたファイルを表示
    # ==========================================

    print("\n==========================================")
    print("生成されたファイル")
    print("==========================================")


    print(
        "予測結果CSV："
        "prediction.csv"
    )

    print(
        "予測グラフ："
        "results/temperature_demand_quadratic.png"
    )

    print(
        "予測マップ："
        "results/kanto_electricity_prediction.png"
    )

    print(
        "GitHub Pages用画像："
        "docs/results/kanto_electricity_prediction.png"
    )


    print("\n==========================================")
    print("すべての処理が完了しました")
    print("==========================================")


# ==========================================
# プログラム開始
# ==========================================

if __name__ == "__main__":
    main()
