import streamlit as st
import datetime
from show_bar_line import show_bar
from package_self import read_excel, show_table_to_web

# 计算 总批数	OK批数	NG批数	批次合格率
def lots_data(get_data,gys_choice,date_range):
    """
    1.定义5个列表，用于存储选定日期内的每个月总批数、OK批数、NG批数、批次合格率
    2.返回:\n
    total_lots_list: 总批数;\n
    OK_lots_list: OK批数;\n
    NG_lots_list: NG批数;\n
    percent_OK_list: 批次合格率;\n
    date_select_list: 选择的日期范围.
    """
    total_lots_list = list()
    OK_lots_list = list()
    NG_lots_list = list()
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



# def show_table_to_web(data):
#     """将从Excel读取的数据加载到内存并展示到web页面上"""
#     with st.status("数据加载",state="running") as status:
#         st.dataframe(data=data, use_container_width=True)
#         status.update(label="加载完成", state = "complete")
#     if st.button("重新加载"):
#         st.cache_data.clear()

    # with st.spinner("正在加载，请稍后。。。"):
    #     st.dataframe(data=data, use_container_width=True)
    # st.success("加载完成")
    
# 读取excel数据
def get_excel_data():
    """return: 返回读取excel的数据"""
    data_path = "./product_data_of_oem.xlsx"

    get_data = read_excel(data_path,sheet_name="数据源")
    return get_data



def fun_run(gys_list):
    """
    gys_list: 用户输入的供应商名称列表
    """
    get_data = get_excel_data()

    # 2、显示在页面
    # ["lifeng","zhaochi","manshen","fanghui","yinghua"]
    st.markdown("##### 一、数据加载")
    with st.container():
        if len(gys_list) ==1:
            show_table_to_web(get_data[get_data["供应商"]==gys_list[0]])

        # elif len(gys_list) == 2:
        #     show_table_to_web(get_data[(get_data["供应商"]==gys_list[0]) | (get_data["供应商"]==gys_list[1])])
        # elif len(gys_list) == 3:
        #     show_table_to_web(get_data[(get_data["供应商"]==gys_list[0]) | (get_data["供应商"]==gys_list[1]) |
        #                                (get_data["供应商"]==gys_list[2])])
        # elif len(gys_list) == 4:
        #     show_table_to_web(get_data[(get_data["供应商"]==gys_list[0]) | (get_data["供应商"]==gys_list[1]) |
        #                                (get_data["供应商"]==gys_list[2]) |(get_data["供应商"]==gys_list[3])])
        # elif len(gys_list) == 5:
        #     show_table_to_web(get_data[(get_data["供应商"]==gys_list[0]) | (get_data["供应商"]==gys_list[1]) |
        #                                (get_data["供应商"]==gys_list[2]) |(get_data["供应商"]==gys_list[3]) |
        #                                (get_data["供应商"]==gys_list[4])])
        elif len(gys_list) > 1:
            show_table_to_web(get_data)

    
    # 3、展示供应商合格率走势。
    st.markdown("##### 二、产品质量水平展示")
    # 创建一个下拉列表：
    # gys_choice = st.selectbox("1.选择供应商",["lifeng","zhaochi","manshen","fanghui","yinghua"])

    gys_choice = st.selectbox("1.选择供应商",gys_list)
    # 创建月份范围选框
    date_range = st.slider("2.请选择日期范围：(默认是当前月份)",1,12,(1,datetime.datetime.now().month))
    # min_value, max_value = date_range[0],date_range[1]
    total_num,OK_num,NG_num,per_num,date_list = lots_data(get_data=get_data,gys_choice=gys_choice,date_range=date_range)
    with st.expander("图表展示::"):
        with st.container():
            # 显示柱状图和折线图的组合图
            show_bar(total_num,OK_num,NG_num,per_num,date_list)


def info():
    """
    展示本页面的说明,\n
    并设置用户使用的密码。
    """
    st.set_page_config(page_title="质量DPHU",page_icon=":bar_chart:")
    
    page_of_info = """
	<h1 style='text-align:center; color:#ff2288'>产品质量数据可视化</h1>

	"""
    st.markdown(page_of_info, unsafe_allow_html=True)

    # 指定供应商名称范围
    GYS_CHOOSE_LIST = ["lifeng","zhaochi","manshen","fanghui","yinghua"]

    # 创建判断后存储输入供应商名称的列表
    # size_up = list()


    ep = st.empty()
    # 用户输入验证信息后再继续跳转
    st.sidebar.markdown("## 请输入密码：")
    psw = st.sidebar.text_input("请输入6位数的密码",type="password")
    if psw in GYS_CHOOSE_LIST:
        st.sidebar.write(f"当前用户:<u>{psw}</u>",unsafe_allow_html=True)
        # # 用户输入供应商的名称
        # gys = st.sidebar.text_input("请输入供应商:point_right:",help="如果一次性输入多个供应商，请用逗号‘,’隔开：")
        # # 将供应商名称以逗号隔开并形成列表
        # gys_to_list = gys.split(",")
        # # 循环遍历gys_to_list,取出每个元素 和制定供应商名称列表元素对比，如果在列表中，就添加到 size_up 列表中
        # for i in gys_to_list:
        #     if i in GYS_CHOOSE_LIST:
        #         size_up.append(i)
        # # 根据判断后size_up列表和初始输入列表的长度对比，确认是否存在输入信息错误情况
        # if len(size_up) == len(gys_to_list):
        #     fun_run(gys_to_list)
        gys_input = psw.split(",")
        fun_run(gys_input)
        # else:
        #     st.sidebar.warning("请输入正确的供应商名称")
    elif psw == "DSM":
        fun_run(GYS_CHOOSE_LIST)
    else:
        st.sidebar.warning("请输入正确密码。。。")
        ep.markdown(
            """
        <p style='color:#008888;font-size:26px;'>
	    &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp这是一个数据可视化的App页面.<br>
		&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp主要展示目前OEM成品质量情况，多维度的展开和分析数据，从数据中得到关键因素，来提升产品的质量。<br><br>
		<strong>主要特点：</strong><br>
        <strong style='color:#8f3e6e;font-size:26px;'>数据可视化</strong>：
        提供多种可视化图表选项，包括柱状图、折线图、饼图、散点图等，用户可以选择合适的图表来展示数据。<br><br>
        <strong style='color:#8f3e6e;font-size:26px;'>实时数据更新</strong>： 
        对于实时数据，用户可以设置自动更新频率，确保展示的数据始终保持最新状态。<br><br>
        <strong style='color:#8f3e6e;font-size:26px;'>导出图表和报告</strong>： 
        用户可以导出生成的图表和分析报告，以便与团队或其他利益相关者共享。<br>
		</p>"""
        ,unsafe_allow_html=True)
        st.stop()



if __name__ == "__main__":
    info()