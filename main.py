import cv2
import numpy as np
import threading
import time
from datetime import datetime
import os
import sys

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from app.models.database import db, init_db
from app.services.face_recognition import FaceRecognitionService
from app.services.tracking import TrackingService
from app.services.attendance import AttendanceService
from app.api.routes import create_app

class FaceTrackingSystem:
    """Hệ thống nhận diện và tracking người chính"""
    
    def __init__(self, face_service=None, tracking_service=None, attendance_service=None):
        # Allow injecting services (useful when running API + camera in same process)
        self.face_service = face_service or FaceRecognitionService()
        self.tracking_service = tracking_service or TrackingService()
        self.attendance_service = attendance_service or AttendanceService()
        self.camera = None
        self.running = False
        self.frame_count = 0
        
    def initialize_camera(self):
        """Khởi tạo camera"""
        try:
            self.camera = cv2.VideoCapture(Config.CAMERA_INDEX)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
            self.camera.set(cv2.CAP_PROP_FPS, Config.CAMERA_FPS)
            
            if not self.camera.isOpened():
                raise Exception("Cannot open camera")
            
            print(f"Camera initialized: {Config.CAMERA_WIDTH}x{Config.CAMERA_HEIGHT} @ {Config.CAMERA_FPS}fps")
            return True
            
        except Exception as e:
            print(f"Error initializing camera: {e}")
            return False
    
    def process_frame(self, frame):
        """Xử lý một frame"""
        self.frame_count += 1
        
        # Nhận diện khuôn mặt
        face_results = self.face_service.recognize_faces_in_frame(frame)
        
        # Tracking người
        tracking_results = self.tracking_service.process_frame(frame, self.face_service)
        
        # Xử lý attendance
        active_track_ids = [result['track_id'] for result in tracking_results]
        self.attendance_service.check_timeout_attendances(active_track_ids)
        
        # Log time_in cho các track mới
        for result in tracking_results:
            track_id = result['track_id']
            person_id = result['person_id']
            name = result['name']
            
            if track_id not in self.attendance_service.active_attendances:
                self.attendance_service.log_time_in(track_id, person_id, name)
            else:
                # If an active attendance exists but person info was previously unknown
                # and now we've recognized the person, update the active attendance
                try:
                    if person_id is not None and person_id != self.attendance_service.active_attendances[track_id].get('person_id'):
                        self.attendance_service.update_active_attendance(track_id, person_id=person_id, person_name=name)
                    elif name and name != self.attendance_service.active_attendances[track_id].get('person_name'):
                        self.attendance_service.update_active_attendance(track_id, person_id=person_id, person_name=name)
                except Exception:
                    pass
        
        # Vẽ kết quả lên frame
        frame = self.face_service.draw_face_boxes(frame, face_results)
        frame = self.tracking_service.draw_tracking_boxes(frame, tracking_results)
        
        # Thêm thông tin hệ thống
        self.draw_system_info(frame, tracking_results)
        
        return frame, tracking_results
    
    def draw_system_info(self, frame, tracking_results):
        """Vẽ thông tin hệ thống lên frame"""
        # Thông tin cơ bản
        info_text = [
            f"Frame: {self.frame_count}",
            f"Active Tracks: {len(tracking_results)}",
            f"Active Attendances: {len(self.attendance_service.active_attendances)}",
            f"Time: {datetime.now().strftime('%H:%M:%S')}"
        ]
        
        y_offset = 30
        for text in info_text:
            cv2.putText(frame, text, (10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            y_offset += 25
    
    def run_camera_loop(self):
        """Vòng lặp chính của camera"""
        print("Starting camera loop...")
        
        while self.running:
            ret, frame = self.camera.read()
            if not ret:
                print("Failed to read frame from camera")
                break
            
            try:
                # Xử lý frame
                processed_frame, tracking_results = self.process_frame(frame)
                
                # Hiển thị frame
                cv2.imshow('Face Tracking System', processed_frame)
                
                # Kiểm tra phím thoát
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("Quit key pressed")
                    break
                elif key == ord('r'):
                    print("Reset tracking")
                    self.tracking_service.reset_tracking()
                    self.attendance_service.active_attendances.clear()
                
            except Exception as e:
                print(f"Error processing frame: {e}")
                continue
        
        print("Camera loop ended")
    
    def start(self):
        """Khởi động hệ thống"""
        print("Starting Face Tracking System...")
        
        # Khởi tạo camera
        if not self.initialize_camera():
            print("Failed to initialize camera. Exiting...")
            return False
        
        self.running = True
        
        try:
            # Chạy camera loop
            self.run_camera_loop()
        except KeyboardInterrupt:
            print("System interrupted by user")
        except Exception as e:
            print(f"System error: {e}")
        finally:
            self.stop()
        
        return True
    
    def stop(self):
        """Dừng hệ thống"""
        print("Stopping Face Tracking System...")
        self.running = False
        
        if self.camera:
            self.camera.release()
        
        cv2.destroyAllWindows()
        print("System stopped")

def run_api_server(app=None):
    """Chạy API server; nếu truyền sẵn app thì chạy app đó (useful for sharing services)
    Nếu không truyền, tự tạo app mới (backward compatible)."""
    print("Starting API server...")
    if app is None:
        app = create_app()
    try:
        app.run(host=Config.API_HOST, port=Config.API_PORT, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("API server stopped by user")
    except Exception as e:
        print(f"API server error: {e}")

def main():
    """Hàm main"""
    print("=" * 50)
    print("Face Recognition & People Tracking System")
    print("=" * 50)
    
    # Tạo thư mục cần thiết
    os.makedirs('database', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    os.makedirs('known_faces', exist_ok=True)
    
    # Khởi tạo database
    from app.api.routes import create_app
    app = create_app()
    with app.app_context():
        init_db(app)
    
    # Chọn chế độ chạy
    print("\nChọn chế độ chạy:")
    print("1. Chạy hệ thống camera (nhận diện + tracking)")
    print("2. Chạy API server (dashboard)")
    print("3. Chạy cả hai (camera + API)")
    
    try:
        choice = input("\nNhập lựa chọn (1/2/3): ").strip()
        
        if choice == '1':
            # Chỉ chạy camera
            system = FaceTrackingSystem()
            system.start()
            
        elif choice == '2':
            # Chỉ chạy API
            run_api_server()
            
        elif choice == '3':
            # Chạy cả hai
            # Chạy API server trong thread riêng
            api_thread = threading.Thread(target=run_api_server, args=(app,), daemon=True)
            api_thread.start()
            
            # Đợi một chút để API server khởi động
            time.sleep(2)
            print("API server started at http://localhost:5000")
            
            # Chạy camera system
            # Reuse services from the Flask app so in-memory state is shared
            try:
                app_services = app
                system = FaceTrackingSystem(
                    face_service=getattr(app_services, 'face_service', None),
                    tracking_service=getattr(app_services, 'tracking_service', None),
                    attendance_service=getattr(app_services, 'attendance_service', None)
                )
            except Exception:
                system = FaceTrackingSystem()
            system.start()
            
        else:
            print("Lựa chọn không hợp lệ")
            
    except KeyboardInterrupt:
        print("\nHệ thống được dừng bởi người dùng")
        print("Đang dừng tất cả processes...")
        
        # Dừng camera system
        if 'system' in locals():
            system.stop()
        
        # Dừng API server nếu đang chạy
        try:
            import requests
            requests.get('http://localhost:5000/shutdown', timeout=1)
        except:
            pass
        
        print("Tất cả processes đã được dừng!")
        
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == '__main__':
    main()
