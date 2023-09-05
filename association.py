
import streamlit as st
import graphviz

graph = graphviz.Digraph()
graph.edge('制程管理', '外观')
graph.edge('制程管理', '钥匙交叉')

graph.edge('制程管理', '指纹线压线')
graph.edge('钥匙交叉', '锁芯故障')
graph.edge('钥匙变形', '锁芯故障')
graph.edge('指纹线压线', '指纹头失效')
graph.edge('指纹线松脱', '指纹头失效')
graph.edge('使用过程撞击', '指纹头失效')

graph.edge('指纹头本体不良', '指纹头失效')
graph.edge('指纹头本体不良', '不通电')
graph.edge('指纹头本体不良', '耗电快')
graph.edge('指纹头失效问题', '不通电')
graph.edge('指纹头回用', '不通电')
graph.edge('电池盒弹簧脱落/短路', '不通电')
graph.edge('面板连接线被压断', '不通电')
graph.edge('面板连接线被压断', '开门故障')
graph.edge('电池盒弹簧脱落/短路', '耗电快')
graph.edge('引脚短路/硬件失效', '耗电快')
graph.edge('引脚短路/硬件失效', '不通电')
graph.edge('引脚短路/硬件失效', '开门故障')
graph.edge('锁体故障问题', '开门故障')
graph.edge('引脚短路/硬件失效', '锁体故障')
graph.edge('指纹头回用', '指纹头本体不良')
graph.edge('制程管理', '钥匙变形')
graph.edge('制程管理', '指纹线松脱')


st.graphviz_chart(graph, use_container_width=True)