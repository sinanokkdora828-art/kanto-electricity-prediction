import os
import matplotlib

# 画面表示なしで画像を作成
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from sklearn.linear_model import LinearRegression


# ==========================================
# 日本語フォント設定
# ==========================================

font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

if os.path.exists(font_path):

    fm.fontManager.addfont(font_path)

    font_prop = fm.FontProperties(fname=font_path)
    font_name = font_prop.get_name()

    plt.rcParams["font.family"] = font_name
    plt.rcParams["axes.unicode_minus"] = False

else:

    print("日本語フォントが見つかりません")

def create_plot(df_model):

    print("二次回帰グラフを作成します")

    prefectures = [
        "茨城県",
        "栃木県",
        "群馬県",
        "埼玉県",
        "千葉県",
        "東京都",
        "神奈川県"
    ]

    plt.figure(figsize=(12, 7))

    for pref in prefectures:

        # 都県ごとのデータ
        df_pref = df_model[
            df_model["都道府県"] == pref
        ].copy()

        if len(df_pref) < 3:
            print(f"{pref}: データ不足のためスキップ")
            continue

        T = df_pref["平均気温_月平均"].to_numpy()
        y = df_pref["電力需要_Wh"].to_numpy()

        # 実測値
        plt.scatter(
            T,
            y / 1e12,
            alpha=0.5,
            label=pref
        )

        # ======================================
        # 二次回帰
        # ======================================

        X = np.column_stack([
            T,
            T ** 2
        ])

        model_pref = LinearRegression()
        model_pref.fit(X, y)

        # 回帰曲線
        T_line = np.linspace(
            T.min(),
            T.max(),
            100
        )

        X_line = np.column_stack([
            T_line,
            T_line ** 2
        ])

        y_line = model_pref.predict(X_line)

        plt.plot(
            T_line,
            y_line / 1e12,
            linewidth=2
        )

    # ======================================
    # グラフ設定
    # ======================================

    plt.xlabel("月平均気温（℃）")
    plt.ylabel("月間電力需要（兆Wh）")

    plt.title(
        "都県別：月平均気温と月間電力需要の関係"
    )

    plt.grid(True, alpha=0.3)
    plt.legend(title="都県")
    plt.tight_layout()

    # ======================================
    # 保存
    # ======================================

    os.makedirs("results", exist_ok=True)

    output_path = "results/temperature_demand_quadratic.png"

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"グラフを保存しました: {output_path}")
