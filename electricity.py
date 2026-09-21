import pandas as pd


def load_electricity_demand():

    print("電力需要データを読み込みます")

    # ==========================================
    # ① 読み込むExcelファイル
    # ==========================================

    files = [
        "data/jyuyou2023.xlsx",
        "data/jyuyou2024.xlsx",
        "data/jyuyou2025.xlsx"
    ]

    # 関東7都県
    kanto = [
        "茨城県",
        "栃木県",
        "群馬県",
        "埼玉県",
        "千葉県",
        "東京都",
        "神奈川県"
    ]

    results = []

    # ==========================================
    # ② Excelファイルごとに処理
    # ==========================================

    for file in files:

        print("読み込み中:", file)

        excel = pd.ExcelFile(file)

        print("シート名:", excel.sheet_names)

        # ==========================================
        # ③ 月別シートを処理
        # ==========================================

        for sheet in excel.sheet_names:

            # Sheet1・年度シートを除外
            if "." not in sheet:
                continue

            print("  → 処理中:", sheet)

            # シートを読み込む
            raw = pd.read_excel(
                file,
                sheet_name=sheet,
                header=None
            )

            # データ部分を抽出
            data = raw.iloc[4:].copy()

            # ==========================================
            # ④ 都道府県と電力需要を抽出
            # ==========================================

            temp = pd.DataFrame({
                "都道府県": data.iloc[:, 0],
                "電力需要_1000kWh": data.iloc[:, 9]
            })

            # 関東7都県だけを残す
            temp = temp[
                temp["都道府県"].isin(kanto)
            ].copy()

            # ==========================================
            # ⑤ 電力需要を数値化
            # ==========================================

            temp["電力需要_1000kWh"] = (
                temp["電力需要_1000kWh"]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.strip()
            )

            temp["電力需要_1000kWh"] = pd.to_numeric(
                temp["電力需要_1000kWh"],
                errors="coerce"
            )

            # 欠損値を削除
            temp = temp.dropna(
                subset=["電力需要_1000kWh"]
            )

            # ==========================================
            # ⑥ 年月を統一
            # ==========================================

            # 例：2023.9 → 2023-09
            year, month = sheet.split(".")

            temp["年月"] = (
                f"{int(year):04d}-{int(month):02d}"
            )

            results.append(temp)

    # ==========================================
    # ⑦ 全データを結合
    # ==========================================

    if not results:
        raise ValueError(
            "電力需要データを読み込めませんでした"
        )

    df_demand = pd.concat(
        results,
        ignore_index=True
    )

    # ==========================================
    # ⑧ 単位を変換
    # ==========================================

    # 1000kWh → kWh
    df_demand["電力需要_kWh"] = (
        df_demand["電力需要_1000kWh"] * 1000
    )

    # kWh → Wh
    df_demand["電力需要_Wh"] = (
        df_demand["電力需要_kWh"] * 1000
    )

    # ==========================================
    # ⑨ 不要な列を整理
    # ==========================================

    df_demand = df_demand[
        [
            "年月",
            "都道府県",
            "電力需要_1000kWh",
            "電力需要_kWh",
            "電力需要_Wh"
        ]
    ]

    # 同じ年月・都道府県の重複を確認
    duplicate_count = df_demand.duplicated(
        subset=["年月", "都道府県"]
    ).sum()

    print(
        "年月・都道府県の重複件数:",
        duplicate_count
    )

    # 重複がある場合は合計せず、最初のデータを残す
    df_demand = df_demand.drop_duplicates(
        subset=["年月", "都道府県"],
        keep="first"
    )

    # 並び替え
    df_demand = df_demand.sort_values(
        ["年月", "都道府県"]
    ).reset_index(drop=True)

    # ==========================================
    # ⑩ 結果を表示
    # ==========================================

    print("電力需要データ読み込み完了")
    print("データ件数:", len(df_demand))

    print(df_demand.head(20).to_string(index=False))

    print("開始年月:", df_demand["年月"].min())
    print("終了年月:", df_demand["年月"].max())

    return df_demand
