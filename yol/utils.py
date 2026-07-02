# -*- encoding: utf-8 -*-

from ultralytics import YOLO
from PIL import Image, ImageDraw
import cv2
import streamlit as st
import tempfile



#Image.MAX_IMAGE_PIXELS = None   #取消图像最大限制


# 定义疾病字典（中文名称和详情）
disease_dic = {
    'black_root': {
        'name': '黑腐病',
        'info': """黑腐病危害症状：：""",
        'solve':"""黑腐病防治方法：""",
        'ill_image':'../pic/grape/rot/rot.jpg',
        'sov_image':'../pic/grape/rot/rot_sov.jpg',
    },
    'black_measles': {
        'name': '黑痘病（出血性麻疹）',
        'info': """黑痘病危害症状：""",
        'solve':"""黑痘病防治方法：""",
        'ill_image':'../pic/grape/pot/pot.jpg',
        'sov_image':'../pic/grape/pot/pot_sov.jpg',
    },
    'blight': {
        'name': '褐斑病',
        'info': """褐斑病危害症状：""",
        'solve': """褐斑病防治方法：""",
        'ill_image':'../pic/grape/blight/blight.jpg',
        'sov_image':'../pic/grape/blight/blight_sov.jpg',
    },
    'healthy': {
        'name': '健康',
        'info': """您的葡萄正在健康成长！""",
        'solve': """葡萄种植小知识：""",
        'ill_image':'../pic/grape/health/left.jpg',
        'sov_image':'../pic/grape/health/right.jpg',
    },
    'Acidrot': {
        'name': '酸腐病',
        'info': """酸腐病危害症状：""",
        'solve': """酸腐病防治方法：""",
        'ill_image':'../pic/grape/sour/sour.jpg',
        'sov_image':'../pic/grape/sour/sour_sov.jpg',
    },
    'Downymildew': {
        'name': '霜霉病',
        'info': """霜霉病危害症状：""",
        'solve': """霜霉病防治方法：""",
        'ill_image': '../pic/grape/downy/downy.jpg',
        'sov_image': '../pic/grape/downy/downy_sov.jpg',
    },
    'Ulcerdisease': {
        'name': '溃疡病',
        'info': """溃疡病危害症状：""",
        'solve': """溃疡病防治方法：""",
        'ill_image': '../pic/grape/canker/canker_1.jpg',
        'sov_image': '../pic/grape/canker/canker_sov.jpg',
    },
    'Botrytiscinerea': {
        'name': '灰霉病',
        'info': """灰霉病危害症状：""",
        'solve': """灰霉病防治方法：""",
        'ill_image': '../pic/grape/gray/gray.jpg',
        'sov_image': '../pic/grape/gray/gray_sov.jpg',
    },
    'Mosaicvirusdisease': {
        'name': '花叶病',
        'info': """花叶病危害症状：""",
        'solve': """花叶病防治方法：""",
        'ill_image': '../pic/grape/flower/flower.jpg',
        'sov_image': '../pic/grape/flower/flower_sov.jpg',
    },


    #苹果
    'Brown_spot': {
        'name': '褐斑病',
        'info': """褐斑病危害症状：""",
        'solve': """褐斑病防治方法：""",
        'ill_image': '../pic/apple/Brown_spot/Brown_spot_1.jpg',
        'sov_image': '../pic/apple/Brown_spot/Brown_spot_sov.jpg',
    },
    'Health': {
        'name': '健康',
        'info': """您的苹果正在健康成长！""",
        'solve': """苹果种植小知识：：""",
        'ill_image': '../pic/apple/Health/left.jpg',
        'sov_image': '../pic/apple/Health/right.jpg',
    },
    'Mosaic': {
        'name': '花叶病',
        'info': """花叶病危害症状：""",
        'solve': """花叶病防治方法：""",
        'ill_image': '../pic/apple/Mosaic/Mosaic.jpg',
        'sov_image': '../pic/apple/Mosaic/Mosaic_sov.jpg',
    },
    'Powdery_mildew': {
        'name': '白粉病',
        'info': """白粉病危害症状：""",
        'solve': """白粉病防治方法：""",
        'ill_image': '../pic/apple/Powdery_mildew/Powdery_mildew.jpg',
        'sov_image': '../pic/apple/Powdery_mildew/Powdery_mildew_sov.jpg',
    },
    'Rust': {
        'name': '腐烂病',
        'info': """腐烂病危害症状：""",
        'solve': """腐烂病防治方法：""",
        'ill_image': '../pic/apple/Rust/Rust.jpg',
        'sov_image': '../pic/apple/Rust/Rust_sov.jpg',
    },


    #水稻病害
    '0 BrownSpot': {
        'name': '褐斑病',
        'info': """褐斑病危害症状：""",
        'solve': """褐斑病防治方法：""",
        'ill_image': '../pic/rice/0 BrownSpot/BrownSpot.jpg',
        'sov_image': '../pic/rice/0 BrownSpot/BrownSpot_sov.jpg',
    },
    '1 RiceBlast': {
        'name': '稻瘟病',
        'info': """稻瘟病危害症状：""",
        'solve': """稻瘟病防治方法：""",
        'ill_image': '../pic/rice/1 RiceBlast/RiceBlast.jpg',
        'sov_image': '../pic/rice/1 RiceBlast/RiceBlast_sov.jpg',
    },
    '2 BacterialBlight': {
        'name': '白叶枯病',
        'info': """白叶枯病危害症状：""",
        'solve': """白叶枯病防治方法：""",
        'ill_image': '../pic/rice/2 BacterialBlight/BacterialBlight.jpg',
        'sov_image': '../pic/rice/2 BacterialBlight/BacterialBlight_sov.jpg',
    },

    #水稻虫害
    '1': {
        'name': '稻蝽虫卵：',
        'info': """稻蝽虫病害介绍：""",
        'solve': """稻蝽虫防治方法：""",
        'ill_image': '../pic/insect/green.jpg',
        'sov_image': '../pic/insect/green_sov.jpg',
    },
    '2': {
        'name': '小菜蛾：',
        'info': """小菜蛾病害介绍：""",
        'solve': """小菜蛾防治方法：""",
        'ill_image': '../pic/insect/cabage.jpg',
        'sov_image': '../pic/insect/cabage_sov.jpg',
    },
    '3': {
        'name': '二化螟幼虫：',
        'info': """二化螟病害介绍：""",
        'solve': """二化螟防治方法：""",
        'ill_image': '../pic/insect/two.jpg',
        'sov_image': '../pic/insect/two_sov.jpg',
    },
    '4': {
        'name': '二化螟成虫：',
        'info': """二化螟病害介绍：""",
        'solve': """二化螟防治方法：""",
        'ill_image': '../pic/insect/two.jpg',
        'sov_image': '../pic/insect/two_sov.jpg',
    },
    '5': {
        'name': '稻绿蝽：',
        'info': """稻蝽虫病害介绍：""",
        'solve': """稻蝽虫防治方法：""",
        'ill_image': '../pic/insect/green.jpg',
        'sov_image': '../pic/insect/green_sov.jpg',
    },
    '6': {
        'name': '稻绿蝽：',
        'info': """稻蝽虫病害介绍：""",
        'solve': """稻蝽虫防治方法：""",
        'ill_image': '../pic/insect/green.jpg',
        'sov_image': '../pic/insect/green_sov.jpg',
    },
    '7': {
        'name': '稻绿蝽：',
        'info': """稻蝽虫病害介绍：""",
        'solve': """稻蝽虫防治方法：""",
        'ill_image': '../pic/insect/green.jpg',
        'sov_image': '../pic/insect/green_sov.jpg',
    },
    '8': {
        'name': '蝗虫：',
        'info': """蝗虫病害介绍：""",
        'solve': """蝗虫防治方法：""",
        'ill_image': '../pic/insect/locust.jpg',
        'sov_image': '../pic/insect/locust_sov.jpg',
    },
}


