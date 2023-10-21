import streamlit as st
from Quality_analysis import date_selelcted
from package_self import read_excel
# from streamlit_echarts import st_echarts
from show_bar_line import plot_line_chart
import time


# 读取excel数据
def get_excel_data():
    """return: 返回读取excel的数据"""
    # data_path = "./product_data_of_oem.xlsx"

    # get_data = read_excel(data_path,sheet_name="数据源")
    # st.session_state.data = get_data

    # 读取session_state中的缓存数据
    get_data = st.session_state.data
    return get_data

# 以上返回 get_data是从excel表中读取的数据，表头主要有1-12月份的日期，供应商名称，型号，判定，streamlit制作供应商选择，产品型号选择，并展示出各型号每个月的批次合格率。
def show_diffrent_product_type(get_data,supplier):
    

    # 获取选择的供应商下所有型号
    product_type = get_data[get_data["供应商"] == supplier]["型号"].unique()    # 返回的是一个列表

    # 获取日期：
    date_turple = date_selelcted()
    date_list = [f"{dt}月" for dt in range(date_turple[0], date_turple[1]+1)]
    # print(date_list)

  
    all_products_data = []  # 在类别中添加字典
    # all_products_data = {}
    column_names = []   

    # 相应供应商下每个型号，在date_list下批次合格率数据
    # """
    # 1.定义5个列表，用于存储选定日期内的每个月总批数、OK批数、NG批数、批次合格率
    # 2.返回:\n
    # total_lots_list: 总批数;\n
    # OK_lots_list: OK批数;\n
    # NG_lots_list: NG批数;\n
    # percent_OK_list: 批次合格率;\n
    # date_select_list: 选择的日期范围.
    # """
    # total_lots_list = list()
    # OK_lots_list = list()
    # NG_lots_list = list()
    # percent_OK_list = list()
    date_select_list = list()

    for product in product_type:
        percent_OK_list = list()
        for date in date_list:
            lots_value = get_data[get_data["月"]==date][get_data["供应商"]==supplier][get_data["型号"]==product]["判定"]
            OK_lots = int((lots_value[get_data["判定"]=="OK"]).count())
            NG_lots = int((lots_value[get_data["判定"]=="NG"]).count())
            total_lots = OK_lots + NG_lots
            if total_lots == 0:
                percent_OK = 0
            else:
                percent_OK = float(round((float(round(OK_lots/total_lots,5)))*100,2))
            # total_lots_list.append(total_lots)
            # OK_lots_list.append(OK_lots)
            # NG_lots_list.append(NG_lots)
            percent_OK_list.append(percent_OK)
            date_select_list.append(f"{date}月")
            # total_lots：总批数
            # OK_lots：合格批数
            # NG_lots：不合格批数
            # percent_OK：批次合格率
        # print(product,"型号的批次合格率:" ,percent_OK_list)
        # all_products_data.append([f"{product}", percent_OK_list])
        all_products_data.append({
             "name": f"{product}",
             "type": "line",
             "emphasis": {"focus": 'series'},
             "data": percent_OK_list,
             "label":{
            "show":True,
            "textStyle":{
                "color":"#bb33f6",
                "fontsize":14
            }
        }
         })
        column_names.append(product)

    # print(all_products_data)
    return all_products_data,column_names,date_list,supplier

    
    



    # 根据选择的供应商，获取该供应商下所有型号的批次合格率  



if __name__ == "__main__":

    page_of_info = """
	<h2 style='text-align:center; color:#ff8888'>产品型号数据展示</h2>

	"""
    st.markdown(page_of_info, unsafe_allow_html=True)
    ep = st.empty()
   
    fetch_data = get_excel_data()
    # 读取唯一供应商，返回列表
    supplier_list = fetch_data["供应商"].unique()

    # st.sidebar.markdown("## 请输入密码：")
    # psw = st.sidebar.text_input("✍️🔢✅😀",type="password")
    psw = st.session_state.psw

    if psw in supplier_list:

        # 展示供应商的选择
        # supplier = st.selectbox("请选择供应商：", ["".join(psw)])
        supplier = psw

        all_products_data,column_names,date_list,supplier = show_diffrent_product_type(fetch_data,supplier)
        st.sidebar.write(f"当前用户:<u>{psw}</u>",unsafe_allow_html=True)
        
        st.info(f"{supplier} 供应商生产  {len(column_names)}  种型号， 如下：",)
        
        if st.button("show name："):
            # for name in column_names:
            #     st.toast(name)
            #     time.sleep(0.5)
            st.success(column_names)

        # st.table(column_names)
        
        plot_line_chart(all_products_data,column_names,date_list)
        
    elif psw == "DSM":
        supplier = st.selectbox("请选择供应商：", supplier_list)
        all_products_data,column_names,date_list,supplier = show_diffrent_product_type(fetch_data,supplier)
        st.sidebar.write(f"当前用户:<u>{psw}</u>",unsafe_allow_html=True)
        

        st.info(f"{supplier} 供应商生产{len(column_names)}种型号 如下点击按钮：",)

        if st.button("查看型号：",help="请点击按钮查看型号"):
            for name in column_names:
                st.toast(name)
                time.sleep(0.5)
        
        plot_line_chart(all_products_data,column_names,date_list)
    else:
        # st.sidebar.warning("请输入正确密码。。。")
        ep.markdown(
            """
        <p style='color:#008888;font-size:26px;'>
	    &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp这是一个数据可视化的App页面.<br>
		&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp主要各每个型号产品合格率,多维度的展开和分析数据。<br><br>
		<strong>主要内容：</strong><br>
        <strong style='color:#8f3e6e;font-size:26px;'>综合显示</strong>：
        所有生产型号的月度推移，折线图灵活选择并显示数据。<br><br>
        <strong style='color:#8f3e6e;font-size:26px;'>选择节点数据</strong>： 
        数据交互选择。<br><br>
        <strong style='color:#8f3e6e;font-size:26px;'>导出图表和报告</strong>： 
        用户可以导出生成的图表和分析报告，以便与团队或其他利益相关者共享。<br>
		</p>""",unsafe_allow_html=True
        )