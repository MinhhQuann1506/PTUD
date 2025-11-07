# 🎯 Face Tracking System
## Hệ thống nhận diện và theo dõi người trong phòng

Hệ thống Face Tracking hoàn chỉnh với khả năng nhận diện khuôn mặt, tracking người và chấm công tự động.

## ✨ Tính năng chính
# Face Tracking System

Hệ thống nhận diện khuôn mặt và tracking người, kèm dashboard thời gian thực và chức năng chấm công.

Mục tiêu:
- Phát hiện và nhận diện khuôn mặt trên video
- Tracking người (YOLOv8 + DeepSORT)
- Ghi nhận time_in / time_out vào database
- Dashboard web và API để theo dõi realtime

---

## Bắt đầu nhanh (Windows PowerShell)

1) Kích hoạt môi trường ảo (nếu có):

```powershell
face_tracking_env\Scripts\activate
```

2) Cài dependencies:

```powershell
pip install -r requirements.txt
# Nếu dùng facenet-pytorch (tăng độ chính xác), cài torch + facenet-pytorch
pip install torch --index-url https://download.pytorch.org/whl/cu117
pip install facenet-pytorch
```

3) Chạy ứng dụng:

```powershell
python main.py
```

Khi chương trình hỏi, chọn:
- `1`: chạy camera (nhận diện + tracking)
- `2`: chạy API server (dashboard) — mặc định http://localhost:5000
- `3`: chạy cả API + camera trong cùng process

---

## Các file / thư mục quan trọng
- `app/` — Flask app, models và services
	- `app/services/face_recognition.py` — pipeline nhận diện (facenet lazy-load, histogram fallback)
	- `app/services/tracking.py` — YOLO + DeepSORT
	- `app/services/attendance.py` — quản lý active attendances và lịch sử
	- `app/api/routes.py` — endpoints REST
- `known_faces/` — ảnh reference cho người đã đăng ký
- `database/attendance.db` — SQLite database (tạo tự động)
- `templates/dashboard.html` — giao diện dashboard
- `tools/` — scripts hỗ trợ (calibration, camera test)

---

## Endpoints chính (tóm tắt)
- `GET /api/stats` — thống kê realtime (active people, tracks, timestamp)
- `POST /api/realtime/update` — camera có thể gửi event realtime (time_in/time_out/tracks)
- `POST /api/persons/register` — đăng ký người (name + up to 3 images)
- `GET /api/attendance` — lấy lịch sử attendance

Chi tiết về các endpoint có thể xem trong `app/api/routes.py`.

---

## Công cụ hỗ trợ (tools/)
- `tools/check_camera.py` — kiểm tra index camera có mở được không
- `tools/compute_embedding_stats.py` — tính pairwise distances giữa encodings và gợi ý threshold

Các script test/nghiên cứu nhỏ khác đã được xóa để giữ repository sạch.

---

## Lưu ý vận hành
- Nếu camera không mở: chạy `python tools/check_camera.py` để kiểm tra indices (Windows thường dùng index 0 hoặc 1).
- Nếu nhận diện chưa tốt: cài `torch` + `facenet-pytorch` để dùng embeddings 512-d (InceptionResnetV1) thay vì histogram.
- Nếu gặp lỗi về "encoding dimension mismatch" đã được xử lý tạm bằng padding/truncation; tốt nhất là tái-encode tất cả `known_faces/` bằng facenet để có kích thước đồng nhất.

---

## Các thay đổi đã thực hiện (gần đây)
- Đồng bộ in-memory active attendances với DB; khi danh tính của một track được xác định sau, attendance hiện tại sẽ được cập nhật (in-memory và DB nếu đã persisted).
- Thêm endpoint `/api/realtime/update` để camera/process khác có thể đẩy event realtime vào API.
- Thêm UI đăng ký người (dashboard) và endpoint nhận upload (3 ảnh tối đa).
- Thêm pipeline nhận diện: CLAHE + centroid + lazy facenet embedding (fallback histogram).

---

## Chính sách cleanup
Xóa hai file tài liệu cũ: `PROJECT_STRUCTURE.md` và `USAGE_GUIDE.md` (đã xóa). Giữ README chính này làm tài liệu duy nhất.

---

Nếu bạn muốn, tôi có thể:
- Tạo script migration để tái-encode toàn bộ ảnh trong `known_faces/` bằng facenet và lưu vào DB.
- Thêm endpoint API để camera push cập nhật identity cho track cụ thể (nếu camera chạy ở process riêng).

Nếu OK, tôi sẽ cập nhật `requirements.txt` hoặc thêm script migration theo bước tiếp theo.
