def create_table(conn, table_name, df):
    # 既存のテーブルがあれば削除
    conn.execute(f"DROP TABLE IF EXISTS {table_name}")

    # データフレームをDuckDBのテーブルに変換
    df.to_sql(table_name, conn, if_exists="replace", index=False)

    select_query = f"SELECT * FROM {table_name}"
    conn.execute(select_query).fetchall()