def count_labels(boxes, labels):
    """
    统计标签数量
    :param boxes: 目标检测框信息
    :param labels: 类别标签信息
    :return: 字典，包含标签数量信息
    """
    labels_num_dict = {}
    for box in boxes:
        label_index = box.cls.cpu().detach().numpy()[0].astype(int)
        for key in labels.keys():
            if int(label_index) == key:
                if labels[key] in labels_num_dict:
                    labels_num_dict[labels[key]] += 1
                else:
                    labels_num_dict[labels[key]] = 1
    return labels_num_dict


def detection_results(labels_num_dict):
    """
    显示检测结果数量及疾病详情
    :param labels_num_dict: 字典，包含标签数量信息
    """
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-weight: bold;'>检测结果</h3><br>", unsafe_allow_html=True)
    for label, count in labels_num_dict.items():
        chinese_name = get_disease_name(label)
        disease_info = get_disease_info(label)
        st.markdown(f"<b>{chinese_name}</b>: {count} ", unsafe_allow_html=True)
        st.write(disease_info)
    st.markdown("</div>", unsafe_allow_html=True)

    if label in disease_dic:
        # 获取对应疾病的信息
        disease_info = disease_dic[label]
        # 读取要插入的图片文件
        img_path = disease_info.get('ill_image', '')  # 获取图片路径，如果没有则为空字符串
        if img_path:
            rot_image1 = Image.open(img_path)
            # 显示插入的图片
            st.image(rot_image1, use_column_width=True)
        else:
            st.write("没有找到图片。")
    else:
        st.write("没有找到相关疾病的信息。")





