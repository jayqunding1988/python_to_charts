"""质量分析主页面：批次合格率、异常问题走势、同型号不同供应商对比。"""
import datetime

import pandas as pd
import streamlit as st

from config import ADMIN_PSW, EXCEL_PATH, EXCEL_SHEET, GYS_CHOOSE_LIST, GYS_PSW, PROBLEM_CATEGORIES
from package_self import read_excel, show_table_to_web
from show_bar_line import draw_line, show_bar


def lots_data(get_data: pd.DataFrame, gys_choice: str, date_range):
    """按月统计 总批数/OK批数/NG批数/批次合格率。

    返回: (total_lots_list, OK_lots_list, NG_lots_list, percent_OK_list, date_select_list)
    """
    months = [f"{m}月" for m in range(date_range[0], date_range[1] + 1)]
    sub = get_data[get_data["月"].isin(months)]
    if gys_choice != "all":
        sub = sub[sub["供应商"] == gys_choice]

    # 一次 groupby 完成所有月份的统计，避免 N 次循环过滤
    grouped = sub.groupby("月")["判定"]
    ok_series = grouped.apply(lambda s: int((s == "OK").sum()))
    ng_series = grouped.apply(lambda s: int((s == "NG").sum()))

    total_list, ok_list, ng_list, pct_list, date_list = [], [], [], [], []
    for m in months:
        ok = int(ok_series.get(m, 0))
        ng = int(ng_series.get(m, 0))
        total = ok + ng
        pct = 0.0 if total == 0 else round(ok / total * 100, 2)
        total_list.append(total)
        ok_list.append(ok)
        ng_list.append(ng)
        pct_list.append(pct)
        date_list.append(m)
    return total_list, ok_list, ng_list, pct_list, date_list


def get_problem_data(data: pd.DataFrame, gys_choice: str):
    """统计每个月各问题分类的 NG 批数，返回 {分类: [12个月的值]}。"""
    months = [f"{m}月" for m in range(1, 13)]
    sub = data[(data["判定"].isin(["NG"]) | data["判定"].isnull()) & (data["问题归属"] == "NG批")]
    if gys_choice != "all":
        sub = sub[sub["供应商"] == gys_choice]

    # 一次 groupby 完成所有月份所有分类的统计
    pivot = sub.pivot_table(
        index="月", columns="问题分类", values="判定", aggfunc="count", fill_value=0
    )

    result = {cat: [] for cat in PROBLEM_CATEGORIES}
    for m in months:
        row = pivot.loc[m] if m in pivot.index else None
        for cat in PROBLEM_CATEGORIES:
            result[cat].append(int(row[cat]) if row is not None and cat in row.index else 0)
    return result


def date_selelcted():
    """月份范围滑块，返回 (start_month, end_month)。"""
    return st.slider(
        "2.请选择日期范围：(默认是当前月份)",
        1, 12, (1, datetime.datetime.now().month),
    )


def get_excel_data():
    """读取 Excel，缓存到 session_state 并返回。"""
    get_data = read_excel(EXCEL_PATH, sheet_name=EXCEL_SHEET)
    st.session_state.data = get_data
    return get_data


def same_product_dif_gys(get_data: pd.DataFrame, date_range):
    """展示相同型号产品在不同供应商之间的批次合格率走势。"""
    months = [f"{m}月" for m in range(date_range[0], date_range[1] + 1)]

    # 找出所有"同型号多供应商"的组合
    model_gys = (
        get_data.groupby("型号")["供应商"].apply(lambda s: list(set(s))).to_dict()
    )
    simple_model_gys = {m: gs for m, gs in model_gys.items() if len(gs) > 1}

    model_list, gys_list, show_linechart_in_row = [], [], []
    for xinghao, gys_s in simple_model_gys.items():
        for gys in gys_s:
            model_list.append(xinghao)
            gys_list.append(gys)

            sub = get_data[
                (get_data["型号"] == xinghao)
                & (get_data["供应商"] == gys)
                & (get_data["月"].isin(months))
            ]
            grouped = sub.groupby("月")["判定"]
            ok = grouped.apply(lambda s: int((s == "OK").sum()))
            ng = grouped.apply(lambda s: int((s == "NG").sum()))

            pchgl_list = []
            for m in months:
                o = int(ok.get(m, 0))
                n = int(ng.get(m, 0))
                pchgl_list.append(0 if (o + n) == 0 else o / (o + n))
            show_linechart_in_row.append(pchgl_list)

    st.checkbox("👈🏻_选择拉伸表查看", value=False, key="use_container_width")
    show_modle = {
        "model": model_list,
        "gys": gys_list,
        "chart": show_linechart_in_row,
    }
    st.dataframe(
        show_modle,
        column_config={
            "model": "👓产品型号",
            "gys": " 🚒供应商",
            "chart": st.column_config.LineChartColumn(
                label="🎢合格率对比走势", y_min=0, y_max=1
            ),
        },
        hide_index=True,
        use_container_width=st.session_state.use_container_width,
    )


