"""项目共享配置：路径、供应商、密码、问题分类。"""
from pathlib import Path

# 数据文件路径（统一从这里取，避免散落在各文件中硬编码）
BASE_DIR = Path(__file__).parent
EXCEL_PATH = str(BASE_DIR / "product_data_of_oem.xlsx")
EXCEL_SHEET = "数据源"

# 问题分类（按月统计 NG 问题时使用）
PROBLEM_CATEGORIES = ["外观", "装配", "低错", "功能", "配件"]

# 全部供应商列表（用于 DSM 管理员视角）
GYS_CHOOSE_LIST = ["介宏", "方汇", "樱花", "荣硕", "协创", "裕鹰", "all"]

# 供应商密码：键值对（键=密码，值=供应商中文名）
# 注：明文存储仅为兼容现有部署流程，安全升级时应迁到环境变量或 hash
GYS_PSW = {
    "lf_06w": "介宏",
    "msh_07x": "曼申",
    "fh_07s": "方汇",
    "yh_07g": "樱花",
    "xc_09h": "协创",
    "rs_08": "荣硕",
    "yy_07": "裕鹰",
}

# 管理员密码
ADMIN_PSW = "DSM"
