"""ECharts 图表配置与渲染。"""
from typing import Iterable, List

from streamlit_echarts import st_echarts

COLORS = ['#5470C6', '#91CC75', '#EE6666', 'green', 'lightblue']
LABEL_STYLE = {"show": True, "textStyle": {"color": "#bb33f6", "fontSize": 14}}


def _base_option(date_list: Iterable[str], legend_data: List[str]) -> dict:
    """生成 ECharts 通用配置（tooltip / toolbox / legend / xAxis）。"""
    return {
        "color": COLORS,
        "tooltip": {"trigger": 'axis', "axisPointer": {"type": 'cross'}},
        "grid": {"right": '5%'},
        "toolbox": {
            "feature": {
                "dataView": {"show": True, "readOnly": True},
                "magicType": {"type": ['line', 'bar']},
                "restore": {"show": True},
                "saveAsImage": {"show": True},
            }
        },
        "legend": {"data": legend_data},
        "xAxis": [
            {
                "type": 'category',
                "axisTick": {"alignWithLabel": True},
                "data": list(date_list),
            }
        ],
    }


def show_bar(y_data1, y_data2, y_data3, y_data4, date_list):
    """柱状图（总批数/合格批数/NG批数）+ 折线图（批次合格率）。"""
    legend = ['总批数', '合格批数', 'NG批数', '百分比']
    option = _base_option(date_list, legend)
    option["yAxis"] = [
        {
            "type": 'value',
            "name": '数量',
            "position": 'left',
            "alignTicks": True,
            "axisLine": {"show": True, "lineStyle": {"color": COLORS[0]}},
        },
        {
            "type": 'value',
            "name": '百分比',
            "position": 'right',
            "alignTicks": False,
            "axisLine": {"show": True, "lineStyle": {"color": COLORS[3]}},
            "axisLabel": {"formatter": '{value} %'},
        },
    ]
    option["series"] = [
        {"name": '总批数', "type": 'bar', "yAxisIndex": 0, "data": y_data1},
        {"name": '合格批数', "type": 'bar', "yAxisIndex": 0, "data": y_data2},
        {"name": 'NG批数', "type": 'bar', "yAxisIndex": 0, "data": y_data3},
        {"name": '百分比', "type": 'line', "yAxisIndex": 1, "data": y_data4, "label": LABEL_STYLE},
    ]
    return st_echarts(options=option)


def draw_line(y_data1, y_data2, y_data3, y_data4, y_data5, date_list, legend_label):
    """5 线折线图：外观/装配/低错/功能/配件。"""
    option = _base_option(date_list, legend_label)
    option["yAxis"] = [
        {
            "type": 'value',
            "name": '数量',
            "position": 'left',
            "alignTicks": True,
            "axisLine": {"show": False, "lineStyle": {"color": COLORS[0]}},
        }
    ]
    series_data = [y_data1, y_data2, y_data3, y_data4, y_data5]
    option["series"] = [
        {"name": name, "type": 'line', "data": data, "label": LABEL_STYLE}
        for name, data in zip(legend_label, series_data)
    ]
    return st_echarts(options=option)


def draw_plot_line_chart(datas, column_names, date_list):
    """可变数据折线图：datas 为 series 列表，column_names 为图例。"""
    option = _base_option(date_list, column_names)
    option["yAxis"] = [
        {
            "type": 'value',
            "name": '数量',
            "position": 'left',
            "alignTicks": True,
            "axisLine": {"show": False, "lineStyle": {"color": COLORS[0]}},
        }
    ]
    option["series"] = datas
    return st_echarts(options=option)
