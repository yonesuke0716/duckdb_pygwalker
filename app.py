import duckdb
from sklearn.datasets import load_iris, load_wine
import pandas as pd

from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html
import streamlit as st
import streamlit.components.v1 as components

# Streamlitページの幅を調整する
st.set_page_config(page_title="StreamlitでPygwalkerを使う", layout="wide")

# PyGWalkerとStreamlitの通信を確立する
init_streamlit_comm()

st.title("DuckDB+pygwalkerによるデータ分析")
# Scikit-learnのIrisデータをロード
iris = load_iris()
iris_data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
iris_data["target"] = iris.target

# Scikit-learnのWineデータをロード
wine = load_wine()
wine_data = pd.DataFrame(data=wine.data, columns=wine.feature_names)
wine_data["target"] = wine.target

wine_data.to_csv("wine_data.csv", index=False)


# `use_kernel_calc=True`を使用する場合は、pygwalkerのHTMLをキャッシュする必要があります（メモリが爆発しないようにするため）
@st.cache_resource
def get_pyg_html(df: pd.DataFrame) -> str:
    # アプリケーションを公開する必要がある場合、`debug=False`に設定し、他のユーザーが設定ファイルを書き換えるのを防ぎます。
    # チャートの設定を保存する機能を使用したい場合は、`debug=True`に設定します。
    html = get_streamlit_html(df, spec="./gw0.json", use_kernel_calc=True, debug=False)
    return html


@st.cache_data
def get_df() -> pd.DataFrame:
    return pd.read_csv("/bike_sharing_dc.csv")


# df = get_df()

components.html(get_pyg_html(wine_data), width=1300, height=1000, scrolling=True)


# # DB の作成
# conn = duckdb.connect("wine.duckdb")
# c = conn.cursor()

# # CSV からデータをインポートしてテーブルを作成
# c.execute("CREATE TABLE wine AS SELECT * FROM read_csv_auto('wine_data.csv');")

# # DuckDBで簡単なクエリを実行
# result = c.execute(
#     "SELECT AVG(alcohol), MAX(color_intensity) FROM wine WHERE target = 1;"
# ).fetchall()
# print("平均 alcohol:", result[0][0])
# print("最大 color_intensity:", result[0][1])

# # DuckDBとの接続を閉じる
# c.close()
