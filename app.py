# ==============================================================================
# DIGITAL BURNOUT ASSESSMENT SYSTEM
# Prototype demo cho sinh viên Việt Nam
# Mô hình sử dụng: Voting Classifier (đã được huấn luyện trước)
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. IMPORT LIBRARIES
# ------------------------------------------------------------------------------

# Thư viện xây dựng giao diện web
import streamlit as st

# Thư viện xử lý dữ liệu dạng bảng
import pandas as pd

# Thư viện tính toán số học
import numpy as np

# Thư viện load mô hình Machine Learning đã huấn luyện
import joblib

# Thư viện vẽ biểu đồ
import matplotlib.pyplot as plt

# Thư viện hỗ trợ thao tác đường dẫn file
import os


# ------------------------------------------------------------------------------
# 2. CẤU HÌNH TRANG STREAMLIT
# ------------------------------------------------------------------------------

st.set_page_config(
    page_title="Digital Burnout Assessment",
    layout="wide"
)


# ------------------------------------------------------------------------------
# 3. LOAD MÔ HÌNH MACHINE LEARNING
# ------------------------------------------------------------------------------

# Mục tiêu: Load mô hình Voting Classifier đã được huấn luyện sẵn.
# Nội dung: Sử dụng joblib để đọc file model từ thư mục models/vietnam_dataset.
# Input: Đường dẫn file model best_model.joblib.
# Output: Đối tượng model đã sẵn sàng để dự đoán, hoặc None nếu không tìm thấy file.

MODEL_PATH = os.path.join("models", "vietnam_dataset", "best_model.joblib")


@st.cache_resource
def load_prediction_model(model_path):
    # Load mô hình Machine Learning đã được huấn luyện
    if not os.path.exists(model_path):
        return None
    model = joblib.load(model_path)
    return model


prediction_model = load_prediction_model(MODEL_PATH)


# ------------------------------------------------------------------------------
# 4. ĐỊNH NGHĨA DANH SÁCH FEATURE ĐẦU VÀO CHO MÔ HÌNH
# ------------------------------------------------------------------------------

# Mục tiêu: Xác định đúng thứ tự 15 feature mà mô hình yêu cầu.
# Nội dung: Danh sách được chia theo ba nhóm chỉ số hành vi.
# Input: Không có.
# Output: Danh sách tên cột theo đúng thứ tự đưa vào DataFrame.

DIGITAL_EXPOSURE_FEATURES = [
    "daily_screen_time",
    "social_media_hours",
    "doomscrolling_duration",
    "late_night_device_usage",
    "notification_count",
    "smartphone_unlocks",
    "app_switch_frequency",
]

COGNITIVE_PERFORMANCE_FEATURES = [
    "concentration_score",
    "distraction_frequency",
    "focus_sessions",
    "deep_work_hours",
    "task_completion_rate",
    "motivation_level",
]

SLEEP_RECOVERY_FEATURES = [
    "sleep_hours",
    "sleep_quality",
]

MODEL_FEATURE_ORDER = (
    DIGITAL_EXPOSURE_FEATURES
    + COGNITIVE_PERFORMANCE_FEATURES
    + SLEEP_RECOVERY_FEATURES
)

# Ánh xạ nhãn dự đoán của mô hình sang tiếng Việt
risk_mapping = {
    0: "Nguy cơ thấp",
    1: "Nguy cơ cao",
    2: "Nguy cơ trung bình",
}


# ------------------------------------------------------------------------------
# 5. HÀM XÂY DỰNG DATAFRAME ĐẦU VÀO TỪ CÂU TRẢ LỜI KHẢO SÁT
# ------------------------------------------------------------------------------

# Mục tiêu: Chuyển câu trả lời khảo sát của người dùng thành DataFrame 15 cột.
# Nội dung: Sắp xếp giá trị theo đúng thứ tự feature mà mô hình yêu cầu.
# Input: Dictionary chứa giá trị các feature.
# Output: DataFrame một dòng, 15 cột, đúng thứ tự MODEL_FEATURE_ORDER.

def build_model_input(user_input):
    # Tạo DataFrame một dòng từ dictionary câu trả lời
    input_row = {feature_name: [user_input[feature_name]] for feature_name in MODEL_FEATURE_ORDER}
    model_input_df = pd.DataFrame(input_row)
    return model_input_df


