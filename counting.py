from ultralytics import YOLO
#from ultralytics.solutions import object_counter
from object_counter import ObjectCounter
import cv2
from IPython.display import Image

model = YOLO("best.pt")
cap = cv2.VideoCapture(0)
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
"""w, h, fps = (1280, 720, 30)"""

# Define region points
line_points_in = [(800, 1080), (800, 0)]


# 
# Video writer
video_writer = cv2.VideoWriter("object_counting_output.avi",
                       cv2.VideoWriter_fourcc(*'mp4v'),
                       fps,
                       (w, h))

# Init Object Counter
#counter = object_counter.ObjectCounter()
counter = ObjectCounter()
counter.set_args(view_img=True,
                 reg_pts=line_points_in,
                 classes_names=model.names,
                 view_in_counts=True,
                 view_out_counts=True,
                 draw_tracks=True)

while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break
    tracks = model.track(im0, persist=True, show=False, save=True, project="runs/detect", exist_ok=True)

    im0 = counter.start_counting(im0, tracks)
    video_writer.write(im0)

cap.release()
video_writer.release()
cv2.destroyAllWindows()