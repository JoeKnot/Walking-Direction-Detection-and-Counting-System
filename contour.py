import tkinter as tk
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO
from object_counter import ObjectCounter

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        self.cap = None # กำหนดตัวแปร cap เป็น None เพื่อใช้ในการตรวจสอบสถานะของกล้อง
        
        self.line_points_in = [(800, 1080), (800, 0)]
        
        self.video_writer = None # กำหนดตัวแปร video_writer เป็น None เพื่อใช้ในการตรวจสอบสถานะของการบันทึกวิดีโอ
        
        self.model = YOLO("best.pt")
        
        self.counter = ObjectCounter()
        self.counter.set_args(view_img=True,
                              reg_pts=self.line_points_in,
                              classes_names=self.model.names,
                              view_in_counts=True,
                              view_out_counts=True,
                              draw_tracks=True)
        
        self.canvas = tk.Label(window)
        self.canvas.pack(anchor="center")
        
        self.btn_toggle_camera = tk.Button(window, text="เปิดกล้อง", command=self.toggle_camera)
        self.btn_toggle_camera.pack()
        
        self.btn_toggle_detecting = tk.Button(window, text="เปิดตรวจจับ", command=self.toggle_detecting)
        self.btn_toggle_detecting.pack()
        
        self.detecting_enabled = False
        
        self.update()
        
        self.window.mainloop()
    
    def toggle_camera(self):
        if self.cap is None: # ถ้ากล้องยังไม่ถูกเปิด
            self.cap = cv2.VideoCapture("vdo_test_1.mp4") # เปิดกล้อง
            desired_width = 1280  # Set your desired width
            desired_height = 720  # Set your desired height
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)
            self.btn_toggle_camera.config(text="ปิดกล้อง") # เปลี่ยนข้อความปุ่มเป็น "ปิดกล้อง"
        
        else:
            self.cap.release() # ปิดกล้อง
            self.cap = None
            self.btn_toggle_camera.config(text="เปิดกล้อง") # เปลี่ยนข้อความปุ่มเป็น "เปิดกล้อง"
         
    
    def toggle_detecting(self):
        self.detecting_enabled = not self.detecting_enabled # เปลี่ยนสถานะการตรวจจับวัตถุ
        if self.detecting_enabled:
            self.btn_toggle_detecting.config(text="ปิดตรวจจับ") # เปลี่ยนข้อความปุ่มเป็น "ปิดตรวจจับ"
        else:
            self.btn_toggle_detecting.config(text="เปิดตรวจจับ") # เปลี่ยนข้อความปุ่มเป็น "เปิดตรวจจับ"
        
    def update(self):
        if self.cap is not None: # ตรวจสอบว่ากล้องถูกเปิดหรือไม่
            success, im0 = self.cap.read()
            if success:
                if self.detecting_enabled: # ตรวจสอบว่าต้องการทำการตรวจจับหรือไม่
                    tracks = self.model.track(im0, persist=True, show=False, save=True, project="runs/detect", exist_ok=True)
                    im0 = self.counter.start_counting(im0, tracks)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(im0, cv2.COLOR_BGR2RGB)))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                if self.video_writer is not None: # ตรวจสอบว่ากล้องถูกเปิดหรือไม่
                    self.video_writer.write(im0)
        self.window.after(15, self.update)

# สร้างหน้าต่าง Tkinter
root = tk.Tk()
# Center the window
window_width = 1440
window_height = 900
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
root.geometry(f'{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}')
app = CameraApp(root, "กล้อง")
