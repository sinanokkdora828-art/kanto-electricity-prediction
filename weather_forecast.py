import requests
import pandas as pd

# ==========================================
# ① 関東7都県の情報
# ==========================================

prefectures = {
    "茨城県": {
        "pref_code": "080000",
        "代表地点": "水戸",
        "city_code": "40201"
    },
    "栃木県": {
        "pref_code": "090000",
        "代表地点": "宇都宮",
        "city_code": "41277"
    },
    "群馬県": {
        "pref_code": "100000",
        "代表地点": "前橋",
        "city_code": "42251"
    },
    "埼玉県": {
        "pref_code": "110000",
        "代表地点": "さいたま",
        "city_code": "43056"
    },
    "千葉県": {
        "pref_code": "120000",
        "代表地点": "千葉",
        "city_code": "45212"
    },
    "東京都": {
        "pref_code": "130000",
        "代表地点": "東京",
        "city_code": "44132"
    },
    "神奈川県": {
        "pref_code": "140000",
        "代表地点": "横浜",
        "city_code": "46106"
    }
}


# ==========================================
# ② 予報データを入れるリスト
# ==========================================

results = []


# ==========================================
# ③ 7都県について順番にJSONを取得
# ==========================================

for pref, info in prefectures.items():

    print("取得中:", pref)

    url = (
        "https://www.jma.go.jp/bosai/forecast/data/forecast/"
        + info["pref_code"]
        + ".json"
    )

    response = requests.get(url, timeout=30)

    response.raise_for_status()

    data = response.json()


    # ==========================================
    # ④ 気温データを持つtimeSeriesを探す
    # ==========================================

    temperature_data = None

    for time_series in data[0]["timeSeries"]:

        if "temps" in time_series["areas"][0]:

            temperature_data = time_series
            break


    if temperature_data is None:

        print("気温データが見つかりません:", pref)

        continue


    # ==========================================
    # ⑤ 代表地点を探す
    # ==========================================

    target_area = None

    for area in temperature_data["areas"]:

        if area["area"]["code"] == info["city_code"]:

            target_area = area
            break


    if target_area is None:

        print("代表地点が見つかりません:", pref)

        continue


    # ==========================================
    # ⑥ 時刻と気温を取得
    # ==========================================

    time_defines = temperature_data["timeDefines"]

    temps = target_area["temps"]


    # ==========================================
    # ⑦ DataFrameを作成
    # ==========================================

    temp = pd.DataFrame({

        "都道府県": pref,

        "代表地点": info["代表地点"],

        "日時": time_defines,

        "気温": temps

    })


    # ==========================================
    # ⑧ データ型を変換
    # ==========================================

    temp["日時"] = pd.to_datetime(
        temp["日時"],
        errors="coerce"
    )

    temp["気温"] = pd.to_numeric(
        temp["気温"],
        errors="coerce"
    )


    # ==========================================
    # ⑨ 結果を保存
    # ==========================================

    results.append(temp)


# ==========================================
# ⑩ 7都県のデータを結合
# ==========================================

if not results:

    raise ValueError("気温データを1件も取得できませんでした")

df_forecast = pd.concat(
    results,
    ignore_index=True
)


# ==========================================
# ⑪ 並び替え
# ==========================================

df_forecast = df_forecast.sort_values(
    ["都道府県", "日時"]
).reset_index(drop=True)


# ==========================================
# ⑫ 確認
# ==========================================

print("\n==========================================")
print("関東7都県の予報気温")
print("==========================================")

print(df_forecast.to_string(index=False))


# ==========================================
# ⑬ CSVファイルに保存
# ==========================================

df_forecast.to_csv(
    "forecast.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nCSVファイルを保存しました")
