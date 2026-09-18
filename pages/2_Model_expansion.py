"""产品型号数据展示页：按供应商展示各型号的月度批次合格率折线图。"""
import time

import streamlit as st

from Quality_analysis import date_selelcted
from show_bar_line import draw_plot_line_chart

# 复用主页面统一的密码字典
from config import GYS_PSW, ADMIN_PSW


def get_excel_data():
    """读取缓存在 session_state 中的数据。"""
    return st.session_state.data


def show_diffrent_product_type(get_data, supplier):
    """计算指定供应商下每个型号在选定月份范围内的批次合格率。

    返回: (series_list, column_names, date_list, supplier)
    """
    product_type = get_data[get_data["供应商"] == supplier]["型号"].unique()

    date_turple = date_selelcted()
    months = [f"{dt}月" for dt in range(date_turple[0], date_turple[1] + 1)]

    # 一次性过滤出该供应商在选定月份内的所有记录
    sub = get_data[
        (get_data["供应商"] == supplier) & (get_data["月"].isin(months))
    ]

    all_products_data = []
    column_names = []

    for product in product_type:
        prod_sub = sub[sub["型号"] == product]
        grouped = prod_sub.groupby("月")["判定"]
        ok = grouped.apply(lambda s: int((s == "OK").sum()))
        ng = grouped.apply(lambda s: int((s == "NG").sum()))

        percent_OK_list = []
        for m in months:
            o = int(ok.get(m, 0))
            n = int(ng.get(m, 0))
            total = o + n
            percent_OK_list.append(0 if total == 0 else round(o / total * 100, 2))

        all_products_data.append({
            "name": f"{product}",
            "type": "line",
            "emphasis": {"focus": 'series'},
            "data": percent_OK_list,
            "label": {
                "show": True,
                "textStyle": {"color": "#bb33f6", "fontSize": 14},
            },
        })
        column_names.append(product)

    return all_products_data, column_names, months, supplier


def main():
    page_of_info = "<h2 style='text-align:center; color:#ff8888'>产品型号数据展示</h2>"
    st.markdown(page_of_info, unsafe_allow_html=True)
    ep = st.empty()

    fetch_data = get_excel_data()
    psw = st.session_state.get("psw", "")

    if fetch_data is None or psw == "":
        st.warning("请先于 Quality analysis 页面登录")
        return

    supplier_list = fetch_data["供应商"].unique()

    if psw == ADMIN_PSW:
        supplier = st.selectbox("请选择供应商：", supplier_list)
        all_products_data, column_names, date_list, supplier = show_diffrent_product_type(
            fetch_data, supplier
        )
        st.sidebar.write(f"当前用户:<u>{psw}</u>", unsafe_allow_html=True)
        st.info(f"{supplier} 供应商生产 {len(column_names)} 种型号，如下点击按钮：")
        if st.button("查看型号：", help="请点击按钮查看型号"):
            for name in column_names:
                st.toast(name)
                time.sleep(0.5)
        draw_plot_line_chart(all_products_data, column_names, date_list)
    elif psw in GYS_PSW and GYS_PSW[psw] in supplier_list:
        supplier = GYS_PSW[psw]
        all_products_data, column_names, date_list, supplier = show_diffrent_product_type(
            fetch_data, supplier
        )
        st.sidebar.write(f"当前用户:<u>{supplier}</u>", unsafe_allow_html=True)
        st.info(f"{supplier} 供应商生产 {len(column_names)} 种型号，如下：")
        if st.button("show name："):
            st.success(column_names)
        draw_plot_line_chart(all_products_data, column_names, date_list)
    else:
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
        </p>""",
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
