import datetime
import pandas as pd
import streamlit as st
from utils.dbi_calculator import calculate_dbi_metrics
from utils.prediction import predict_burnout

# Cấu hình giao diện trang làm bài khảo sát
st.set_page_config(page_title="Assessment Form", layout="wide")

st.title("Khảo sát đánh giá tình trạng kiệt sức kỹ thuật số")
st.write("Vui lòng nhập đầy đủ các thông tin dưới đây để hệ thống tiến hành phân tích điểm số.")

# Tạo form thu thập thông tin người dùng
with st.form("assessment_form"):
    
    # Nhóm thông tin cá nhân cơ bản
    st.subheader("Personal Information")
    gender = st.selectbox("Giới tính", ["Male", "Female", "Other"])
    birth_year = st.number_input("Năm sinh", min_value=1990, max_value=2020, value=2004)
    education_stage = st.selectbox("Giai đoạn học tập", ["Undergraduate Year 1", "Undergraduate Year 2", "Undergraduate Year 3", "Undergraduate Year 4", "Postgraduate"])
    work_mode = st.selectbox("Hình thức làm việc học tập", ["Onsite", "Hybrid", "Remote"])
    device_usage_type = st.selectbox("Mục đích sử dụng thiết bị chủ yếu", ["Study", "Entertainment", "Work", "Mixed"])

    # Nhóm chỉ số về mức độ tiếp xúc với thiết bị kỹ thuật số
    st.subheader("Digital Exposure")
    daily_screen_time = st.slider("Thời gian sử dụng màn hình hàng ngày (giờ)", 0.0, 16.0, 6.0)
    social_media_hours = st.slider("Thời gian dùng mạng xã hội hàng ngày (giờ)", 0.0, 12.0, 3.0)
    doomscrolling_duration = st.slider("Thời gian lướt mạng vô định - doomscrolling (giờ)", 0.0, 8.0, 1.0)
    late_night_device_usage = st.slider("Thời gian dùng thiết bị muộn ban đêm (giờ)", 0.0, 6.0, 1.0)
    notification_count = st.number_input("Số lượng thông báo nhận được mỗi ngày", min_value=0, max_value=1000, value=80)
    smartphone_unlocks = st.number_input("Số lần mở khóa điện thoại hàng ngày", min_value=0, max_value=500, value=50)
    app_switch_frequency = st.slider("Tần suất chuyển đổi qua lại giữa các ứng dụng (thang điểm 1-10)", 1, 10, 5)

    # Nhóm chỉ số về hiệu suất nhận thức và sự tập trung
    st.subheader("Cognitive Performance")
    concentration_score = st.slider("Mức độ tập trung tự đánh giá (thang điểm 1-10)", 1, 10, 6)
    distraction_frequency = st.slider("Tần suất bị phân tâm khi học tập (thang điểm 1-10)", 1, 10, 5)
    focus_sessions = st.number_input("Số phiên tập trung làm việc sâu trong ngày", min_value=0, max_value=20, value=3)
    deep_work_hours = st.slider("Tổng số giờ làm việc sâu trong ngày (giờ)", 0.0, 12.0, 2.0)
    task_completion_rate = st.slider("Tỷ lệ hoàn thành công việc đề ra (%)", 0, 100, 75)

    # Nhóm chỉ số về giấc ngủ và khả năng phục hồi
    st.subheader("Sleep Recovery")
    sleep_hours = st.slider("Số giờ ngủ trung bình mỗi đêm (giờ)", 3.0, 12.0, 7.0)
    sleep_quality = st.slider("Chất lượng giấc ngủ tự đánh giá (thang điểm 1-10)", 1, 10, 6)

    # Nhóm chỉ số về các triệu chứng tâm lý cá nhân
    st.subheader("Psychological Symptoms")
    emotional_exhaustion = st.slider("Mức độ kiệt quệ về cảm xúc (thang điểm 1-10)", 1, 10, 4)
    stress_level = st.slider("Mức độ căng thẳng áp lực (thang điểm 1-10)", 1, 10, 5)
    mental_fatigue = st.slider("Mức độ mệt mỏi tinh thần (thang điểm 1-10)", 1, 10, 4)
    motivation_level = st.slider("Mức độ động lực học tập (thang điểm 1-10)", 1, 10, 6)

    # Nhóm bổ sung dành riêng cho mô hình dự đoán Machine Learning
    st.subheader("Additional ML Features")
    work_satisfaction = st.slider("Mức độ hài lòng với việc học tập công việc (thang điểm 1-10)", 1, 10, 6)
    physical_activity = st.slider("Thời gian vận động thể chất hàng ngày (giờ)", 0.0, 4.0, 0.5)
    meeting_hours = st.slider("Số giờ tham gia họp hoặc thảo luận nhóm hàng ngày (giờ)", 0.0, 8.0, 1.0)
    workspace_quality = st.slider("Chất lượng không gian học tập làm việc (thang điểm 1-10)", 1, 10, 7)
    internet_stability = st.slider("Độ ổn định của kết nối mạng internet (thang điểm 1-10)", 1, 10, 8)
    caffeine_intake = st.slider("Số ly thức uống chứa caffeine tiêu thụ mỗi ngày", 0, 10, 1)
    remote_work_days = st.slider("Số ngày học tập trực tuyến từ xa trong tuần", 0, 7, 2)

    # Nút bấm xử lý gửi dữ liệu khảo sát
    submit_button = st.form_submit_button(label="Gửi đánh giá")

