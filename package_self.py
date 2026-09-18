"""数据读取与基础 Streamlit 组件封装。"""
import base64
import datetime

import pandas as pd
import streamlit as st

from config import EXCEL_PATH, EXCEL_SHEET


@st.cache_data
def read_excel(file_path: str = EXCEL_PATH, sheet_name: str = EXCEL_SHEET) -> pd.DataFrame:
    """读取指定路径下的 Excel 文件，跳过首行表头。"""
    return pd.read_excel(file_path, sheet_name=sheet_name, skiprows=1)


def date_selected():
    """日期范围选择器（按天）。"""
    today = datetime.datetime.now()
    this_year = today.year
    jan_1 = datetime.date(this_year, 1, 1)
    dec_31 = datetime.date(this_year, 12, 31)
    date_value = st.date_input(
        "请选择日期：",
        (jan_1, datetime.date(this_year, today.month, 7)),
        jan_1,
        dec_31,
        format="YYYY/MM/DD",
    )
    return date_value


def show_table_to_web(data: pd.DataFrame):
    """将 DataFrame 展示到页面，并提供 CSV 下载链接与缓存清理按钮。"""
    with st.status("数据加载", state="running") as status:
        st.dataframe(data=data, use_container_width=True)
        status.update(label="加载完成", state="complete")

    cl1, cl2 = st.columns(2)
    with st.container():
        if cl1.button("重新加载", help="清除缓存，重新读取和载入"):
            st.cache_data.clear()
        # 提供 CSV 下载链接
        to_csv = data.to_csv(index=False)
        b64 = base64.b64encode(to_csv.encode()).decode()
        href = f'<a href="data:file/to_csv;base64,{b64}" download="data_table.csv">点击此处下载 CSV 文件</a>'
        cl2.markdown(href, unsafe_allow_html=True)
