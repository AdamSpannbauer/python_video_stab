import tempfile
import numpy as np
import cv2
from vidstab import ROIStab, layer_overlay, download_ostrich_video

# Download test video to stabilize
tmp_dir = tempfile.TemporaryDirectory()
ostrich_video_path = f'{tmp_dir.name}/vid.avi'
download_ostrich_video(ostrich_video_path)

# Init stabilizer and video reader
stabilizer = ROIStab()
vidcap = cv2.VideoCapture(ostrich_video_path)


x, y, w, h = 438, 223, 100, 100
while True:
    grabbed_frame, frame = vidcap.read()

    if frame is not None:
        # Do frame pre-processing
        cv2.rectangle(frame, (x, y), (x + w, y + h), color=(0, 0, 255), thickness=-1)
        cv2.rectangle(frame, (x + 10, y + 10), (x + w - 10, y + h - 10), color=(0, 255, 255), thickness=-1)
        cv2.rectangle(frame, (x + 15, y + 15), (x + w - 15, y + h - 15), color=(255, 0, 0), thickness=-1)
        cv2.rectangle(frame, (x + 20, y + 20), (x + w - 20, y + h - 20), color=(0, 255, 255), thickness=-1)
        cv2.rectangle(frame, (x + 25, y + 25), (x + w - 25, y + h - 25), color=(255, 0, 255), thickness=-1)
        cv2.rectangle(frame, (x + 30, y + 30), (x + w - 30, y + h - 30), color=(0, 255, 0), thickness=-1)

        bb = x - 10, y - 10, w + 20, h + 20
        x1 = bb[0]
        y1 = bb[1]
        x2 = bb[0] + bb[2]
        y2 = bb[1] + bb[3]

        roi = frame[y1:y2, x1:x2]
        print(roi.shape)
        cv2.imshow('Input ROI', roi)

    # Pass frame to stabilizer even if frame is None
    stabilizer.roi_bb = bb
    stabilized_frame = stabilizer.stabilize_frame(input_frame=frame,
                                                  smoothing_window=3,
                                                  layer_func=layer_overlay,
                                                  border_size=100)

    # If stabilized_frame is None then there are no frames left to process
    if stabilized_frame is None:
        break

    # Display stabilized output
    cv2.imshow('Stabilized Frame', stabilized_frame)

    key = cv2.waitKey(5)
    if key == 27:
        break

vidcap.release()
cv2.destroyAllWindows()
