import pandas as pd
from pathlib import Path


def load_electricity_demand():

    print("電力需要データを読み込みます")

    data_folder = Path("data")

    files = [
        data_folder / "jyuyou2023.xlsx",
        data_folder / "jyuyou2024.xlsx",
        data_folder / "jyuyou2025.xlsx"
    ]

    dataframes = []

    for file in files:

        print(f"読み込み中: {file}")

        excel = pd.ExcelFile(file)

        print("シート名:", excel.sheet_names)

        for sheet_name in excel.sheet_names:

            df = pd.read_excel(
                file,
                sheet_name=sheet_name,
                header=None
            )

            df["年度ファイル"] = file.name
            df["シート名"] = sheet_name

            dataframes.append(df)

    result = pd.concat(
        dataframes,
        ignore_index=True
    )

    print("電力需要データ読み込み完了")
    print("データ件数:", len(result))

    return result
