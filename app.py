import os
import pandas as pd
from sklearn.datasets import load_iris, load_wine

from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html
import streamlit as st
import streamlit.components.v1 as components
import duckdb

from libs.utils import display_loadtime
from libs.sql import create_table

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
st.set_page_config(page_title="AdventCalender2023_Aidemy_yonekura", layout="wide")

# PyGWalkerとStreamlitの通信を確立する
init_streamlit_comm()

st.title("DuckDB+pygwalkerで、データ分析基盤作ってみた")

con = duckdb.connect()

# DWHの作成(scikit-learn -> duckdb)
# irisデータをロード
# display_loadtime(st, "Irisデータをロード中...")
iris = load_iris()
iris_data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
iris_data["target"] = iris.target
# テーブルの作成
# create_table(conn, "iris", iris_data)
duckdb.sql("SELECT * FROM iris_data")

# wineデータをロード
# display_loadtime(st, "Wineデータをロード中...")
wine = load_wine()
wine_data = pd.DataFrame(data=wine.data, columns=wine.feature_names)
wine_data["target"] = wine.target
# テーブルの作成
# create_table(conn, "wine", wine_data)
duckdb.sql("SELECT * FROM wine_data")

# DMの作成(duckdb -> pandas)
table_name = st.selectbox("テーブルを選択してください", ["iris", "wine"])
# テーブルの読み込み
read_df = con.execute(f"SELECT * FROM {table_name}_data").fetchdf()
st.header(table_name)

# BI機能の作成(pandas -> pygwalker)
components.html(get_pyg_html(read_df), width=1300, height=1000, scrolling=True)
