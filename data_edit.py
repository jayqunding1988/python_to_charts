import streamlit as st
from main_app import read_excel
import pandas as pd


def editer_data():
    file_path = "./product data pf oem.xlsx"
    # df = read_excel(file_path, sheet_name="数据源", skiprows=1)
    df = pd.read_excel(file_path,sheet_name="demo")

    # print(df.dtypes)

    edit_df = st.data_editor(df,
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

    # favorite_command = edit_df.loc[edit_df["周"].idxmax()]["序号"]
    # st.markdown(f"Your favorite command is **{favorite_command}** 🎈")


editer_data()