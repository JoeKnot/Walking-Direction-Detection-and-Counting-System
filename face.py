import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO
from object_counter import ObjectCounter
from datetime import datetime

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        self.cap = None
        self.line_points_in = [(800, 1080), (800, 0)]
        self.video_writer = None
        self.model = YOLO("best.pt")
        
        self.counter = ObjectCounter()
        self.counter.set_args(view_img=True,
                              reg_pts=self.line_points_in,
                              classes_names=self.model.names,
                              view_in_counts=True,
                              view_out_counts=True,
                              draw_tracks=True)
        
        cam_icon = PhotoImage(file=r"C:\Users\Nathakrit\Downloads\weights\cam.png")
        notcam_icon = PhotoImage(file=r"C:\Users\Nathakrit\Downloads\weights\notcam.png")
        
        self.label = tk.Label(window)
        self.label.pack(expand=True, fill="both",anchor="center")

        self.label_clock = tk.Label(window, text="", font=("Arial", 20))
        self.label_clock.place(x=10, y=10)

        self.btn_toggle_camera = tk.Button(window, text="เปิดกล้อง", command=self.toggle_camera, width=10, height=6)
        self.btn_toggle_camera.place(x=1250, y=700)
        #self.btn_toggle_camera.pack(side="right", padx=50, pady=50)
        
        self.btn_toggle_detecting = tk.Button(window, text="เปิดตรวจจับ", command=self.toggle_detecting, width=10, height=6)
        self.btn_toggle_detecting.place(x=1350, y=700)
        #self.btn_toggle_detecting.pack(side="right", padx=50, pady=50)
        
        self.detecting_enabled = False
        
        self.label_countin = tk.Label(window, text="Count IN: ", font=("Arial", 25))
        self.label_countin.place(x=10, y=700)

        self.label_countout = tk.Label(window, text= "Count OUT: ", font=("Arial", 25))
        self.label_countout.place(x=250, y=700)

        self.label_diff = tk.Label(window, text= "Difference = ", font=("Arial", 25))
        self.label_diff.place(x=10, y=750)

        self.label1 = tk.Label(text="Camera Off", font=("Arial", 20))
        self.label1.place(x=640, y=700)
        """self.label1.place(anchor="center", padx=10, pady=10)"""

        self.label2 = tk.Label(text="Detection Off", font=("Arial", 20))
        self.label2.place(x=640, y=750)
        """self.label2.place(anchor="center", padx=10, pady=12)"""


        self.update()
        self.update_clock()
        self.window.mainloop()
    
    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.label_clock.config(text=current_time)
        self.window.after(1000, self.update_clock)

    def toggle_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture("vdo_test_1.mp4")
            desired_width = 1290  # Set your desired width
            desired_height = 720  # Set your desired height
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)
            self.btn_toggle_camera.config(text="ปิดกล้อง", width=10, height=6)
            self.label1.config(text="Camera On")



        else:
            self.cap.release()
            self.cap = None
            self.btn_toggle_camera.config(text="เปิดกล้อง", width=10, height=6)
            self.label1.config(text="Camera Off")
            


    def toggle_detecting(self):
        self.detecting_enabled = not self.detecting_enabled # เปลี่ยนสถานะการตรวจจับวัตถุ
        if self.detecting_enabled:
            self.btn_toggle_detecting.config(text="ปิดตรวจจับ", width=10, height=6) # เปลี่ยนข้อความปุ่มเป็น "ปิดตรวจจับ"
            self.label2.config(text="Detection On")
        else:
            self.btn_toggle_detecting.config(text="เปิดตรวจจับ", width=10, height=6) # เปลี่ยนข้อความปุ่มเป็น "เปิดตรวจจับ"
            self.label2.config(text="Detection Off")

    def update(self):
        if self.cap is not None: # ตรวจสอบว่ากล้องถูกเปิดหรือไม่
            success, im0 = self.cap.read()
            if success:
                if self.detecting_enabled: # ตรวจสอบว่าต้องการทำการตรวจจับหรือไม่
                    tracks = self.model.track(im0, persist=True, show=False, save=True, project="runs/detect", exist_ok=True)
                    im0 = self.counter.start_counting(im0, tracks)
                    self.update_count_label()
                photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(im0, cv2.COLOR_BGR2RGB)))
                self.label.config(image=photo)
                self.label.image = photo

                if self.video_writer is not None: # ตรวจสอบว่ากล้องถูกเปิดหรือไม่
                    self.video_writer.write(im0)
        self.window.after(15, self.update)

    def update_count_label(self):
        incount_label = f"Count IN: {self.counter.in_counts}"
        outcount_label = f"Count OUT: {self.counter.out_counts}"
        self.label_countin.config(text=incount_label, font=("Arial", 25))
        self.label_countout.config(text=outcount_label, font=("Arial", 25))
        diff = self.counter.in_counts - self.counter.out_counts
        diff_label = f"Difference = {diff}"
        self.label_diff.config(text=diff_label, font=("Arial", 25))

# Create Tkinter window
root = tk.Tk()
# Center the window
window_width = 1280
window_height = 720
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
root.geometry(f'{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}')



app = CameraApp(root, "กล้อง")

