import numpy as np

# Tính toán các chỉ số thành phần và tổng điểm số kiệt sức kỹ thuật số
def calculate_dbi_metrics(raw_data):
    # Tính toán điểm số cho khía cạnh tiếp xúc kỹ thuật số
    # Chuẩn hóa các thang đo về cùng hệ điểm để tính trung bình
    digital_exposure_score = float(np.mean([
        raw_data['daily_screen_time'] * 20,          # Giả định thang ban đầu tối đa 5 giờ
        raw_data['social_media_hours'] * 20,         # Giả định thang ban đầu tối đa 5 giờ
        raw_data['doomscrolling_duration'] * 25,     # Giả định thang ban đầu tối đa 4 giờ
        raw_data['late_night_device_usage'] * 20,    # Giả định thang ban đầu tối đa 5 giờ
        (raw_data['notification_count'] / 200) * 100 if raw_data['notification_count'] <= 200 else 100,
        (raw_data['smartphone_unlocks'] / 100) * 100 if raw_data['smartphone_unlocks'] <= 100 else 100,
        raw_data['app_switch_frequency'] * 10
    ]))

    # Tính toán điểm số cho các triệu chứng tâm lý
    psychological_symptoms_score = float(np.mean([
        raw_data['emotional_exhaustion'] * 10,
        raw_data['stress_level'] * 10,
        raw_data['mental_fatigue'] * 10,
        (10 - raw_data['motivation_level']) * 10     # Đảo ngược điểm vì động lực cao thì kiệt sức thấp
    ]))

    # Tính toán điểm số cho khía cạnh hiệu suất nhận thức
    cognitive_performance_score = float(np.mean([
        (10 - raw_data['concentration_score']) * 10, # Đảo ngược điểm tập trung
        raw_data['distraction_frequency'] * 10,
        (10 - raw_data['focus_sessions']) * 10,      # Đảo ngược số phiên tập trung
        (10 - raw_data['deep_work_hours']) * 10,     # Đảo ngược giờ làm việc sâu
        (100 - raw_data['task_completion_rate'])     # Đảo ngược tỷ lệ hoàn thành công việc
    ]))

    # Tính toán điểm số cho giấc ngủ và phục hồi
    sleep_and_recovery_score = float(np.mean([
        (12 - raw_data['sleep_hours']) * 8.33 if raw_data['sleep_hours'] <= 12 else 0, # Giả định tối ưu là ngủ đủ giấc
        (10 - raw_data['sleep_quality']) * 10        # Đảo ngược chất lượng giấc ngủ
    ]))

    # Tính toán tổng điểm kiệt sức kỹ thuật số dựa trên trung bình bốn khía cạnh chính
    digital_burnout_score = float(np.mean([
        digital_exposure_score,
        psychological_symptoms_score,
        cognitive_performance_score,
        sleep_and_recovery_score
    ]))

    # Phân loại mức độ kiệt sức dựa trên tổng điểm thu được
    if digital_burnout_score < 30:
        dbi_level = "Thấp"
    elif digital_burnout_score < 60:
        dbi_level = "Trung bình"
    elif digital_burnout_score < 80:
        dbi_level = "Cao"
    else:
        dbi_level = "Rất cao"

    print("Đã hoàn thành việc tính toán điểm số DBI.")
    return {
        "digital_exposure_score": round(digital_exposure_score, 2),
        "psychological_symptoms_score": round(psychological_symptoms_score, 2),
        "cognitive_performance_score": round(cognitive_performance_score, 2),
        "sleep_and_recovery_score": round(sleep_and_recovery_score, 2),
        "digital_burnout_score": round(digital_burnout_score, 2),
        "dbi_level": dbi_level
    }