# ------------------------------------------------------------------------------
# 6. HÀM DỰ ĐOÁN DIGITAL BURNOUT BẰNG MÔ HÌNH VOTING CLASSIFIER
# ------------------------------------------------------------------------------

# Mục tiêu: Sử dụng mô hình đã huấn luyện để dự đoán mức độ nguy cơ.
# Nội dung: Gọi predict và predict_proba trên dữ liệu đầu vào của người dùng.
# Input: DataFrame 15 cột theo đúng thứ tự feature.
# Output: Nhãn dự đoán (tiếng Việt) và độ tin cậy tương ứng (phần trăm).

def predict_digital_burnout(model_input_df):
    if prediction_model is None:
        # Trường hợp không tìm thấy file model, trả về giá trị mặc định
        return None, None, None

    # Dự đoán nhãn lớp (0, 1, 2)
    predicted_class = prediction_model.predict(model_input_df)[0]

    # Dự đoán xác suất cho từng lớp
    predicted_proba = prediction_model.predict_proba(model_input_df)[0]

    # Lấy độ tin cậy của lớp được dự đoán
    confidence_score = predicted_proba[predicted_class] * 100

    # Chuyển nhãn số sang nhãn tiếng Việt
    predicted_label = risk_mapping.get(predicted_class, "Không xác định")

    return predicted_label, confidence_score, predicted_proba


# ------------------------------------------------------------------------------
# 7. HÀM TÍNH DIGITAL BURNOUT SCORE (THANG ĐIỂM 0 - 5)
# ------------------------------------------------------------------------------

# Mục tiêu: Cung cấp một điểm số tổng quát dễ hiểu (thang 0 - 5) cho người dùng.
# Nội dung: Vì prototype không có sẵn digital_burnout_score từ dataset gốc,
#           điểm số được ước lượng từ câu trả lời khảo sát theo công thức trọng số
#           dựa trên các chỉ số thuộc khung DBI Framework.
# Input: Dictionary chứa giá trị các feature khảo sát.
# Output: Điểm số digital_burnout_score trong khoảng 0 đến 5.

def calculate_digital_burnout_score(user_input):
    # Chuẩn hóa từng chỉ số về thang điểm 0 - 1, trong đó 1 là mức rủi ro cao nhất
    normalized_screen_time = min(user_input["daily_screen_time"] / 12, 1)
    normalized_social_media = min(user_input["social_media_hours"] / 8, 1)
    normalized_doomscrolling = min(user_input["doomscrolling_duration"] / 4, 1)
    normalized_late_night = min(user_input["late_night_device_usage"] / 7, 1)
    normalized_distraction = min(user_input["distraction_frequency"] / 10, 1)
    normalized_low_concentration = 1 - min(user_input["concentration_score"] / 10, 1)
    normalized_low_motivation = 1 - min(user_input["motivation_level"] / 10, 1)
    normalized_low_sleep_hours = 1 - min(user_input["sleep_hours"] / 8, 1)
    normalized_low_sleep_quality = 1 - min(user_input["sleep_quality"] / 10, 1)

    # Tính trung bình có trọng số các chỉ số rủi ro
    weighted_burnout_index = np.mean([
        normalized_screen_time,
        normalized_social_media,
        normalized_doomscrolling,
        normalized_late_night,
        normalized_distraction,
        normalized_low_concentration,
        normalized_low_motivation,
        normalized_low_sleep_hours,
        normalized_low_sleep_quality,
    ])

    # Quy đổi sang thang điểm 0 - 5
    digital_burnout_score = round(weighted_burnout_index * 5, 2)
    return digital_burnout_score


# ------------------------------------------------------------------------------
# 8. HÀM XÁC ĐỊNH DBI LEVEL TỪ DIGITAL BURNOUT SCORE
# ------------------------------------------------------------------------------

# Mục tiêu: Phân loại mức độ burnout dựa trên điểm số tổng quát.
# Nội dung: Áp dụng ngưỡng cố định trên thang điểm 0 - 5.
# Input: Điểm số digital_burnout_score.
# Output: Nhãn mức độ (Nguy cơ thấp / trung bình / cao).

def determine_dbi_level(digital_burnout_score):
    if digital_burnout_score < 2:
        dbi_level = "Nguy cơ thấp"
    elif digital_burnout_score < 3.5:
        dbi_level = "Nguy cơ trung bình"
    else:
        dbi_level = "Nguy cơ cao"
    return dbi_level


