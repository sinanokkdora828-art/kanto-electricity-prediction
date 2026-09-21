import pandas as pd


def load_historical_weather():

    print("過去の気温データを読み込みます")

    df_2023 = pd.read_csv(
        "data/kantotem2023.csv",
        encoding="cp932",
        skiprows=6
    )

    df_2024 = pd.read_csv(
        "data/kantotem2024.csv",
        encoding="cp932",
        skiprows=6
    )

    df_2025 = pd.read_csv(
        "data/kantotem2025.csv",
        encoding="cp932",
        skiprows=6
    )

    df = pd.concat(
        [df_2023, df_2024, df_2025],
        ignore_index=True
    )

    print("過去の気温データ読み込み完了")
    print("データ件数:", len(df))

    return df
