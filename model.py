import pandas as pd
from sklearn.linear_model import LinearRegression


def train_model(df_temperature, df_demand):

    print("機械学習モデルを作成します")

    # 動作確認用のデータを結合
    df_model = pd.DataFrame({
        "平均気温": [20, 25, 30],
        "人口": [1000000, 1000000, 1000000],
        "電力需要": [100, 150, 200]
    })

    X = df_model[
        ["平均気温", "人口"]
    ]

    y = df_model["電力需要"]

    model = LinearRegression()

    model.fit(X, y)

    print("機械学習モデルの学習が完了しました")

    return model, df_model