# ------------------------------------------------------------------------------
# 9. HÀM XÁC ĐỊNH CÁC YẾU TỐ NGUY CƠ CHÍNH
# ------------------------------------------------------------------------------

# Mục tiêu: Liệt kê các yếu tố hành vi đang ở mức đáng chú ý.
# Nội dung: So sánh giá trị khảo sát của người dùng với ngưỡng tham chiếu.
# Input: Dictionary chứa giá trị các feature khảo sát.
# Output: Danh sách chuỗi mô tả các yếu tố nguy cơ.

def identify_risk_factors(user_input):
    risk_factor_list = []

    if user_input["daily_screen_time"] >= 8:
        risk_factor_list.append("Thời gian sử dụng thiết bị số hàng ngày ở mức cao.")

    if user_input["doomscrolling_duration"] >= 2:
        risk_factor_list.append("Thời gian lướt mạng xã hội không mục đích khá nhiều.")

    if user_input["late_night_device_usage"] >= 4:
        risk_factor_list.append("Tần suất sử dụng thiết bị vào ban đêm cao, ảnh hưởng đến giấc ngủ.")

    if user_input["notification_count"] >= 80:
        risk_factor_list.append("Số lượng thông báo nhận được mỗi ngày quá nhiều.")

    if user_input["distraction_frequency"] >= 7:
        risk_factor_list.append("Tần suất mất tập trung trong học tập ở mức cao.")

    if user_input["concentration_score"] <= 4:
        risk_factor_list.append("Khả năng tập trung khi học tập còn hạn chế.")

    if user_input["sleep_hours"] < 6:
        risk_factor_list.append("Thời gian ngủ mỗi ngày chưa đủ khuyến nghị.")

    if user_input["sleep_quality"] <= 4:
        risk_factor_list.append("Chất lượng giấc ngủ ở mức thấp.")

    if user_input["motivation_level"] <= 4:
        risk_factor_list.append("Mức độ động lực học tập đang suy giảm.")

    if not risk_factor_list:
        risk_factor_list.append("Chưa phát hiện yếu tố nguy cơ đáng chú ý.")

    return risk_factor_list


# ------------------------------------------------------------------------------
# 10. HÀM SINH KHUYẾN NGHỊ CÁ NHÂN HÓA (RULE-BASED)
# ------------------------------------------------------------------------------

# Mục tiêu: Đưa ra khuyến nghị phù hợp với từng nhóm hành vi của người dùng.
# Nội dung: Áp dụng tập luật (rule-based) dựa trên ngưỡng của từng feature.
# Input: Dictionary chứa giá trị các feature khảo sát.
# Output: Danh sách khuyến nghị dạng chuỗi tiếng Việt.

def generate_recommendations(user_input):
    recommendation_list = []

    if user_input["daily_screen_time"] >= 8:
        recommendation_list.append("Giảm thời gian sử dụng thiết bị ngoài mục đích học tập.")

    if user_input["social_media_hours"] >= 4:
        recommendation_list.append("Đặt giới hạn thời gian sử dụng mạng xã hội mỗi ngày.")

    if user_input["doomscrolling_duration"] >= 2:
        recommendation_list.append("Giới hạn thời gian lướt mạng xã hội không mục đích.")

    if user_input["late_night_device_usage"] >= 4:
        recommendation_list.append("Hạn chế sử dụng thiết bị điện tử sau 23 giờ.")

    if user_input["sleep_hours"] < 6:
        recommendation_list.append("Cố gắng ngủ đủ từ 7 đến 8 giờ mỗi ngày.")

    if user_input["sleep_quality"] <= 4:
        recommendation_list.append("Cải thiện thói quen ngủ và hạn chế sử dụng thiết bị trước khi ngủ.")

    if user_input["concentration_score"] <= 4 or user_input["distraction_frequency"] >= 7:
        recommendation_list.append("Áp dụng kỹ thuật học tập tập trung như Pomodoro để cải thiện khả năng tập trung.")

    if user_input["deep_work_hours"] < 2:
        recommendation_list.append("Dành thêm thời gian cho các phiên học tập sâu, không bị gián đoạn.")

    if user_input["motivation_level"] <= 4:
        recommendation_list.append("Đặt mục tiêu học tập nhỏ, cụ thể để duy trì động lực.")

    if user_input["notification_count"] >= 80:
        recommendation_list.append("Tắt bớt thông báo không cần thiết trên thiết bị di động.")

    if not recommendation_list:
        recommendation_list.append("Duy trì thói quen sử dụng thiết bị số và học tập hiện tại.")

    return recommendation_list


