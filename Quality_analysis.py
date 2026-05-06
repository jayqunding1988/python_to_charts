import streamlit as st
import datetime
from show_bar_line import show_bar, draw_line
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
    if gys_choice != "all":
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
    else:
        
        for date in range(date_range[0],date_range[1]+1):
            lots_value = get_data[get_data["月"]==f"{date}月"]["判定"]
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
    if "data" not in get_data:
        st.session_state.data = None
    st.session_state.data = get_data
    
    return get_data


def get_problem_data(data,gys_choice):
    """
    主要功能实现从读取excel数据中筛选出问题点进行归类和图表输出。\n
    data:读取excel返回的值。\n
    date_range:日期范围.\n
    gys_choice:选择供应商。\n
    return:返回一个字典
    """
    PROBLEMS_DESCRIBE = ["外观","装配","低错","功能","配件"]
    dict_problem_data = {
        # "months":[f"{i}月" for i in range(1,13)],
        # "months":date_range,
        "外观":[],
        "装配":[],
        "低错":[],
        "功能":[],
        "配件":[]
    }
    if gys_choice != "all":
        for i in range(1,13):
            filtered_data = data[((((data["判定"]=="NG")|(data["判定"].isnull())) & (data["问题归属"]=="NG批")) & (data["月"]==f"{i}月")) & (data["供应商"]==gys_choice)]

            problem_counts = filtered_data["问题分类"].value_counts()

            #获取筛选出来的问题描述
            get_problems = [i for i in problem_counts.keys()]

            for problem in PROBLEMS_DESCRIBE:
                if problem in get_problems:
                    dict_problem_data[problem].append(int(problem_counts[problem]))
                else:
                    dict_problem_data[problem].append(0)
    else:

        for i in range(1,13):
            filtered_data = data[((((data["判定"]=="NG")|(data["判定"].isnull())) & (data["问题归属"]=="NG批")) & (data["月"]==f"{i}月"))]

            problem_counts = filtered_data["问题分类"].value_counts()

            #获取筛选出来的问题描述
            get_problems = [i for i in problem_counts.keys()]

            for problem in PROBLEMS_DESCRIBE:
                if problem in get_problems:
                    dict_problem_data[problem].append(int(problem_counts[problem]))
                else:
                    dict_problem_data[problem].append(0)

    return dict_problem_data


def date_selelcted():
    """
    主要功能：通过滑动来选择相应的月份。\n
    return: 返回的是一个元祖(0,9)
    """
    date_range = st.slider("2.请选择日期范围：(默认是当前月份)",1,12,(1,datetime.datetime.now().month))
    return date_range



def same_product_dif_gys(get_data,date_range):
    """
    主要功能：展示出相同型号产品，不同供应商之间的质量水平差\n
    get_data: 通过read_excel函数读取的数据\n
    args:其他参数
    """
    # 创建临时存储数据的字典
    # 第1个是存储:单个型号--->多个供应商列表；
    many_models_gys = dict()
    # 第2个是存储：单个型号----> 两个供应商数量的列表
    simple_model_gys = dict()
    # 第3个：型号列表，为后面使用st.dataframe(df)方法显示图表准备
    model_list = list()
    # 第4个：供应商列表，为后面使用st.dataframe(df)方法显示图表准备
    gys_list = list()
    # 第5个：是展示 Linechart图表的源数据。
    show_linechart_in_row = list()

    # 从get_data数据中筛选出型号，并将型号去重，以及转化成列表
    get_model = get_data["型号"]
    get_single_model_list = list(set(get_model))

    # 遍历 get_single_model_list ,并通过筛选型号==型号元素，将对应型号所有的的供应商筛选出来（一个列表），并用：
    # set()方法，将列表去重，并再转化成列表，最后装进 many_models_gys字典里 
    for model in get_single_model_list:
        get_gys_list = get_data[get_data["型号"]==model]["供应商"]
        many_models_gys[model] = list(set(get_gys_list))

    # 通过再遍历 many_models_gys字典，将keys和values拆成单个的列表，分别装进model_list和gys_list:
    for key, value in many_models_gys.items():
        # 判断 value的数据长度是否>1
        if len(value) > 1:
            simple_model_gys[key] = value
            model_list.append(key)
            model_list.append(key)
            # 下面是通过value的长度进行遍历，并通过下标把value的元素添加到gys_list列表中。
            for index in range(len(value)):
                gys_list.append(value[index])

    
    # 对重复gys的字典进行遍历，取出每个gys下该相同型号的 月度批次合格率

    for xinghao, gys_s in simple_model_gys.items():
        for gys in gys_s:
            # 一个临时存储的列表
            tecent_ = list()
            for date in range(date_range[0],date_range[1]+1):
                OK_NG_data = get_data[((get_data["型号"] == xinghao) & (get_data["供应商"] == gys)) &
                                      (get_data["月"] == f"{date}月")]

                # print(OK_count, NG_count)
                OK_count = OK_NG_data["判定"][OK_NG_data["判定"] == "OK"].count()
                NG_count = OK_NG_data["判定"][OK_NG_data["判定"] == "NG"].count()
                # print(f"{xinghao}，供应商为{gys},{date}月分的,OK lots为 {OK_count}")
                # print(f"{xinghao}，供应商为{gys},{date}月分的,OK lots为 {NG_count}")
                # print(f"{xinghao}，供应商为{gys},{date}月分的,批次合格率为 {(OK_count)/(NG_count+OK_count)}")

                if OK_count + NG_count == 0:
                    # print(f"{xinghao}，供应商为{gys},{date}月分的,批次合格率为{0}")
                    pchgl = 0
                    tecent_.append(pchgl)
                else:
                    # print(f"{xinghao}，供应商为{gys},{date}月分的,批次合格率为 {(OK_count)/(NG_count+OK_count)}")
                    pchgl = (OK_count) / (NG_count + OK_count)
                    tecent_.append(pchgl)
            show_linechart_in_row.append(tecent_)
    
    st.checkbox("👈🏻_选择拉伸表查看", value=False,key="use_container_width")
    # 展示数据的格式
    show_modle = {
        "model": model_list,
        "gys": gys_list,
        # "chart": [[random.randint(0, 5000) for _ in range(30)] for _ in range(len(gys_list))]
        "chart": show_linechart_in_row
    }
    
    # 展示数据：
    st.dataframe(show_modle,
                 column_config={
                     "model":"👓产品型号",
                     "gys":" 🚒供应商",
                     "chart":st.column_config.LineChartColumn(
                        label="🎢合格率对比走势",y_min=0,y_max=1
                     )
                 },
                 hide_index=True,
                 use_container_width=st.session_state.use_container_width
                 )