# Xử lý tính toán sau khi người dùng nhấn nút gửi biểu mẫu
if submit_button:
    current_year = datetime.datetime.now().year
    age = current_year - birth_year

    # Tạo từ điển lưu trữ dữ liệu gốc phục vụ tính toán dbi
    raw_inputs = {
        "gender": gender,
        "birth_year": birth_year,
        "education_stage": education_stage,
        "work_mode": work_mode,
        "device_usage_type": device_usage_type,
        "daily_screen_time": daily_screen_time,
        "social_media_hours": social_media_hours,
        "doomscrolling_duration": doomscrolling_duration,
        "late_night_device_usage": late_night_device_usage,
        "notification_count": notification_count,
        "smartphone_unlocks": smartphone_unlocks,
        "app_switch_frequency": app_switch_frequency,
        "concentration_score": concentration_score,
        "distraction_frequency": distraction_frequency,
        "focus_sessions": focus_sessions,
        "deep_work_hours": deep_work_hours,
        "task_completion_rate": task_completion_rate,
        "sleep_hours": sleep_hours,
        "sleep_quality": sleep_quality,
        "emotional_exhaustion": emotional_exhaustion,
        "stress_level": stress_level,
        "mental_fatigue": mental_fatigue,
        "motivation_level": motivation_level,
        "work_satisfaction": work_satisfaction,
        "physical_activity": physical_activity,
        "meeting_hours": meeting_hours,
        "workspace_quality": workspace_quality,
        "internet_stability": internet_stability,
        "caffeine_intake": caffeine_intake,
        "remote_work_days": remote_work_days,
        "age": age
    }

    # Thực hiện tính toán các chỉ số dbi và dự đoán rủi ro
    dbi_results = calculate_dbi_metrics(raw_inputs)
    prediction, prediction_probability = predict_burnout(raw_inputs)

    # Ghi nhận kết quả xử lý vào session state của hệ thống
    st.session_state["user_input"] = raw_inputs
    st.session_state["dbi_results"] = dbi_results
    st.session_state["ml_prediction"] = prediction
    st.session_state["ml_probability"] = prediction_probability

    st.success("Hệ thống đã ghi nhận thông tin khảo sát. Vui lòng chuyển sang trang Result để xem kết quả phân tích chi tiết.")