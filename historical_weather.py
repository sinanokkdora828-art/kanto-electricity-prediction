import pandas as pd


def load_historical_weather():

    print("過去の気温データを読み込みます")

    # ==========================================
    # ① ファイル設定
    # ==========================================

    temperature_files = [
        "data/kantotem2023.csv",
        "data/kantotem2024.csv",
        "data/kantotem2025.csv"
    ]

    # 代表地点とCSV内の列番号
    cities = {
        "東京": 1,
        "さいたま": 10,
        "宇都宮": 19,
        "前橋": 28,
        "水戸": 37,
        "千葉": 46,
        "横浜": 55
    }

    # 代表地点と都道府県の対応
    city_to_pref = {
        "水戸": "茨城県",
        "宇都宮": "栃木県",
        "前橋": "群馬県",
        "さいたま": "埼玉県",
        "千葉": "千葉県",
        "東京": "東京都",
        "横浜": "神奈川県"
    }

    # 都道府県人口
    population = {
        "茨城県": 2810000,
        "栃木県": 1900000,
        "群馬県": 1900000,
        "埼玉県": 7300000,
        "千葉県": 6300000,
        "東京都": 14100000,
        "神奈川県": 9200000
    }

    # ==========================================
    # ② CSVから日別データを抽出
    # ==========================================

    results = []

    for file in temperature_files:

        print(f"処理中: {file}")

        raw = pd.read_csv(
            file,
            encoding="cp932",
            header=None,
            skiprows=6,
            engine="python"
        )

        for city, col in cities.items():

            temp = pd.DataFrame({
                "日付": raw.iloc[:, 0],
                "都道府県": city_to_pref[city],
                "代表地点": city,
                "最高気温": raw.iloc[:, col],
                "最低気温": raw.iloc[:, col + 3],
                "平均気温": raw.iloc[:, col + 6]
            })

            results.append(temp)

    # ==========================================
    # ③ 7都県のデータを結合
    # ==========================================

    df_temperature = pd.concat(
        results,
        ignore_index=True
    )

    # ==========================================
    # ④ データ型を変換
    # ==========================================

    df_temperature["日付"] = pd.to_datetime(
        df_temperature["日付"],
        errors="coerce"
    )

    for column in [
        "最高気温",
        "最低気温",
        "平均気温"
    ]:

        df_temperature[column] = pd.to_numeric(
            df_temperature[column],
            errors="coerce"
        )

    # ==========================================
    # ⑤ 欠損値を削除
    # ==========================================

    df_temperature = df_temperature.dropna(
        subset=[
            "日付",
            "最高気温",
            "最低気温",
            "平均気温"
        ]
    ).copy()

    # ==========================================
    # ⑥ 人口・年月・月を追加
    # ==========================================

    df_temperature["人口"] = (
        df_temperature["都道府県"].map(population)
    )

    df_temperature["年月"] = (
        df_temperature["日付"]
        .dt.to_period("M")
        .astype(str)
    )

    df_temperature["月"] = (
        df_temperature["日付"].dt.month
    )

    # ==========================================
    # ⑦ CDD・HDDを計算
    # ==========================================

    # CDD：平均気温が24℃を超えた分
    df_temperature["CDD"] = (
        df_temperature["平均気温"] - 24
    ).clip(lower=0)

    # HDD：平均気温が14℃を下回った分
    df_temperature["HDD"] = (
        14 - df_temperature["平均気温"]
    ).clip(lower=0)

    # ==========================================
    # ⑧ 月別に集計
    # ==========================================

    df_temperature_monthly = (
        df_temperature
        .groupby(
            ["年月", "都道府県"],
            as_index=False
        )
        .agg(

            平均気温_月平均=(
                "平均気温",
                "mean"
            ),

            最高気温_月最高=(
                "最高気温",
                "max"
            ),

            最低気温_月最低=(
                "最低気温",
                "min"
            ),

            CDD=(
                "CDD",
                "sum"
            ),

            HDD=(
                "HDD",
                "sum"
            ),

            観測日数=(
                "日付",
                "count"
            ),

            人口=(
                "人口",
                "first"
            )
        )
    )

    # ==========================================
    # ⑨ 観測日数が20日未満のデータを除外
    # ==========================================

    df_temperature_monthly = (
        df_temperature_monthly[
            df_temperature_monthly["観測日数"] >= 20
        ]
        .copy()
    )

    # ==========================================
    # ⑩ 並び替え
    # ==========================================

    df_temperature_monthly = (
        df_temperature_monthly
        .sort_values(
            ["年月", "都道府県"]
        )
        .reset_index(drop=True)
    )

    # ==========================================
    # ⑪ データ確認
    # ==========================================

    print("月別気温データ作成完了")

    print(
        "データ件数:",
        len(df_temperature_monthly)
    )

    print(
        df_temperature_monthly.head(10)
    )

    print(
        "開始年月:",
        df_temperature_monthly["年月"].min()
    )

    print(
        "終了年月:",
        df_temperature_monthly["年月"].max()
    )

    return df_temperature_monthly
