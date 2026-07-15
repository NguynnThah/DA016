# Import thư viện Streamlit

import streamlit as st



# Cấu hình thông tin hiển thị của ứng dụng

st.set_page_config(
    page_title="Digital Burnout Assessment System",
    layout="wide"
)



# Hiển thị tiêu đề chính của hệ thống

st.title(
    "Digital Burnout Assessment System"
)



# Hiển thị mô tả tổng quan hệ thống

st.write(
    """
    Hệ thống đánh giá Digital Burnout dành cho sinh viên Việt Nam.

    Hệ thống kết hợp hai thành phần:

    - Digital Burnout Indicator (DBI):
      Đánh giá mức độ Digital Burnout dựa trên bộ chỉ số được xây dựng
      từ dữ liệu khảo sát sinh viên Việt Nam.

    - Machine Learning Model:
      Dự đoán nguy cơ Digital Burnout bằng mô hình được huấn luyện
      trên bộ dữ liệu quốc tế.
    """
)



# Tạo bố cục giới thiệu các chức năng chính

first_column, second_column, third_column = st.columns(3)



# Hiển thị chức năng đánh giá dữ liệu đầu vào

with first_column:

    st.subheader(
        "Student Assessment"
    )

    st.write(
        """
        Thu thập thông tin về:

        - Hành vi sử dụng thiết bị
        - Thói quen học tập
        - Giấc ngủ
        - Trạng thái burnout
        """
    )



# Hiển thị chức năng tính toán DBI

with second_column:

    st.subheader(
        "DBI Analysis"
    )

    st.write(
        """
        Hệ thống tính toán:

        - Digital Burnout Score
        - Burnout Level
        - Các nhóm chỉ số rủi ro
        """
    )



# Hiển thị chức năng dự đoán Machine Learning

with third_column:

    st.subheader(
        "Machine Learning Prediction"
    )

    st.write(
        """
        Mô hình dự đoán:

        - Burnout Risk
        - Prediction Probability
        """
    )



# Hiển thị hướng dẫn sử dụng hệ thống

st.subheader(
    "Hướng dẫn sử dụng"
)


st.write(
    """
    1. Truy cập trang Assessment để nhập thông tin cá nhân.

    2. Hệ thống xử lý dữ liệu đầu vào thông qua:
       - DBI Assessment Framework.
       - Machine Learning Model.

    3. Kết quả bao gồm:
       - Digital Burnout Score.
       - Risk Level.
       - Burnout Prediction.
       - Recommendation.
    """
)