import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


def train_model(df_temperature, df_demand):

    print("機械学習モデルを作成します")

    # ==========================================
    # ① 気温データと電力需要データを結合
    # ==========================================

    df_model = pd.merge(
        df_temperature,
        df_demand,
        on=["年月", "都道府県"],
        how="inner"
    )

    print("結合後のデータ件数:", len(df_model))

    if len(df_model) == 0:
        raise ValueError(
            "気温データと電力需要データを結合できませんでした"
        )

    # ==========================================
    # ② 欠損値を削除
    # ==========================================

    df_model = df_model.dropna(
        subset=[
            "平均気温_月平均",
            "人口",
            "電力需要_Wh"
        ]
    )

    print("欠損値削除後のデータ件数:", len(df_model))

    # ==========================================
    # ③ 説明変数を作成
    # ==========================================

    temperature = df_model["平均気温_月平均"]
    population = df_model["人口"]

    # 気温の二次項を追加
    X = pd.DataFrame({
        "気温": temperature,
        "気温²": temperature ** 2,
        "人口": population
    })

    # 予測対象
    y = df_model["電力需要_Wh"]

    # ==========================================
    # ④ 二次回帰モデルを学習
    # ==========================================

    model = LinearRegression()

    model.fit(X, y)

    print("\n二次回帰モデルの学習が完了しました")

    # ==========================================
    # ⑤ モデル評価
    # ==========================================

    y_pred = model.predict(X)

    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)

    print("\n==========================================")
    print("モデル評価")
    print("==========================================")

    print("平均絶対誤差（MAE）:", mae)
    print("決定係数（R²）:", r2)

    # ==========================================
    # ⑥ モデルの係数
    # ==========================================

    print("\n==========================================")
    print("モデルの係数")
    print("==========================================")

    print("切片:", model.intercept_)

    for name, coefficient in zip(X.columns, model.coef_):
        print(name, ":", coefficient)

    return model, df_model