def fun_run(gys_list,psw):
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

        elif len(gys_list) > 1:
            show_table_to_web(get_data)

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

    
    # 3、展示供应商合格率走势。
    st.markdown("##### 二、产品质量水平展示")
    # 创建一个下拉列表：
    # gys_choice = st.selectbox("1.选择供应商",["lifeng","zhaochi","manshen","fanghui","yinghua"])

    gys_choice = st.selectbox("1.选择供应商",gys_list)

    # 创建月份范围选框
    # date_range = st.slider("2.请选择日期范围：(默认是当前月份)",1,12,(1,datetime.datetime.now().month))
    date_range = date_selelcted()

    # min_value, max_value = date_range[0],date_range[1]


    total_num,OK_num,NG_num,per_num,date_list = lots_data(get_data=get_data,gys_choice=gys_choice,date_range=date_range)
    with st.expander("图表展示:sunglasses:",expanded=True):
        with st.container():
            # 显示柱状图和折线图的组合图
            if gys_choice != "all":
                st.markdown("###### :one:批次合格率:")
            else:
                st.markdown("###### :one:外O整体批次合格率:")
            show_bar(total_num,OK_num,NG_num,per_num,date_list)
        st.write("<hr>",unsafe_allow_html=True)
        with st.container():
            date_list = [f"{i}月" for i in range(date_range[0],(date_range[1]+1))]
            dic_problem_data = get_problem_data(get_data,gys_choice)
            legend_label = ["外观","装配","低错","功能","配件"]
            if gys_choice != "all":
                st.markdown("###### :two:异常问题走势:")
            else:
                st.markdown("###### :two:外O整体异常问题:")
            draw_line(dic_problem_data["外观"],dic_problem_data["装配"],dic_problem_data["低错"],
                      dic_problem_data["功能"],dic_problem_data["配件"],date_list,legend_label)
        with st.container():
            st.markdown("###### :three:同型号不同供应商之间对比")
            if psw == "DSM":
                same_product_dif_gys(get_data,date_range)
    


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
    GYS_CHOOSE_LIST = ["介宏","方汇","樱花","荣硕","协创","all"]


    # 建立供应商密码：键值对
    GYS_PSW = {
        "lf_06w":"介宏",
        "msh_07x":"曼申",
        "fh_07s":"方汇",
        "yh_07g":"樱花",
        # "oms_07n":"欧迈斯",
        "xc_09h":"协创",
        "rs_08":"荣硕"
    }


    # 创建判断后存储输入供应商名称的列表
    # size_up = list()
    
    
    ep = st.empty()
    # 用户输入验证信息后再继续跳转
    st.sidebar.markdown("## 请输入密码：")
    psw = st.sidebar.text_input("✍️🔢✅😀",type="password")
   
    st.session_state.psw = psw
    # if psw in GYS_CHOOSE_LIST:
    if st.session_state.psw in GYS_PSW.keys():
        # st.sidebar.write(f"当前用户:<u>{psw}</u>",unsafe_allow_html=True)
        st.sidebar.write(f"当前用户:<u>{GYS_PSW[st.session_state.psw]}</u>",unsafe_allow_html=True)
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
        # gys_input = psw.split(",")
        # fun_run(gys_input,psw)
        # gys_input = psw.split(",")
        gys_input = GYS_PSW[st.session_state.psw].split(",")
        # fun_run(gys_input,st.session_state.psw)
        fun_run(gys_input,st.session_state.psw)
        # else:
        #     st.sidebar.warning("请输入正确的供应商名称")
    # elif psw == "DSM":
    elif st.session_state.psw == "DSM":

        fun_run(GYS_CHOOSE_LIST,st.session_state.psw)

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
    if "psw" not in st.session_state:
        st.session_state.pwd = ""
    if "data" not in st.session_state:
        st.session_state.data = None
    info()
