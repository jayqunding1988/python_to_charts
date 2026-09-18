"""质量问题因果关系图：用 graphviz 展示问题传导链。"""
import streamlit as st
import graphviz


def build_graph() -> "graphviz.Digraph":
    """构建质量问题因果图。"""
    g = graphviz.Digraph()
    g.edge('制程管理', '外观')
    g.edge('制程管理', '钥匙交叉')
    g.edge('制程管理', '指纹线压线')
    g.edge('制程管理', '钥匙变形')
    g.edge('制程管理', '指纹线松脱')

    g.edge('钥匙交叉', '锁芯故障')
    g.edge('钥匙变形', '锁芯故障')
    g.edge('指纹线压线', '指纹头失效')
    g.edge('指纹线松脱', '指纹头失效')
    g.edge('使用过程撞击', '指纹头失效')

    g.edge('指纹头本体不良', '指纹头失效')
    g.edge('指纹头本体不良', '不通电')
    g.edge('指纹头本体不良', '耗电快')
    g.edge('指纹头失效问题', '不通电')
    g.edge('指纹头回用', '不通电')
    g.edge('电池盒弹簧脱落/短路', '不通电')
    g.edge('面板连接线被压断', '不通电')
    g.edge('面板连接线被压断', '开门故障')
    g.edge('电池盒弹簧脱落/短路', '耗电快')
    g.edge('引脚短路/硬件失效', '耗电快')
    g.edge('引脚短路/硬件失效', '不通电')
    g.edge('引脚短路/硬件失效', '开门故障')
    g.edge('锁体故障问题', '开门故障')
    g.edge('引脚短路/硬件失效', '锁体故障')
    g.edge('指纹头回用', '指纹头本体不良')
    return g


def main():
    st.graphviz_chart(build_graph(), use_container_width=True)


if __name__ == "__main__":
    main()
