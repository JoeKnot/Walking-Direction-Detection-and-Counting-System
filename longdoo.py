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
        
        self.canvas = tk.Canvas(window,width=800, height=600)
        self.canvas.pack()
        
        self.btn_toggle_camera = tk.Button(window, text="เปิดกล้อง", command=self.toggle_camera)
        self.btn_toggle_camera.pack()
        
        self.update()
        
        self.window.mainloop()
    
    def toggle_camera(self):
        if self.cap is None: # ถ้ากล้องยังไม่ถูกเปิด
            self.cap = cv2.VideoCapture(0) # เปิดกล้อง
            self.btn_toggle_camera.config(text="ปิดกล้อง") # เปลี่ยนข้อความปุ่มเป็น "ปิดกล้อง"
        else:
            self.cap.release() # ปิดกล้อง
            self.cap = None
            self.btn_toggle_camera.config(text="เปิดกล้อง") # เปลี่ยนข้อความปุ่มเป็น "เปิดกล้อง"
        
    def update(self):
        if self.cap is not None: # ตรวจสอบว่ากล้องถูกเปิดหรือไม่
            success, im0 = self.cap.read()
            if success:
                tracks = self.model.track(im0, persist=True, show=False, save=True, project="runs/detect", exist_ok=True)
                im0 = self.counter.start_counting(im0, tracks)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(im0, cv2.COLOR_BGR2RGB)))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                if self.video_writer is not None: # ตรวจสอบว่ากล้องถูกเปิดหรือไม่
                    self.video_writer.write(im0)
        self.window.after(15, self.update)

# สร้างหน้าต่าง Tkinter
root = tk.Tk()
app = CameraApp(root, "กล้อง")