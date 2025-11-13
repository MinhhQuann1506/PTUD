# 🎯 Face Recognition & People Tracking System

Hệ thống nhận diện khuôn mặt và theo dõi người tự động với chức năng chấm công thời gian thực.

## ✨ Tính năng

- **Nhận diện khuôn mặt**: Tự động nhận diện người đã đăng ký
- **Tracking người**: Theo dõi người trong video real-time
- **Chấm công tự động**: Ghi nhận thời gian vào/ra tự động
- **Web Dashboard**: Giao diện web để xem thống kê và quản lý

## 📦 Cài đặt

### Yêu cầu
- Python 3.8 trở lên
- Webcam hoặc camera

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

### Bước 3: Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### Bước 4: Cài đặt PyTorch và Facenet (Tùy chọn - để tăng độ chính xác)
```bash
# CPU
pip install torch torchvision
pip install facenet-pytorch

# GPU (nếu có)
pip install torch --index-url https://download.pytorch.org/whl/cu117
pip install facenet-pytorch
```

## 🚀 Sử dụng

### Chạy hệ thống
```bash
python main.py
```

Sau khi chạy:
- **Camera window**: Hiển thị video với nhận diện và tracking
- **Web Dashboard**: Mở trình duyệt tại `http://localhost:5000`

### Phím tắt Camera
- **`q`**: Thoát
- **`r`**: Reset tracking
- **`l`**: Reload face encodings

## 📝 Đăng ký người mới

### Cách 1: Qua Web Dashboard (Khuyến nghị)
1. Mở `http://localhost:5000`
2. Tìm phần "Đăng ký người mới"
3. Nhập tên và upload 1-3 ảnh (ảnh phải có khuôn mặt rõ ràng)
4. Nhấn "Đăng ký người mới"

**Lưu ý về ảnh:**
- Khuôn mặt rõ ràng, hướng về phía trước
- Ánh sáng đủ
- Khuôn mặt chiếm phần lớn khung hình

### Cách 2: Qua Script
```bash
# Đặt ảnh vào thư mục known_faces/ với format: Tên_1.jpg, Tên_2.jpg, Tên_3.jpg
python register_person.py
```

## 🔧 Cấu hình

Chỉnh sửa file `config.py` để thay đổi cấu hình:

```python
# Camera
CAMERA_INDEX = 0        # Index camera (0, 1, 2...)
CAMERA_WIDTH = 640      # Độ rộng
CAMERA_HEIGHT = 480     # Độ cao

# Face Recognition
FACE_RECOGNITION_TOLERANCE = 0.4  # Ngưỡng nhận diện (0.0-1.0)

# API
API_PORT = 5000         # Port của web server
```

## 🛠️ Công cụ hỗ trợ

### Kiểm tra camera
```bash
python tools/check_camera.py
```

### Xóa database
```bash
python tools/force_clear_database.py
```

### Reset database từ ảnh
```bash
python tools/reset_db_from_known_faces.py
```

## 🐛 Xử lý lỗi

### Camera không mở được
- Chạy `python tools/check_camera.py` để kiểm tra
- Thử thay đổi `CAMERA_INDEX` trong `config.py` (0, 1, 2...)

### Không nhận diện được khuôn mặt
- Kiểm tra ảnh đăng ký có khuôn mặt rõ ràng
- Giảm `FACE_RECOGNITION_TOLERANCE` trong `config.py` (ví dụ: 0.5 hoặc 0.6)
- Nhấn `l` trong camera window để reload face encodings

### Lỗi "No valid faces detected"
- Đảm bảo ảnh có khuôn mặt rõ ràng, hướng về phía trước
- Thử với ảnh khác, góc chụp tốt hơn

## 📁 Cấu trúc thư mục

```
PTUD/
├── main.py                 # Chạy hệ thống
├── run_camera.py          # Chạy camera riêng
├── register_person.py     # Đăng ký người
├── config.py              # Cấu hình
├── app/                   # Code chính
│   ├── api/routes.py     # API endpoints
│   ├── models/           # Database models
│   └── services/         # Business logic
├── templates/            # Web dashboard
├── known_faces/          # Ảnh đăng ký người
├── tools/                # Công cụ hỗ trợ
└── database/             # Database SQLite
```

## 📡 API Endpoints

- `GET /api/stats` - Thống kê real-time
- `GET /api/attendance` - Lịch sử chấm công
- `GET /api/persons` - Danh sách người
- `POST /api/persons/register` - Đăng ký người mới
- `GET /api/export/attendance` - Xuất dữ liệu (JSON/CSV/Excel)

Xem chi tiết trong `app/api/routes.py`
