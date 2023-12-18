import os
import pandas as pd

from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html
import streamlit as st
import streamlit.components.v1 as components
import duckdb

# 時間計測開始
import time


@st.cache_resource
def get_pyg_html(df: pd.DataFrame) -> str:
    html = get_streamlit_html(df, use_kernel_calc=True, debug=False)
    return html


# Streamlitページの幅を調整する
st.set_page_config(page_title="AdventCalender2023_Aidemy_yonekura", layout="wide")

# PyGWalkerとStreamlitの通信を確立する
init_streamlit_comm()

st.title("DuckDB+pygwalkerで、データ分析基盤作ってみた")

# 計測開始(duckdb)
start = time.time()

read_df = duckdb.read_csv("csv/diabetes_data.csv")

# BI機能の作成(duckdb -> pygwalker)
components.html(get_pyg_html(read_df), width=1300, height=1000, scrolling=True)

# 時間計測終了
elapsed_time = time.time() - start
# 時間を小数点以下2桁まで表示する
elapsed_time = round(elapsed_time, 3)
st.write(f"elapsed_time: {elapsed_time} [sec]")
