import streamlit as st

# Thiết lập cấu hình trang hiển thị
st.set_page_config(
    page_title="Digital Burnout Assessment System",
    layout="wide"
)

# Tiêu đề chính của ứng dụng
st.title("Hệ thống đánh giá kiệt sức kỹ thuật số ở sinh viên Việt Nam")

# Giới thiệu tổng quan về hệ thống và mục tiêu
st.subheader("Giới thiệu hệ thống")
st.write(
    "Hệ thống giúp sinh viên Việt Nam tự đánh giá mức độ kiệt sức kỹ thuật số của bản thân. "
    "Ứng dụng kết hợp giữa Khung đánh giá DBI (Digital Burnout Index) xây dựng dựa trên dữ liệu khảo sát tại Việt Nam "
    "và mô hình Machine Learning được huấn luyện để dự đoán mức độ rủi ro kiệt sức dựa trên các chỉ số hành vi, tâm lý."
)

# Mô tả các chức năng chính của hệ thống
st.subheader("Các chức năng chính")
st.write(
    "1. Khảo sát đánh giá: Sinh viên cung cấp thông tin về thói quen sử dụng thiết bị, hiệu suất nhận thức, "
    "chất lượng giấc ngủ và các triệu chứng tâm lý cá nhân.\n"
    "2. Phân tích đa chiều: Hệ thống tính toán điểm số cụ thể cho từng khía cạnh như mức độ tiếp xúc kỹ thuật số, "
    "triệu chứng tâm lý, hiệu suất nhận thức và khả năng phục hồi giấc ngủ.\n"
    "3. Dự đoán từ Machine Learning: Đưa ra cảnh báo nguy cơ kiệt sức kỹ thuật số bằng mô hình học máy chuyên sâu.\n"
    "4. Đề xuất giải pháp: Cung cấp các khuyến nghị cá nhân hóa nhằm cải thiện sức khỏe tinh thần và tối ưu hóa thói quen công nghệ."
)

# Hướng dẫn người dùng di chuyển sang trang làm bài khảo sát
st.subheader("Hướng dẫn sử dụng")
st.write("Vui lòng chọn mục Assessment ở thanh điều hướng bên cạnh để bắt đầu bài đánh giá tình trạng của bạn.")