"""数据编辑页面：基于 st.data_editor 提供 Excel 数据的在线编辑。"""
import streamlit as st
import pandas as pd

from config import EXCEL_PATH


def editer_data():
    df = pd.read_excel(EXCEL_PATH, sheet_name="demo")
    st.data_editor(
        df,
        column_config={
            "widgets": st.column_config.Column(
                "Streamlit Widgets",
                help="Streamlit **widget** commands 🎈",
                width="medium",
                required=True,
            )
        },
        hide_index=True,
        num_rows="dynamic",
    )


if __name__ == "__main__":
    editer_data()
