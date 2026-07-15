# Import thư viện cần thiết

import joblib



# Load mô hình Machine Learning

model = joblib.load(
    "models/best_model.joblib"
)



# Hiển thị thông tin mô hình

print("Đã tải mô hình thành công.")

print(model)