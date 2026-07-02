# -*- encoding: utf-8 -*-


#系统主类,系统程序的入口,在命令行中运行该类
from pathlib import Path
from PIL import Image
import streamlit as st
import config
from utils import load_model, infer_uploaded_image, infer_uploaded_video, infer_uploaded_webcam

# 设置页面布局
st.set_page_config(
    page_title="yolov8",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
    )

# img_path = "../pic/logo.png"  # 替换为您实际图片的路径
# st.image(img_path, width=100)

# 显示标题
st.title("基于YOLOV8的病虫害专家系统")

# 侧边栏标题
st.sidebar.header("模型配置")

# # 侧边栏-任务选择
# task_type = st.sidebar.selectbox(
#     "选择要进行的任务",
#     ["葡萄病虫害检测"]
# )

# 侧边栏-任务选择
task_type = st.sidebar.selectbox(
    "选择要进行的任务",
    ["葡萄病虫害检测", "苹果病虫害检测", "水稻病虫害检测"]
)

# 清空图片上传部分
source_img = None

# 从config.py中获取相应的模型选择列表
DETECTION_MODEL_LIST = config.get_detection_model_list(task_type)

# 侧边栏-模型选择
model_type = st.sidebar.selectbox(
    "选取模型",
    DETECTION_MODEL_LIST
)




# model_type = None
# # 侧边栏-模型选择
# if task_type == "葡萄病虫害检测":
#     model_type = st.sidebar.selectbox(
#         "选取模型",
#         config.DETECTION_MODEL_LIST
#     )
# else:
#     st.error("目前仅仅实现了目标检测任务")


#侧边栏-置信度
confidence = float(st.sidebar.slider(
    "选取最小置信度", 10, 100, 25)) / 100

model_path = ""
if model_type:
    model_path = Path(config.DETECTION_MODEL_DIR, str(model_type))
else:
    st.error("请在下拉框选择一个模型")

# 加载模型
try:
    model = load_model(model_path)
except Exception as e:
    st.error(f"无法加载模型. 请检查路径: {model_path}")


# # 加载模型
# try:
#     model = load_model(model_path)
#     st.success("模型加载成功！")
# except Exception as e:
#     st.error(f"无法加载模型. 请检查路径: {model_path}")
#     st.error(f"异常信息: {str(e)}")


# 侧边栏-图像、视频、摄像头选择
st.sidebar.header("图片/视频配置")
source_selectbox = st.sidebar.selectbox(
    "选取文件类型",
    config.SOURCES_LIST
)

source_img = None
if source_selectbox == config.SOURCES_LIST[2]: # 摄像头
    infer_uploaded_webcam(confidence,model)
elif source_selectbox == config.SOURCES_LIST[0]: # 视频
    infer_uploaded_image(confidence, model)
elif source_selectbox == config.SOURCES_LIST[1]: # 视频
    infer_uploaded_video(confidence, model)
else:
    st.error("目前仅支持 '图片' '视频' '本地摄像头' ")