def detection_solve(labels_num_dict):
    """
    显示检测结果数量及疾病详情，包括疾病解决方案和相关图片
    :param labels_num_dict: 字典，包含标签数量信息
    """
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-weight: bold;'><br><br>防治技术<br><br></h3>", unsafe_allow_html=True)
    for label, count in labels_num_dict.items():
        if label in disease_dic:
            disease_info = get_disease_info(label)
            solve_info = disease_dic[label]['solve']  # 获取疾病解决方案
            st.write(solve_info)  # 显示解决方案信息
    st.markdown("</div>", unsafe_allow_html=True)

    if label in disease_dic:
        # 获取对应疾病的信息
        disease_info = disease_dic[label]
        # 读取要插入的图片文件
        img_path = disease_info.get('sov_image', '')  # 获取图片路径，如果没有则为空字符串
        if img_path:
            rot_image1 = Image.open(img_path)
            # 显示插入的图片
            st.image(rot_image1, use_column_width=True)
        else:
            st.write("没有找到图片。")
    else:
        st.write("没有找到相关疾病的信息。")




def get_disease_name(label, font_size='18px'):
    """根据label获取对应的中文疾病名称，并设置字体大小"""
    chinese_name = disease_dic.get(label, {}).get('name', label)
    return f"<span style='font-size: {font_size};'>{chinese_name}</span>"


def get_disease_info(label):
    """根据label获取对应的疾病详情"""
    if label in disease_dic:
        return disease_dic[label]['info']
    else:
        return '暂无详情信息'  # 可根据需要进行修改

@st.cache_resource
def load_model(model_path):
    """
    从具体的路径中加载一个模型
    Parameters:
        model_path (str): The path to the YOLO model file.
    Returns:
         YOLO 模型
    """
    model = YOLO(model_path)
    return model



def infer_uploaded_image(conf, model):
    """
    执行图片推理
    :param conf: Confidence of YOLO model
    :param model: An instance of the `YOLO class containing the YOLO model.
    :return: None
    """
    source_img = st.sidebar.file_uploader(
        label="选择一张图片...",
        type=("jpg", "jpeg", "png", 'bmp', 'webp')
    )
    # 页面划分一个区域用于显示检测前后的图片（一行两列）
    col1, col2 = st.columns(2)

    with col1:
        if source_img:
            uploaded_image = Image.open(source_img)
            # 将原始图片显示在页面中(col1位置)
            st.image(
                image=uploaded_image,
                caption="上传图片",
                use_column_width=True
            )


        if source_img:
            if st.button("执行"):
                with st.spinner("执行中..."):
                    """yolo预测返回的结果全在返回变量res中
                    这是一个ultralytics.yolo.engine.results.Results 类
                    该类包含了检测、分割、关键点检测、分类任务的所有预测信息
                    Results类中names属性:类别标签
                    boxes属性:目标检测信息
                    masks：实例分割信息
                    probs：图像分类信息
                    keypoints：人体关键点检测信息
                    具体信息可以参看 ultralytics.yolo.engine.results 路径中的Results类
                    """
                    res = model.predict(uploaded_image, conf=conf)
                    if res is not None:
                        labels = res[0].names
                        # 转换为中文标签
                        chinese_labels = [get_disease_name(label) for label in labels]
                        boxes = res[0].boxes
                        res_plotted = res[0].plot()[:, :, ::-1]
                        # 调用 count_labels 函数统计标签数量
                        labels_num_dict = count_labels(boxes, labels)
                        with col2:
                            st.image(res_plotted, caption="检测图片", use_column_width=True)
                            # 调用函数显示检测结果数量及疾病详情
                            detection_solve(labels_num_dict)

                        with col1:
                            try:
                                # 调用函数显示检测结果数量及疾病详情
                                detection_results(labels_num_dict)
                            except Exception as ex:
                                st.write("未检测到目标!")
                                st.write(ex)
                    else:
                        st.write("未检测到目标!")






