# -*- encoding: utf-8 -*-

#该类用于配置模型
from pathlib import Path
import sys

#获取当前文件的绝对路径
file_path = Path(__file__).resolve()

#获取当前文件的上一级目录的路径
root_path = file_path.parent

#如果当前文件的父目录不在搜索路径中则添加进去
if root_path not in sys.path:
    sys.path.append(str(root_path))

#获取当前项目(工作目录)的相对路径
ROOT = root_path.relative_to(Path.cwd())
#数据源
SOURCES_LIST = ["图像", "视频","摄像头"]

# 模型路径配置
DETECTION_MODEL_DIR = ROOT / 'weights'


#侧边栏模型选择列表
DETECTION_MODEL_LIST = [
    "grape_a.pt","grape_all.pt","apple.pt","rice.pt"]


# 定义一个函数根据任务类型设置模型选择列表
def get_detection_model_list(task_type):
    if task_type == "葡萄病虫害检测":
        return ["grape_a.pt", "grape_all.pt"]
    elif task_type == "苹果病虫害检测":
        return ["apple.pt"]
    elif task_type == "水稻病虫害检测":
        return ["rice.pt","insect.pt",]
    else:
        return []  # 或者添加其他默认值或错误处理