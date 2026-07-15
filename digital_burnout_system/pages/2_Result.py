import streamlit as st
from utils.recommendation import get_personalized_recommendations
from utils.visualization import create_dbi_dimension_chart, create_risk_chart

# Cấu hình giao diện trang kết quả phân tích
st.set_page_config(page_title="Assessment Results", layout="wide")

st.title("Kết quả phân tích kiệt sức kỹ thuật số")

# Kiểm tra dữ liệu khảo sát trong bộ nhớ phiên làm việc
if "user_input" not in st.session_state:
    st.warning("Vui lòng hoàn thành bài khảo sát tại trang Assessment trước khi xem kết quả phân tích.")
else:
    # Lấy thông tin đã tính toán từ session state
    dbi_results = st.session_state["dbi_results"]
    prediction = st.session_state["ml_prediction"]
    probability = st.session_state["ml_probability"]

    # Hiển thị phần kết quả tổng quan theo khung khảo sát Việt Nam
    st.subheader("Kết quả đánh giá DBI")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Digital Burnout Score (Điểm số kiệt sức)", value=f"{dbi_results['digital_burnout_score']} / 100")
    with col2:
        st.metric(label="DBI Level (Mức độ kiệt sức)", value=dbi_results['dbi_level'])

    # Hiển thị chi tiết điểm số của bốn khía cạnh cốt lõi
    st.subheader("Phân tích chi tiết các khía cạnh thành phần")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(label="Digital Exposure", value=f"{dbi_results['digital_exposure_score']} / 100")
    c2.metric(label="Psychological Symptoms", value=f"{dbi_results['psychological_symptoms_score']} / 100")
    c3.metric(label="Cognitive Performance", value=f"{dbi_results['cognitive_performance_score']} / 100")
    c4.metric(label="Sleep Recovery", value=f"{dbi_results['sleep_and_recovery_score']} / 100")

    # Hiển thị phần dự đoán rủi ro của mô hình học máy
    st.subheader("Dự đoán từ mô hình Machine Learning")
    if prediction is not None:
        risk_status = "Nguy cơ cao" if prediction == 1 else "An toàn"
        col_ml1, col_ml2 = st.columns(2)
        with col_ml1:
            st.metric(label="Mức độ rủi ro kiệt sức dự đoán", value=risk_status)
        with col_ml2:
            st.metric(label="Xác suất xảy ra rủi ro kiệt sức", value=f"{probability * 100:.1f}%")
    else:
        st.info("Mô hình Machine Learning hiện tại chưa được tải hoặc cấu hình chưa sẵn sàng.")

    # Hiển thị khu vực đồ thị trực quan hóa dữ liệu
    st.subheader("Đồ thị trực quan hóa dữ liệu")
    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        fig_dbi = create_dbi_dimension_chart(dbi_results)
        st.pyplot(fig_dbi)
    with fig_col2:
        if probability is not None:
            fig_risk = create_risk_chart(probability)
            st.pyplot(fig_risk)

    # Hiển thị các khuyến nghị hành vi cá nhân hóa tương ứng với kết quả điểm số
    st.subheader("Đề xuất giải pháp khắc phục cá nhân hóa")
    recommendations = get_personalized_recommendations(dbi_results)
    for idx, rec in enumerate(recommendations, 1):
        st.write(f"{idx}. {rec}")