import streamlit as st
import pandas as pd
import datetime
from show_bar_line import show_bar




# @st.cache_data
# 读取Excel文件中的数据
def read_excel(file_path):
    """参数:file_path.\n
    读取指定路径下的文件"""
    return pd.read_excel(file_path, sheet_name="数据源", skiprows=1)



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

# 计算 总批数	OK批数	NG批数	批次合格率
def lots_data(get_data,gys_choice,date_range):
    """
    1.定义5个列表，用于存储选定日期内的每个月总批数、OK批数、NG批数、批次合格率
    2.返回 总批数、OK批数、NG批数、批次合格率、选择的日期范围
    """
    OK_lots_list = list()
    NG_lots_list = list()
    total_lots_list = list()
    percent_OK_list = list()
    date_select_list = list()
    for date in range(date_range[0],date_range[1]+1):
        lots_value = get_data[get_data["月"]==f"{date}月"][get_data["供应商"]==gys_choice]["判定"]
        OK_lots = int((lots_value[get_data["判定"]=="OK"]).count())
        NG_lots = int((lots_value[get_data["判定"]=="NG"]).count())
        total_lots = OK_lots + NG_lots
        if total_lots == 0:
            percent_OK = 0
        else:
            percent_OK = float(round((float(round(OK_lots/total_lots,5)))*100,2))
        total_lots_list.append(total_lots)
        OK_lots_list.append(OK_lots)
        NG_lots_list.append(NG_lots)
        percent_OK_list.append(percent_OK)
        date_select_list.append(f"{date}月")
        # total_lots：总批数
        # OK_lots：合格批数
        # NG_lots：不合格批数
        # percent_OK：批次合格率
    
    return total_lots_list,OK_lots_list,NG_lots_list,percent_OK_list,date_select_list



def show_table_to_web(data):
    """将从Excel读取的数据加载到内存并展示到web页面上"""
    with st.status("数据加载",state="running"):
        st.dataframe(data=data, use_container_width=True)



def fun_run():
    # 数据路径
    data_path = "./外O成品数据.xlsx"
    # 1、获取数据
    get_data = read_excel(data_path)

    # 2、显示在页面
    st.markdown("##### 一、数据加载")
    with st.container():
        show_table_to_web(get_data)
    
    # 3、展示供应商合格率走势。
    st.markdown("##### 二、展示各供应商产品质量水平")
    # 创建一个下拉列表：
    gys_choice = st.selectbox("1.选择供应商",["砺峰","兆驰","曼申","方汇","樱花"])
    # 创建月份范围选框
    date_range = st.slider("2.请选择日期范围：(默认是当前月份)",1,12,(1,datetime.datetime.now().month))
    # min_value, max_value = date_range[0],date_range[1]
    total_num,OK_num,NG_num,per_num,date_list = lots_data(get_data=get_data,gys_choice=gys_choice,date_range=date_range)
    with st.expander("图表展示::"):
        with st.container():
            # 显示柱状图和折线图的组合图
            show_bar(total_num,OK_num,NG_num,per_num,date_list)





if __name__ == "__main__":
    fun_run()