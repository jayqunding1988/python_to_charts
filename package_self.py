import pandas as pd
import streamlit as st
import datetime
# import os
import base64
"""
read_excel
date_selected
"""

@st.cache_data
def read_excel(file_path,sheet_name):
    # 读取Excel文件中的数据
    """参数:file_path.\n
    读取指定路径下的文件"""
    return pd.read_excel(file_path, sheet_name=sheet_name, skiprows=1)



# 日期选择函数
def date_selected():
    today = datetime.datetime.now()
    this_year = today.year
    jan_1 = datetime.date(this_year,1,1)
    dec_31 = datetime.date(this_year,12,31)
    date_value = st.date_input(
        "请选择日期：",
        (jan_1,datetime.date(this_year,today.month,7)),
        jan_1,
        dec_31,
        format="YYYY/MM/DD"
    )
    return date_value


def show_table_to_web(data):
    """将从Excel读取的数据加载到内存并展示到web页面上,并提供下载的连接"""
    # 获取下载文件夹的路径,
    # downloads = os.path.join(os.path.expanduser("~"),'Downloads')
    with st.status("数据加载",state="running") as status:
        st.dataframe(data=data, use_container_width=True)
        status.update(label="加载完成", state = "complete")
    cl1,cl2 = st.columns(2)
    with st.container():
            
        if cl1.button("重新加载",help="清楚缓存，重新读取和载入"):
            st.cache_data.clear()
        # if cl2.button("导出Excel",help=f"导出Excel文件到{downloads}"):
        #     data.to_excel(downloads+"/new_data.xlsx",index=False)
        # 添加下载的连接格式是csv
        to_csv = data.to_csv(index=False)
        b64 = base64.b64encode(to_csv.encode()).decode()
        href = f'<a href="data:file/to_csv;base64,{b64}" download="data_table.csv">点击此处下载 CSV 文件</a>'
        cl2.markdown(href,unsafe_allow_html=True)

    # with st.spinner("正在加载，请稍后。。。"):
    #     st.dataframe(data=data, use_container_width=True)
    # st.success("加载完成")