def fun_run(gys_list, psw):
    """主流程：数据加载 + 批次合格率 + 异常问题走势 + 同型号对比。"""
    get_data = get_excel_data()

    st.markdown("##### 一、数据加载")
    with st.container():
        if len(gys_list) == 1:
            show_table_to_web(get_data[get_data["供应商"] == gys_list[0]])
        elif len(gys_list) > 1:
            show_table_to_web(get_data)

    st.markdown("##### 二、产品质量水平展示")
    gys_choice = st.selectbox("1.选择供应商", gys_list)
    date_range = date_selelcted()

    total_num, OK_num, NG_num, per_num, date_list = lots_data(
        get_data=get_data, gys_choice=gys_choice, date_range=date_range
    )
    with st.expander("图表展示:sunglasses:", expanded=True):
        with st.container():
            if gys_choice != "all":
                st.markdown("###### :one:批次合格率:")
            else:
                st.markdown("###### :one:外O整体批次合格率:")
            show_bar(total_num, OK_num, NG_num, per_num, date_list)
        st.write("<hr>", unsafe_allow_html=True)
        with st.container():
            date_list = [f"{i}月" for i in range(date_range[0], date_range[1] + 1)]
            dic_problem_data = get_problem_data(get_data, gys_choice)
            legend_label = PROBLEM_CATEGORIES
            if gys_choice != "all":
                st.markdown("###### :two:异常问题走势:")
            else:
                st.markdown("###### :two:外O整体异常问题:")
            draw_line(
                dic_problem_data["外观"], dic_problem_data["装配"],
                dic_problem_data["低错"], dic_problem_data["功能"],
                dic_problem_data["配件"], date_list, legend_label,
            )
        with st.container():
            st.markdown("###### :three:同型号不同供应商之间对比")
            if psw == ADMIN_PSW:
                same_product_dif_gys(get_data, date_range)


def info():
    """主页面：登录校验 + 路由到 fun_run。"""
    st.set_page_config(page_title="质量DPHU", page_icon=":bar_chart:")
    page_of_info = "<h1 style='text-align:center; color:#ff2288'>产品质量数据可视化</h1>"
    st.markdown(page_of_info, unsafe_allow_html=True)

    ep = st.empty()
    st.sidebar.markdown("## 请输入密码：")
    psw = st.sidebar.text_input("✍️🔢✅😀", type="password")
    st.session_state.psw = psw

    if st.session_state.psw in GYS_PSW.keys():
        st.sidebar.write(
            f"当前用户:<u>{GYS_PSW[st.session_state.psw]}</u>", unsafe_allow_html=True
        )
        gys_input = GYS_PSW[st.session_state.psw].split(",")
        fun_run(gys_input, st.session_state.psw)
    elif st.session_state.psw == ADMIN_PSW:
        fun_run(GYS_CHOOSE_LIST, st.session_state.psw)
    else:
        st.sidebar.warning("请输入正确密码。。。")
        ep.markdown(
            """
        <p style='color:#008888;font-size:26px;'>
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp这是一个数据可视化的App页面.<br>
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp主要展示目前OEM成品质量情况，多维度的展开和分析数据，从数据中得到关键因素，来提升产品的质量.<br><br>
        <strong>主要特点：</strong><br>
        <strong style='color:#8f3e6e;font-size:26px;'>数据可视化</strong>：
        提供多种可视化图表选项，包括柱状图、折线图、饼图、散点图等，用户可以选择合适的图表来展示数据.<br><br>
        <strong style='color:#8f3e6e;font-size:26px;'>实时数据更新</strong>：
        对于实时数据，用户可以设置自动更新频率，确保展示的数据始终保持最新状态.<br><br>
        <strong style='color:#8f3e6e;font-size:26px;'>导出图表和报告</strong>：
        用户可以导出生成的图表和分析报告，以便与团队或其他利益相关者共享.<br>
        </p>""",
            unsafe_allow_html=True,
        )
        st.stop()


if __name__ == "__main__":
    if "psw" not in st.session_state:
        st.session_state.psw = ""
    if "data" not in st.session_state:
        st.session_state.data = None
    info()
