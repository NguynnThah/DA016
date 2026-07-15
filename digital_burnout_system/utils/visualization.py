import matplotlib.pyplot as plt

# Tạo biểu đồ thể hiện điểm số các khía cạnh thuộc DBI Framework
def create_dbi_dimension_chart(dbi_results):
    categories = [
        'Digital Exposure', 
        'Psychological Symptoms', 
        'Cognitive Performance', 
        'Sleep Recovery'
    ]
    scores = [
        dbi_results["digital_exposure_score"],
        dbi_results["psychological_symptoms_score"],
        dbi_results["cognitive_performance_score"],
        dbi_results["sleep_and_recovery_score"]
    ]

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(categories, scores, color='#2b5c8f')
    
    # Thiết lập tiêu đề và nhãn giới hạn trục cho biểu đồ
    ax.set_title('DBI Dimension Breakdown')
    ax.set_ylabel('Score (0-100)')
    ax.set_ylim(0, 100)
    
    # Hiển thị số liệu trực tiếp trên đầu mỗi cột
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f"{yval:.1f}", ha='center', va='bottom')
        
    plt.xticks(rotation=15)
    plt.tight_layout()
    print("Đã vẽ biểu đồ các khía cạnh DBI thành công.")
    return fig

# Tạo biểu đồ thể hiện mức độ phần trăm rủi ro từ mô hình Machine Learning
def create_risk_chart(probability):
    labels = ['Burnout Risk', 'Safe Status']
    sizes = [probability * 100, (1 - probability) * 100]
    colors = ['#d9534f', '#5cb85c']

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')
    
    # Thiết lập tiêu đề cho biểu đồ hình quạt
    ax.set_title('Machine Learning Risk Probability')
    plt.tight_layout()
    print("Đã vẽ biểu đồ rủi ro Machine Learning thành công.")
    return fig