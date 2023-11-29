import os
import pandas as pd
from sklearn.datasets import load_iris, load_wine

from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html
import streamlit as st
import streamlit.components.v1 as components

from libs.utils import create_duckdb, display_loadtime

# ディレクトリを作成する
os.makedirs("duckdb", exist_ok=True)
os.makedirs("csv", exist_ok=True)


# `use_kernel_calc=True`を使用する場合は、pygwalkerのHTMLをキャッシュする必要があります（メモリが爆発しないようにするため）
@st.cache_resource
def get_pyg_html(df: pd.DataFrame) -> str:
    # アプリケーションを公開する必要がある場合、`debug=False`に設定し、他のユーザーが設定ファイルを書き換えるのを防ぎます。
    # チャートの設定を保存する機能を使用したい場合は、`debug=True`に設定します。
    html = get_streamlit_html(df, use_kernel_calc=True, debug=False)
    return html


# Streamlitページの幅を調整する
st.set_page_config(page_title="StreamlitでPygwalkerを使う", layout="wide")

# PyGWalkerとStreamlitの通信を確立する
init_streamlit_comm()

st.title("DuckDB+pygwalkerによるデータ分析基盤")

# DWHの作成(scikit-learn -> duckdb)
display_loadtime(st, "Irisデータをロード中...")
iris = load_iris()
iris_data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
iris_data["target"] = iris.target
iris_data.to_csv("csv/iris.csv", index=False)
if not os.path.isfile("duckdb/iris.duckdb"):
    create_duckdb("iris")

display_loadtime(st, "Wineデータをロード中...")
wine = load_wine()
wine_data = pd.DataFrame(data=wine.data, columns=wine.feature_names)
wine_data["target"] = wine.target
wine_data.to_csv("csv/wine.csv", index=False)
if not os.path.isfile("duckdb/wine.duckdb"):
    create_duckdb("wine")

# DMの作成(duckdb -> pandas)


# BI機能の作成(pandas -> pygwalker+streamlit)
components.html(get_pyg_html(wine_data), width=1300, height=1000, scrolling=True)
