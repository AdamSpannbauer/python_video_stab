import tempfile
import cv2
from vidstab import VidStab, layer_overlay, download_ostrich_video

# Download test video to stabilize
tmp_dir = tempfile.TemporaryDirectory()
ostrich_video_path = f'{tmp_dir.name}/vid.avi'
download_ostrich_video(ostrich_video_path)

# Init stabilizer and video reader
stabilizer = VidStab()
vidcap = cv2.VideoCapture(ostrich_video_path)

while True:
    grabbed_frame, frame = vidcap.read()

    if grabbed_frame:
        # Do frame pre-processing
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Pass frame to stabilizer even if frame is None
    stabilized_frame = stabilizer.stabilize_frame(input_frame=frame,
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
