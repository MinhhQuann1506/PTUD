# 🎯 Face Recognition & People Tracking System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green.svg)](https://opencv.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-red.svg)](https://flask.palletsprojects.com/)

Hệ thống nhận diện khuôn mặt và theo dõi người tự động với khả năng chấm công thời gian thực, được xây dựng bằng Python, OpenCV, YOLOv8, DeepSORT và Flask.

## 📋 Mục lục

- [Tính năng](#-tính-năng)
- [Công nghệ sử dụng](#-công-nghệ-sử-dụng)
- [Cài đặt](#-cài-đặt)
- [Sử dụng](#-sử-dụng)
- [API Documentation](#-api-documentation)
- [Cấu trúc Project](#-cấu-trúc-project)
- [Cấu hình](#-cấu-hình)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## ✨ Tính năng

### 🎭 Nhận diện khuôn mặt
- **Face Recognition** với nhiều phương pháp:
  - Facenet-PyTorch (512D embeddings) - độ chính xác cao
  - Histogram-based encoding (fallback) - không cần GPU
- **Tự động phát hiện** với nhiều tham số tối ưu
- **Xử lý ảnh nâng cao**: CLAHE, resize tự động
- **Hỗ trợ đăng ký** qua web dashboard hoặc script

### 👥 Tracking người
- **YOLOv8** để phát hiện người
- **DeepSORT** để tracking đa đối tượng
- **Theo dõi liên tục** qua nhiều frame
- **Tự động cập nhật** danh tính khi nhận diện được

### ⏰ Chấm công tự động
- **Tự động ghi nhận** time_in/time_out
- **Theo dõi thời gian hiện diện** real-time
- **Hỗ trợ nhiều người** đồng thời
- **Timeout tự động** khi người rời khỏi

### 📊 Web Dashboard
- **Dashboard real-time** với Flask
- **Thống kê trực quan**: active people, attendance history
- **Đăng ký người mới** qua web interface
- **Xuất dữ liệu**: JSON, CSV, Excel
- **API RESTful** đầy đủ

## 🛠️ Công nghệ sử dụng

### Core AI/ML
- **OpenCV** - Xử lý ảnh và phát hiện khuôn mặt
- **YOLOv8** (Ultralytics) - Phát hiện người
- **DeepSORT** - Tracking đa đối tượng
- **Facenet-PyTorch** - Face embeddings (optional)

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - ORM database
- **SQLite** - Database

### Frontend
- **HTML/CSS/JavaScript** - Dashboard interface

## 📦 Cài đặt

### Yêu cầu hệ thống
- Python 3.8+
- Webcam hoặc camera
- Windows/Linux/macOS

### Bước 1: Clone repository
```bash
git clone https://github.com/MinhhQuann1506/PTUD.git
cd PTUD
```

### Bước 2: Tạo môi trường ảo (khuyến nghị)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 4: Cài đặt PyTorch và Facenet (Tùy chọn - để tăng độ chính xác)
```bash
# CPU only
pip install torch torchvision
pip install facenet-pytorch

# GPU (CUDA 11.7)
pip install torch --index-url https://download.pytorch.org/whl/cu117
pip install facenet-pytorch
```

### Bước 5: Tải YOLOv8 model
Model sẽ được tải tự động khi chạy lần đầu. Hoặc tải thủ công:
```bash
# Model sẽ được tải tự động từ ultralytics
# File: yolov8n.pt
```

## 🚀 Sử dụng

### Chạy hệ thống đầy đủ (Camera + API)
```bash
python main.py
```
- Camera window sẽ hiển thị video với nhận diện và tracking
- API server chạy tại: `http://localhost:5000`
- Dashboard: `http://localhost:5000`

### Chỉ chạy Camera
```bash
python run_camera.py
```

### Chỉ chạy API Dashboard
```bash
python main.py
# Chọn option 2 trong menu
```

### Phím tắt Camera
- **`q`**: Thoát
- **`r`**: Reset tracking
- **`l`**: Reload face encodings
- **`i`**: Toggle check-in checkbox
- **`o`**: Toggle check-out checkbox
- **`c`**: Xác nhận hành động (check-in/check-out)

## 📝 Đăng ký người mới

### Cách 1: Web Dashboard (Khuyến nghị)
1. Mở `http://localhost:5000`
2. Cuộn xuống phần "Đăng ký người mới"
3. Nhập tên và upload tối đa 3 ảnh
4. Nhấn "Đăng ký người mới"
5. Hệ thống tự động reload face encodings

**Lưu ý về ảnh:**
- Ảnh phải có khuôn mặt rõ ràng, hướng về phía trước
- Ánh sáng đủ, không quá tối hoặc quá sáng
- Khuôn mặt chiếm phần lớn khung hình
- Tránh đeo kính râm hoặc che khuất khuôn mặt

### Cách 2: Script
```bash
# Đặt ảnh vào thư mục known_faces/ với format: Tên_1.jpg, Tên_2.jpg, Tên_3.jpg
python register_person.py
```

## 📡 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints chính

#### Thống kê
```http
GET /api/stats
```
Trả về thống kê real-time: active people, tracks, attendance stats

#### Đăng ký người mới
```http
POST /api/persons/register
Content-Type: multipart/form-data

Fields:
- name: string (required)
- images: file[] (1-3 files, required)
```

#### Lấy danh sách attendance
```http
GET /api/attendance?limit=100
```

#### Lấy danh sách người
```http
GET /api/persons
```

#### Reload face encodings
```http
POST /api/face-recognition/reload
```

#### Xuất dữ liệu attendance
```http
GET /api/export/attendance?date_from=2024-01-01&date_to=2024-12-31&format=excel
```
Formats: `json`, `csv`, `excel`

#### Realtime updates (từ camera)
```http
POST /api/realtime/update
Headers:
  X-API-KEY: <SECRET_KEY>

Body:
{
  "event": "time_in",
  "track_id": "t1",
  "person_id": 1,
  "person_name": "John"
}
```

Xem chi tiết trong `app/api/routes.py`

## 📁 Cấu trúc Project

```
PTUD/
├── main.py                      # Entry point chính
├── run_camera.py                # Script chạy camera riêng
├── register_person.py           # Đăng ký người từ ảnh
├── config.py                    # Cấu hình hệ thống
├── requirements.txt             # Python dependencies
│
├── app/                         # Core application
│   ├── api/
│   │   └── routes.py           # REST API endpoints
│   ├── models/
│   │   └── database.py        # Database models (Person, Attendance, etc.)
│   └── services/
│       ├── face_recognition.py # Face recognition service
│       ├── tracking.py         # People tracking service (YOLO + DeepSORT)
│       └── attendance.py       # Attendance management service
│
├── templates/
│   └── dashboard.html          # Web dashboard UI
│
├── known_faces/                 # Ảnh đăng ký người
│   ├── Person1_1.jpg
│   ├── Person1_2.jpg
│   └── ...
│
├── tools/                       # Công cụ quản lý
│   ├── check_camera.py         # Kiểm tra camera
│   ├── clear_database.py      # Xóa database
│   ├── force_clear_database.py # Xóa database (force)
│   ├── compute_embedding_stats.py # Phân tích face encodings
│   ├── reencode_db_faces.py    # Re-encode face encodings
│   └── reset_db_from_known_faces.py # Reset DB từ ảnh
│
├── database/
│   └── attendance.db           # SQLite database (tự động tạo)
│
└── logs/                        # Log files
```

## ⚙️ Cấu hình

Chỉnh sửa `config.py` để tùy chỉnh hệ thống:

```python
# Face Recognition
FACE_RECOGNITION_TOLERANCE = 0.4  # Ngưỡng nhận diện (0.0-1.0, càng thấp càng strict)

# Camera
CAMERA_INDEX = 0                  # Index camera (0, 1, 2...)
CAMERA_WIDTH = 640                # Độ rộng
CAMERA_HEIGHT = 480               # Độ cao
CAMERA_FPS = 30                   # FPS

# Tracking
TRACKING_CONFIDENCE_THRESHOLD = 0.5  # Ngưỡng phát hiện người
DEEPSORT_MAX_AGE = 30            # Thời gian track tồn tại (frames)

# Attendance
CHECKOUT_TIMEOUT = 10            # Timeout tự động checkout (giây)

# API
API_HOST = '0.0.0.0'            # Host
API_PORT = 5000                 # Port
```

## 🔧 Công cụ hỗ trợ

### Kiểm tra camera
```bash
python tools/check_camera.py
```

### Xóa database
```bash
# Xóa hoàn toàn
python tools/force_clear_database.py

# Reset từ ảnh trong known_faces/
python tools/reset_db_from_known_faces.py
```

### Phân tích face encodings
```bash
python tools/compute_embedding_stats.py
```

### Re-encode face encodings
```bash
python tools/reencode_db_faces.py
```

## 🐛 Troubleshooting

### Camera không mở được
```bash
# Kiểm tra camera index
python tools/check_camera.py

# Thử các index khác: 0, 1, 2...
# Sửa CAMERA_INDEX trong config.py
```

### Không nhận diện được khuôn mặt
1. **Kiểm tra ảnh đăng ký:**
   - Ảnh có khuôn mặt rõ ràng, hướng về phía trước
   - Ánh sáng đủ, không quá tối hoặc quá sáng
   - Khuôn mặt chiếm phần lớn khung hình

2. **Điều chỉnh threshold:**
   ```python
   # Trong config.py, giảm threshold để nhạy hơn
   FACE_RECOGNITION_TOLERANCE = 0.5  # hoặc 0.6
   ```

3. **Reload face encodings:**
   - Nhấn `l` trong camera window
   - Hoặc gọi API: `POST /api/face-recognition/reload`

4. **Cài đặt facenet-pytorch:**
   ```bash
   pip install torch facenet-pytorch
   ```

### Lỗi "No valid faces detected in uploaded images"
- Đảm bảo ảnh có khuôn mặt rõ ràng
- Thử với ảnh khác, góc chụp tốt hơn
- Kiểm tra log console để xem file nào lỗi

### Database lỗi
```bash
# Reset database
python tools/force_clear_database.py
```

### Encoding dimension mismatch
```bash
# Re-encode tất cả face encodings
python tools/reencode_db_faces.py
```

### YOLO model không tải được
- Kiểm tra kết nối internet (model tự động tải)
- Hoặc tải thủ công: `yolov8n.pt` từ Ultralytics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available for use.

## 👥 Authors

- **MinhhQuann1506** - *Initial work*

## 🙏 Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [DeepSORT](https://github.com/nwojke/deep_sort)
- [Facenet-PyTorch](https://github.com/timesler/facenet-pytorch)
- [OpenCV](https://opencv.org/)
- [Flask](https://flask.palletsprojects.com/)

---

⭐ Nếu project này hữu ích, hãy cho một star!
