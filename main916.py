import requests
import pandas as pd

# ==========================================
# 東京都のJMA予報JSONを取得
# ==========================================

url = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"

response = requests.get(url)

# HTTP通信が正常だったか確認
response.raise_for_status()

# JSONをPythonのデータに変換
data = response.json()

# ==========================================
# 気温データを取得
# ==========================================

temperature_data = data[0]["timeSeries"][2]

# 日時
time_defines = temperature_data["timeDefines"]

# 東京の気温
temps = temperature_data["areas"][0]["temps"]

# ==========================================
# DataFrameにする
# ==========================================

df_forecast = pd.DataFrame({
    "日時": time_defines,
    "気温": temps
})

# ==========================================
# データ型を変換
# ==========================================

df_forecast["日時"] = pd.to_datetime(
    df_forecast["日時"]
)

df_forecast["気温"] = pd.to_numeric(
    df_forecast["気温"],
    errors="coerce"
)

# ==========================================
# 結果を表示
# ==========================================

print("================================")
print("JMA 東京 気温予報")
print("================================")

print(df_forecast)
