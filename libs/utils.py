import time


# 演出用のロード画面
def display_loadtime(st, text):
    my_bar = st.progress(0, text=text)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=text)
    my_bar.empty()
