import os
import joblib
import pandas as pd
import streamlit as st

# Tải mô hình Machine Learning đã được huấn luyện với cơ chế lưu bộ nhớ đệm
@st.cache_resource
def load_model():
    model_path = os.path.join("models", "best_model.joblib")
    if not os.path.exists(model_path):
        print("Không tìm thấy file mô hình tại đường dẫn đã chỉ định.")
        return None
    try:
        model = joblib.load(model_path)
        print("Đã tải mô hình thành công.")
        return model
    except Exception as e:
        print(f"Lỗi khi tải mô hình: {str(e)}")
        return None

# Dự đoán nguy cơ kiệt sức kỹ thuật số dựa trên dữ liệu đầu vào
def predict_burnout(input_data):
    model = load_model()
    if model is None:
        return None, None

    # Khởi tạo danh sách 26 thuộc tính yêu cầu theo đúng thứ tự của mô hình
    feature_order = [
        'emotional_exhaustion', 'stress_level', 'daily_screen_time', 'work_satisfaction',
        'doomscrolling_duration', 'distraction_frequency', 'sleep_hours', 'notification_count',
        'physical_activity', 'deep_work_hours', 'late_night_device_usage', 'focus_sessions',
        'app_switch_frequency', 'smartphone_unlocks', 'social_media_hours', 'task_completion_rate',
        'meeting_hours', 'age', 'concentration_score', 'mental_fatigue',
        'sleep_quality', 'motivation_level', 'workspace_quality', 'internet_stability',
        'caffeine_intake', 'remote_work_days'
    ]

    # Chuyển đổi dữ liệu sang dạng DataFrame với đúng thứ tự cột
    df_input = pd.DataFrame([input_data])
    df_model = df_input[feature_order]

    # Thực hiện dự đoán nhãn và xác suất rủi ro
    try:
        prediction = model.predict(df_model)[0]
        prediction_probability = model.predict_proba(df_model)[0][1]
        print("Đã thực hiện dự đoán thành công.")
        return prediction, prediction_probability
    except Exception as e:
        print(f"Lỗi trong quá trình dự đoán: {str(e)}")
        return None, None