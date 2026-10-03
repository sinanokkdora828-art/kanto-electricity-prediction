import os
import requests
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
import geopandas as gpd
import pandas as pd


# ==========================================
# 日本語フォント設定
# ==========================================

font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

if os.path.exists(font_path):

    fm.fontManager.addfont(font_path)

    font_prop = fm.FontProperties(
        fname=font_path
    )

    plt.rcParams["font.family"] = (
        font_prop.get_name()
    )

else:

    print("日本語フォントが見つかりません")


plt.rcParams["axes.unicode_minus"] = False


# ==========================================
# 都道府県の表示位置
# ==========================================

card_positions = {

    "群馬県": (138.25, 36.15),

    "栃木県": (139.35, 36.55),

    "茨城県": (140.65, 36.25),

    "埼玉県": (138.55, 35.75),

    "千葉県": (140.65, 35.65),

    "東京都": (139.85, 35.35),

    "神奈川県": (138.55, 35.05)

}


# ==========================================
# 代表地点
# ==========================================

city_positions = {

    "群馬県": (139.06, 36.39),

    "栃木県": (139.88, 36.56),

    "茨城県": (140.47, 36.37),

    "埼玉県": (139.65, 35.86),

    "千葉県": (140.11, 35.61),

    "東京都": (139.65, 35.68),

    "神奈川県": (139.64, 35.44)

}


# ==========================================
# GeoJSON取得
# ==========================================

def load_kanto_map():

    url = (
        "https://raw.githubusercontent.com/"
        "kyodo-official/japan-choropleth/"
        "main/data/geojson/prefectures.geojson"
    )

    print("関東地方の地図データを取得しています...")

    response = requests.get(
        url,
        timeout=30
    )

    response.raise_for_status()

    geojson_path = "kanto_prefectures.geojson"

    with open(
        geojson_path,
        "wb"
    ) as f:

        f.write(
            response.content
        )

    gdf = gpd.read_file(
        geojson_path
    )

    # ==========================================
    # 関東7都県だけ抽出
    # ==========================================

    kanto_codes = [

        "08",  # 茨城
        "09",  # 栃木
        "10",  # 群馬
        "11",  # 埼玉
        "12",  # 千葉
        "13",  # 東京
        "14"   # 神奈川

    ]

    gdf["id"] = (
        gdf["id"]
        .astype(str)
        .str.zfill(2)
    )

    gdf = gdf[
        gdf["id"].isin(kanto_codes)
    ].copy()

    return gdf


# ==========================================
# 地図画像作成
# ==========================================

def create_prediction_map(df_prediction):

    print("\n==========================================")
    print("電力需要予測マップを作成します")
    print("==========================================")


    # ==========================================
    # データ確認
    # ==========================================

    required_columns = [

        "都道府県",

        "予測気温",

        "予測電力需要_兆Wh"

    ]

    for column in required_columns:

        if column not in df_prediction.columns:

            raise ValueError(
                f"必要な列がありません: {column}"
            )


    # ==========================================
    # 地図データ取得
    # ==========================================

    gdf = load_kanto_map()


    # ==========================================
    # 描画領域
    # ==========================================

    fig, ax = plt.subplots(
        figsize=(12, 9),
        dpi=150
    )


    # ==========================================
    # 背景
    # ==========================================

    fig.patch.set_facecolor(
        "#eeeeee"
    )

    ax.set_facecolor(
        "#eeeeee"
    )


    # ==========================================
    # 関東地方を描画
    # ==========================================

    gdf.plot(

        ax=ax,

        color="#dcefd8",

        edgecolor="#333333",

        linewidth=1.5

    )


    # ==========================================
    # 地図範囲
    # ==========================================

    ax.set_xlim(
        138.15,
        140.95
    )

    ax.set_ylim(
        34.95,
        36.95
    )


    # ==========================================
    # タイトル
    # ==========================================

    ax.text(

        0.5,
        1.08,

        "⚡ 関東地方 1か月電力需要予測",

        transform=ax.transAxes,

        ha="center",

        va="center",

        fontsize=23,

        fontweight="bold",

        color="#222222",

        bbox=dict(

            boxstyle="round,pad=0.55",

            facecolor="white",

            edgecolor="#dddddd",

            linewidth=1.2

        )

    )


    # ==========================================
    # 各都県のカードを描画
    # ==========================================

    for _, row in df_prediction.iterrows():

        pref = row["都道府県"]

        temperature = row["予測気温"]

        demand = row["予測電力需要_兆Wh"]


        # --------------------------------------
        # カード位置
        # --------------------------------------

        card_x, card_y = card_positions[pref]


        # --------------------------------------
        # 代表地点
        # --------------------------------------

        city_x, city_y = city_positions[pref]


        # --------------------------------------
        # 表示文字
        # --------------------------------------

        text = (

            f"{pref}\n"

            f"\n"

            f"予報代表気温：{temperature:.1f} ℃\n"

            f"\n"

            f"⚡ {demand:.2f} 兆Wh"

        )


        # ======================================
        # 代表地点からカードへ線を引く
        # ======================================

        ax.annotate(

            "",

            xy=(city_x, city_y),

            xytext=(card_x, card_y),

            arrowprops=dict(

                arrowstyle="-",

                color="#555555",

                linewidth=1.3

            )

        )


        # ======================================
        # 代表地点の丸
        # ======================================

        ax.scatter(

            city_x,

            city_y,

            s=80,

            facecolor="white",

            edgecolor="#222222",

            linewidth=1.5,

            zorder=10

        )


        # ======================================
        # カード
        # ======================================

        ax.text(

            card_x,

            card_y,

            text,

            ha="center",

            va="center",

            fontsize=11,

            color="#333333",

            zorder=20,

            bbox=dict(

                boxstyle="round,pad=0.8",

                facecolor="white",

                edgecolor="#dddddd",

                linewidth=1.2,

                alpha=0.98

            )

        )


    # ==========================================
    # 単位表示
    # ==========================================

    ax.text(

        0.97,

        0.04,

        "⚡ 単位：兆Wh",

        transform=ax.transAxes,

        ha="right",

        va="bottom",

        fontsize=11,

        color="#333333",

        bbox=dict(

            boxstyle="round,pad=0.4",

            facecolor="white",

            edgecolor="#bbbbbb"

        )

    )


    # ==========================================
    # 軸などを消す
    # ==========================================

    ax.axis("off")


    # ==========================================
    # 画像保存
    # ==========================================

    os.makedirs(
        "results",
        exist_ok=True
    )

    output_path = (
        "results/"
        "kanto_electricity_prediction.png"
    )

    plt.savefig(

        output_path,

        dpi=150,

        bbox_inches="tight",

        facecolor=fig.get_facecolor()

    )

    plt.close()


    print(
        f"\n予測マップを保存しました: "
        f"{output_path}"
    )

    return output_path