def infer_uploaded_video(conf, model):
    """
    执行视频推理
    :param conf: YOLOv8 模型的置信度
    :param model: 包含 YOLOv8 模型的 `YOLOv8` 类的实例。
    :return: None
    """
    source_video = st.sidebar.file_uploader(
        label="选择一个视频..."
    )

    # 创建一个字典用于存储疾病标签及其数量
    disease_labels_count = {}

    # 在页面中显示传入的原始视频
    if source_video:
        col1, col2 = st.columns(2)
        with col1:
            st.video(source_video)

        # 页面划分一个区域用于显示检测前后的图片和疾病详情（一行两列）
        with col1:
            if st.button("执行"):
                with st.spinner("执行中..."):
                    with col2:
                        try:
                            tfile = tempfile.NamedTemporaryFile()
                            tfile.write(source_video.read())
                            vid_cap = cv2.VideoCapture(
                                tfile.name)

                            # 页面创建两个空容器一个实时播放画面一个实时展示信息
                            st_frame = st.empty()
                            st_text = st.empty()
                            while (vid_cap.isOpened()):
                                success, image = vid_cap.read()
                                if success:
                                    # 调用方法逐帧预测
                                    _display_detected_frames(conf,
                                                             model,
                                                             st_frame,
                                                             st_text,
                                                             image,
                                                             disease_labels_count
                                                             )
                                else:
                                    vid_cap.release()
                                    break
                        except Exception as e:
                            st.error(f"加载视频时出错: {e}")



                    # 显示疾病标签名称和相关信息
                    with col1:
                        st.markdown("**<big>检测到有以下病害：</big>**", unsafe_allow_html=True)
                        for label0, count in disease_labels_count.items():
                            label_name0 = disease_dic[label0]['name']
                            st.write(label_name0)

                        with col2:
                            for _ in range(30):
                                st.write("")
                            st.markdown("<h3 style='font-weight: bold;'>防治技术</h3>",
                                        unsafe_allow_html=True)


                        num = 1
                        for label, count in disease_labels_count.items():
                            label_name = disease_dic[label]['name']
                            # st.write(label_name)


                            # 显示疾病图片和名称
                            ill_image_path = disease_dic[label]['ill_image']
                            sov_image_path = disease_dic[label]['sov_image']

                            with col1:
                                st.write("")
                                st.write(f"**{num}{label_name}疾病介绍**")
                                st.image(ill_image_path)

                            with col2:
                                st.write("")
                                st.write(f"**{num}{label_name}防治措施**")
                                st.image(sov_image_path)
                            num += 1







def _display_detected_frames(conf, model, st_frame, st_text, image, label_counts):
    """
    逐帧推理
    :param conf (float): Confidence threshold for object detection.
    :param model (YOLOv8): An instance of the `YOLOv8` class containing the YOLOv8 model.
    :param st_frame (Streamlit object): A Streamlit object to display the detected video.
    :param image (numpy array): A numpy array representing the video frame.
    :param label_counts (dict): A dictionary to store label counts.
    :return: None
    """
    # 设置每一帧(图片)合适的大小  显示在页面中
    image = cv2.resize(image, (720, int(720 * (9 / 16))))

    # yolo模型推理预测
    res = model.predict(image, conf=conf)

    res_plotted = res[0].plot()

    # 将后处理的检测目标(带框)逐帧显示在页面上
    st_frame.image(res_plotted,
                   caption='Detected Video',
                   channels="BGR",
                   use_column_width=True
                   )

    # 统计疾病标签的数量
    if res is not None:
        labels = res[0].names
        for box in res[0].boxes:
            label_index = int(box.cls.cpu().detach().numpy()[0])
            label_name = labels[label_index]
            if label_name in label_counts:
                label_counts[label_name] += 1
            else:
                label_counts[label_name] = 1




def infer_uploaded_webcam(conf, model):
    """
    执行实时摄像头推理
    :param conf: YOLO 模型的置信度阈值
    :param model: 包含 YOLO 模型的 `YOLO` 类的实例。
    :return: None
    """
    try:
        # 创建一个按钮用于终止执行
        flag = st.button(label="终止执行")

        # 打开本地摄像头
        vid_cap = cv2.VideoCapture(0)

        # 创建两个空的 Streamlit 容器，用于显示实时播放画面和实时展示信息
        st_frame = st.empty()
        st_text = st.empty()

        # 循环捕获摄像头图像，并进行推理
        while not flag:
            # 读取摄像头图像帧
            success, image = vid_cap.read()

            if success:
                # 调用方法逐帧进行推理，并在页面上显示结果
                _display_detected_frames(conf, model, st_frame, st_text, image, {})
            else:
                # 如果无法读取图像帧，则释放摄像头资源并退出循环
                vid_cap.release()
                break

    except Exception as e:
        # 如果出现异常，则在页面上显示错误消息
        st.error(f"加载视频时出错: {str(e)}")
