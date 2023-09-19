import streamlit as st
from streamlit_echarts import st_echarts

def show_bar(y_data1,y_data2,y_data3,y_data4,date_list):
    """主要功能：显示柱状图和折线图的组合图"""
    colors = ['#5470C6', '#91CC75', '#EE6666','green','lightblue']
    option = {
    "color": colors,
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": {
        "type": 'cross'
        }
    },
    "grid": {
        "right": '5%'
    },
    "toolbox": {
        "feature": {
        "dataView": { "show": True, "readOnly": True },
        "restore": { "show": True },
        "saveAsImage": { "show": True }
        }
    },
    "legend": {
        "data": ['总批数', '合格批数', 'NG批数','百分比']
    },
    "xAxis": [
        {
        "type": 'category',
        "axisTick": {
            "alignWithLabel": True
        },
        #   // prettier-ignore
        "data": date_list
        }
    ],
    "yAxis": [
        {
        "type": 'value',
        "name": '',
        "position": '',
        "alignTicks": True,
        "axisLine": {
            "show": True,
            "lineStyle": {
            "color": colors[0]
            }
        },
        # "axisLabel": {
        #     "formatter": '{value}'
        # }
        },
        {
        "type": 'value',
        "name": '合格批数',
        "position": 'right',
        "alignTicks": True,
        "offset": 80,
        "axisLine": {
            "show": False,
            "lineStyle": {
            "color": colors[1]
            }
        },
        # "axisLabel": {
        #     "formatter": '{value}'
        # }
        },
        {
        "type": 'value',
        "name": '',
        "position": 'right',
        "alignTicks": True,
        "axisLine": {
            "show": False,
            "lineStyle": {
                "color": colors[2]
            }
        },
        # "axisLabel": {
        #     "formatter": '{value}'
        # }
        },
        {
        "type": 'value',
        "name": '百分比',
        "position": 'left',
        "alignTicks": False,
        "axisLine": {
            "show": True,
            "lineStyle": {
                "color": colors[3]
            }
        },
        "axisLabel": {
            "formatter": '{value} %'
        }
        }
    ],
    "series": [
        {
        "name": '总批数',
        "type": 'bar',
        "yAxisIndex": 2,
        "data": y_data1
        },
        {
        "name": '合格批数',
        "type": 'bar',

        # "yAxisIndex": 2,
        "data":y_data2
        },
        {
        "name": 'NG批数',
        "type": 'bar',
        # "yAxisIndex": 2,
        "data": y_data3
        },
        {
        "name": '百分比',
        "type": 'line',
        "yAxisIndex": 1,
        "data": y_data4,
        "label":{
            "show":True,
            "textStyle":{
                "color":"#bb33f6",
                "fontsize":14
            }
        }
    }]}
    values_echart = st_echarts(options=option)
    return values_echart







def draw_line(y_data1,y_data2,y_data3,y_data4,y_data5,date_list, legend_label):
    """
    主要功能：显示5线折线图\n
    legend_label:5条折线对应的名称
    """
    colors = ['#5470C6', '#91CC75', '#EE6666','green','lightblue']
    option = {
    "color": colors,
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": {
        "type": 'cross'
        }
    },
    "grid": {
        "right": '5%'
    },
    "toolbox": {
        "feature": {
        "dataView": { "show": True, "readOnly": True },
        "restore": { "show": True },
        "saveAsImage": { "show": True }
        }
    },
    "legend": {
        "data": legend_label
    },
    "xAxis": [
        {
        "type": 'category',
        "axisTick": {
            "alignWithLabel": True
        },
        #   // prettier-ignore
        "data": date_list
        }
    ],
    "yAxis": [
        {
        "type": 'value',
        "name": '数量',
        "position": 'left',
        "alignTicks": True,
        "axisLine": {
            "show": False,
            "lineStyle": {
            "color": colors[0]
            }
        },
        # "axisLabel": {
        #     "formatter": '{value}'
        # }
        },
        {
        "type": 'value',
        "name": '',
        "position": 'left',
        "alignTicks": False,
        "offset": 80,
        "axisLine": {
            "show": False,
            "lineStyle": {
            "color": colors[1]
            }
        },
        # "axisLabel": {
        #     "formatter": '{value}'
        # }
        },
        {
        "type": 'value',
        "name": '',
        "position": 'left',
        "alignTicks": False,
        "axisLine": {
            "show": False,
            "lineStyle": {
                "color": colors[2]
            }
        },
        # "axisLabel": {
        #     "formatter": '{value}'
        # }
        },
        {
        "type": 'value',
        "name": '',
        "position": 'left',
        "alignTicks": False,
        "axisLine": {
            "show": False,
            "lineStyle": {
                "color": colors[3]
            }
        },
        "axisLabel": {
            "formatter": '{value} %'
        }
        },
        {
        "type": 'value',
        "name": '',
        "position": 'left',
        "alignTicks": False,
        "axisLine": {
            "show": False,
            "lineStyle": {
                "color": colors[3]
            }
        },
        "axisLabel": {
            "formatter": '{value} %'
        }
        }
    ],
    "series": [
        {
        "name": '外观',
        "type": 'line',
        # "yAxisIndex": 2,
        "data": y_data1,
        "label":{
            "show":True,
            "textStyle":{
                "color":"#bb33f6",
                "fontsize":14
            }
        }
        },
        {
        "name": '装配',
        "type": 'line',

        # "yAxisIndex": 2,
        "data":y_data2,
        "label":{
            "show":True,
            "textStyle":{
                "color":"#bb33f6",
                "fontsize":14
            }
        }
        },
        {
        "name": '低错',
        "type": 'line',
        # "yAxisIndex": 2,
        "data": y_data3,
        "label":{
            "show":True,
            "textStyle":{
                "color":"#bb33f6",
                "fontsize":14
            }
        }
        },
         {
        "name": '功能',
        "type": 'line',
        # "yAxisIndex": 2,
        "data": y_data4,
        "label":{
            "show":True,
            "textStyle":{
                "color":"#bb33f6",
                "fontsize":14
            }
        }
        
        },
        {
        "name": '配件',
        "type": 'line',
        # "yAxisIndex": 1,
        "data": y_data5,
        "label":{
            "show":True,
            "textStyle":{
                "color":"#bb33f6",
                "fontsize":14
            }
        }
    }]}
    values_echart = st_echarts(options=option)
    return values_echart