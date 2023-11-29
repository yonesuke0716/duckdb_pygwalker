import duckdb
import time


# duckdbのDBを作成する関数
def create_duckdb(db_name):
    # DB の作成
    conn = duckdb.connect(f"duckdb/{db_name}.duckdb", read_only=False)
    c = conn.cursor()

    # CSV からデータをインポートしてテーブルを作成
    c.execute(f"CREATE TABLE wine AS SELECT * FROM read_csv_auto('csv/{db_name}.csv');")

    # DuckDBとの接続を閉じる
    c.close()


# 演出用のロード画面
def display_loadtime(st, text):
    my_bar = st.progress(0, text=text)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=text)
    my_bar.empty()
