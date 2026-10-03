import requests
import pandas as pd


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


def load_weather_forecast():

    results = []

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

        temperature_data = None

        for time_series in data[0]["timeSeries"]:

            if "temps" in time_series["areas"][0]:
                temperature_data = time_series
                break

        if temperature_data is None:
            print("気温データが見つかりません:", pref)
            continue

        target_area = None

        for area in temperature_data["areas"]:

            if area["area"]["code"] == info["city_code"]:
                target_area = area
                break

        if target_area is None:
            print("代表地点が見つかりません:", pref)
            continue

        time_defines = temperature_data["timeDefines"]
        temps = target_area["temps"]

        temp = pd.DataFrame({
            "都道府県": pref,
            "代表地点": info["代表地点"],
            "日時": time_defines,
            "気温": temps
        })

        temp["日時"] = pd.to_datetime(
            temp["日時"],
            errors="coerce"
        )

        temp["気温"] = pd.to_numeric(
            temp["気温"],
            errors="coerce"
        )

        results.append(temp)

    if not results:
        raise ValueError("気温データを取得できませんでした")

    df_forecast = pd.concat(
        results,
        ignore_index=True
    )

    return df_forecast