# ------------------------------------------------------------------------------
# 11. KHỞI TẠO SESSION STATE
# ------------------------------------------------------------------------------

# Mục tiêu: Lưu trữ kết quả khảo sát và dự đoán giữa các lần tương tác.
# Nội dung: Sử dụng st.session_state để giữ dữ liệu khi chuyển trang.
# Input: Không có.
# Output: Các biến session_state được khởi tạo với giá trị mặc định.

if "assessment_completed" not in st.session_state:
    st.session_state.assessment_completed = False

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

if "user_input" not in st.session_state:
    st.session_state.user_input = {}

if "assessment_result" not in st.session_state:
    st.session_state.assessment_result = {}


# ------------------------------------------------------------------------------
# 12. SIDEBAR NAVIGATION
# ------------------------------------------------------------------------------

st.sidebar.title("Digital Burnout Assessment")
st.sidebar.markdown("Hệ thống hỗ trợ đánh giá tình trạng quá tải kỹ thuật số của sinh viên.")

page_selection = st.sidebar.radio(
    "Chọn trang",
    ["Digital Burnout Assessment", "Result Dashboard"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("Prototype demo, chỉ phục vụ mục đích minh họa.")


# ------------------------------------------------------------------------------
# 13. TRANG 1: DIGITAL BURNOUT ASSESSMENT
# ------------------------------------------------------------------------------

def render_assessment_page():
    # Mục tiêu: Thu thập thông tin cá nhân và câu trả lời khảo sát từ sinh viên.
    # Nội dung: Form được chia thành bốn nhóm câu hỏi thân thiện, không dùng thuật ngữ kỹ thuật.
    # Input: Thao tác nhập liệu của người dùng trên giao diện Streamlit.
    # Output: Cập nhật session_state với thông tin cá nhân và dữ liệu khảo sát.

    st.title("Digital Burnout Assessment")
    st.markdown(
        "Khảo sát này giúp đánh giá mức độ quá tải kỹ thuật số dựa trên thói quen "
        "sử dụng thiết bị và hiệu suất học tập của bạn. Vui lòng trả lời trung thực "
        "theo tình trạng thực tế trong hai tuần gần đây."
    )

    with st.form("digital_burnout_survey_form"):

        # ---------------- Nhóm 1: Thông tin cá nhân ----------------
        st.subheader("1. Thông tin cá nhân")

        col_profile_1, col_profile_2 = st.columns(2)

        with col_profile_1:
            gender = st.selectbox("Giới tính", ["Nữ", "Nam", "Khác"])
            birth_year = st.number_input("Năm sinh", min_value=1990, max_value=2012, value=2003, step=1)
            education_stage = st.selectbox(
                "Bậc học",
                ["Trung học phổ thông", "Đại học năm 1-2", "Đại học năm 3-4", "Sau đại học"]
            )

        with col_profile_2:
            work_mode = st.selectbox("Hình thức học tập/làm việc", ["Trực tiếp", "Trực tuyến", "Kết hợp"])
            device_usage_type = st.selectbox(
                "Mục đích sử dụng thiết bị chủ yếu",
                ["Học tập", "Giải trí", "Kết hợp học tập và giải trí"]
            )

        # ---------------- Nhóm 2: Digital Exposure ----------------
        st.subheader("2. Thói quen sử dụng thiết bị số")

        daily_screen_time = st.slider(
            "Bạn sử dụng thiết bị số trung bình bao nhiêu giờ mỗi ngày?",
            min_value=0.0, max_value=16.0, value=6.0, step=0.5
        )

        social_media_hours = st.slider(
            "Bạn dành bao nhiêu giờ mỗi ngày cho mạng xã hội?",
            min_value=0.0, max_value=12.0, value=3.0, step=0.5
        )

        doomscrolling_duration = st.slider(
            "Bạn dành bao nhiêu giờ mỗi ngày để lướt mạng xã hội một cách vô định, không mục đích cụ thể?",
            min_value=0.0, max_value=6.0, value=1.0, step=0.5
        )

        late_night_device_usage = st.slider(
            "Trong một tuần, bạn sử dụng thiết bị sau 23 giờ đêm bao nhiêu ngày?",
            min_value=0, max_value=7, value=2, step=1
        )

        notification_count = st.slider(
            "Trung bình mỗi ngày bạn nhận được khoảng bao nhiêu thông báo trên thiết bị?",
            min_value=0, max_value=200, value=50, step=5
        )

        smartphone_unlocks = st.slider(
            "Trung bình mỗi ngày bạn mở khóa điện thoại khoảng bao nhiêu lần?",
            min_value=0, max_value=150, value=40, step=5
        )

        app_switch_frequency = st.slider(
            "Bạn có thường xuyên chuyển đổi qua lại giữa nhiều ứng dụng khi đang học tập không?",
            min_value=1, max_value=10, value=5, step=1,
            help="1 là hiếm khi, 10 là liên tục chuyển đổi ứng dụng."
        )

        # ---------------- Nhóm 3: Cognitive Performance ----------------
        st.subheader("3. Hiệu suất học tập và khả năng tập trung")

        concentration_score = st.slider(
            "Khả năng tập trung của bạn trong quá trình học tập như thế nào?",
            min_value=1, max_value=10, value=6, step=1,
            help="1 là rất kém, 10 là rất tốt."
        )

        distraction_frequency = st.slider(
            "Bạn có thường xuyên bị phân tâm khi đang học tập không?",
            min_value=1, max_value=10, value=5, step=1,
            help="1 là hiếm khi, 10 là rất thường xuyên."
        )

        focus_sessions = st.slider(
            "Trung bình mỗi ngày bạn có bao nhiêu phiên học tập tập trung, không bị gián đoạn?",
            min_value=0, max_value=10, value=2, step=1
        )

        deep_work_hours = st.slider(
            "Bạn dành bao nhiêu giờ mỗi ngày để học tập sâu, không bị gián đoạn bởi thiết bị số?",
            min_value=0.0, max_value=8.0, value=2.0, step=0.5
        )

        task_completion_rate = st.slider(
            "Bạn hoàn thành khoảng bao nhiêu phần trăm nhiệm vụ học tập đã đặt ra?",
            min_value=0, max_value=100, value=70, step=5
        )

        motivation_level = st.slider(
            "Mức độ động lực học tập của bạn hiện tại như thế nào?",
            min_value=1, max_value=10, value=6, step=1,
            help="1 là rất thấp, 10 là rất cao."
        )

        # ---------------- Nhóm 4: Sleep and Recovery ----------------
        st.subheader("4. Giấc ngủ và khả năng phục hồi")

        sleep_hours = st.slider(
            "Bạn ngủ trung bình bao nhiêu giờ mỗi ngày?",
            min_value=0.0, max_value=12.0, value=6.5, step=0.5
        )

        sleep_quality = st.slider(
            "Bạn đánh giá chất lượng giấc ngủ của mình như thế nào?",
            min_value=1, max_value=10, value=6, step=1,
            help="1 là rất kém, 10 là rất tốt."
        )

        submit_button = st.form_submit_button("Xem kết quả đánh giá")

    # Xử lý sau khi người dùng bấm nút submit
    if submit_button:
        # Lưu thông tin cá nhân, chỉ dùng để hiển thị, không đưa vào mô hình
        user_profile = {
            "gender": gender,
            "birth_year": birth_year,
            "education_stage": education_stage,
            "work_mode": work_mode,
            "device_usage_type": device_usage_type,
        }

        # Lưu giá trị khảo sát dùng làm feature đầu vào cho mô hình
        user_input = {
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
            "motivation_level": motivation_level,
            "sleep_hours": sleep_hours,
            "sleep_quality": sleep_quality,
        }

        # Xây dựng DataFrame đầu vào cho mô hình
        model_input_df = build_model_input(user_input)

        # Thực hiện dự đoán bằng Voting Classifier
        predicted_label, confidence_score, predicted_proba = predict_digital_burnout(model_input_df)

        # Tính điểm digital_burnout_score và mức độ DBI
        digital_burnout_score = calculate_digital_burnout_score(user_input)
        dbi_level = determine_dbi_level(digital_burnout_score)

        # Xác định yếu tố nguy cơ và khuyến nghị
        risk_factor_list = identify_risk_factors(user_input)
        recommendation_list = generate_recommendations(user_input)

        # Lưu toàn bộ kết quả vào session_state
        st.session_state.user_profile = user_profile
        st.session_state.user_input = user_input
        st.session_state.assessment_result = {
            "predicted_label": predicted_label,
            "confidence_score": confidence_score,
            "predicted_proba": predicted_proba,
            "digital_burnout_score": digital_burnout_score,
            "dbi_level": dbi_level,
            "risk_factor_list": risk_factor_list,
            "recommendation_list": recommendation_list,
        }
        st.session_state.assessment_completed = True

        st.success("Đã hoàn thành khảo sát. Vui lòng chuyển sang trang Result Dashboard để xem kết quả chi tiết.")


# ------------------------------------------------------------------------------
# 14. TRANG 2: RESULT DASHBOARD
# ------------------------------------------------------------------------------

def render_result_dashboard_page():
    # Mục tiêu: Trình bày toàn bộ kết quả đánh giá Digital Burnout cho sinh viên.
    # Nội dung: Hiển thị điểm số, mức độ, dự đoán AI, yếu tố nguy cơ và khuyến nghị.
    # Input: Dữ liệu đã được lưu trong session_state từ trang khảo sát.
    # Output: Giao diện trực quan hiển thị kết quả theo thứ tự yêu cầu.

    st.title("Result Dashboard")

    if not st.session_state.assessment_completed:
        st.info("Bạn chưa hoàn thành khảo sát. Vui lòng quay lại trang Digital Burnout Assessment để thực hiện.")
        return

    user_profile = st.session_state.user_profile
    assessment_result = st.session_state.assessment_result

    # Hiển thị thông tin người dùng
    st.subheader("Thông tin sinh viên")
    profile_col_1, profile_col_2, profile_col_3 = st.columns(3)
    profile_col_1.markdown(f"Giới tính: {user_profile['gender']}")
    profile_col_1.markdown(f"Năm sinh: {user_profile['birth_year']}")
    profile_col_2.markdown(f"Bậc học: {user_profile['education_stage']}")
    profile_col_2.markdown(f"Hình thức học tập: {user_profile['work_mode']}")
    profile_col_3.markdown(f"Mục đích sử dụng thiết bị: {user_profile['device_usage_type']}")

    st.markdown("---")

    # ---------------- 1. Digital Burnout Score ----------------
    st.subheader("1. Digital Burnout Score")
    digital_burnout_score = assessment_result["digital_burnout_score"]
    st.metric(label="Digital Burnout Score", value=f"{digital_burnout_score} / 5")
    st.progress(min(digital_burnout_score / 5, 1.0))

    st.markdown("---")

    # ---------------- 2. DBI Level ----------------
    st.subheader("2. Mức độ Digital Burnout Index (DBI)")
    st.markdown(f"Mức độ: **{assessment_result['dbi_level']}**")

    st.markdown("---")

    # ---------------- 3. AI Prediction ----------------
    st.subheader("3. Dự đoán từ mô hình AI")

    if assessment_result["predicted_label"] is None:
        st.warning(
            "Không tìm thấy file mô hình tại models/vietnam_dataset/best_model.joblib. "
            "Vui lòng kiểm tra lại đường dẫn model."
        )
    else:
        predicted_label = assessment_result["predicted_label"]
        confidence_score = assessment_result["confidence_score"]

        st.markdown(f"Dự đoán AI (Voting Classifier): **{predicted_label}**")
        st.markdown(f"Độ tin cậy: **{confidence_score:.0f}%**")

        # Vẽ biểu đồ phân phối xác suất theo từng mức độ nguy cơ
        predicted_proba = assessment_result["predicted_proba"]
        class_labels_english = ["Low", "High", "Moderate"]

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(class_labels_english, predicted_proba, color=["#4CAF50", "#E53935", "#FB8C00"])
        ax.set_title("Digital Burnout Risk Probability Distribution")
        ax.set_xlabel("Risk Level")
        ax.set_ylabel("Probability")
        ax.set_ylim(0, 1)
        st.pyplot(fig)

    st.markdown("---")

    # ---------------- 4. Risk Factors ----------------
    st.subheader("4. Các yếu tố cần chú ý")
    for risk_factor in assessment_result["risk_factor_list"]:
        st.markdown(f"- {risk_factor}")

    st.markdown("---")

    # ---------------- 5. Recommendations ----------------
    st.subheader("5. Khuyến nghị cá nhân hóa")
    for recommendation in assessment_result["recommendation_list"]:
        st.markdown(f"- {recommendation}")


# ------------------------------------------------------------------------------
# 15. ĐIỀU HƯỚNG GIỮA CÁC TRANG
# ------------------------------------------------------------------------------

if page_selection == "Digital Burnout Assessment":
    render_assessment_page()
elif page_selection == "Result Dashboard":
    render_result_dashboard_page()