import os
import cv2
from vidstab import VidStab
import numpy as np
from tqdm import tqdm

# Init stabilizer and video reader
stabilizer = VidStab()
frames = np.load(os.path.join(os.getcwd(), 'vids', 'SEQ_10652.npy'))
frames = frames.astype(np.float32) / 65535.0

frameidx = 0
frame_len = frames.shape[2]
pbar = tqdm(total=frame_len)  # Initialize tqdm with the total number of frames

while frameidx < frame_len:
    frame = frames[:, :, frameidx]

    # Pass frame to stabilizer even if frame is None
    stabilized_frame = stabilizer.stabilize_frame(input_frame=frame,
                                                  border_size=-30,
                                                  smoothing_window=100)

    # If stabilized_frame is None then there are no frames left to process
    if stabilized_frame is None:
        break

    # Display stabilized output
    cv2.imshow('Stabilized Frame', stabilized_frame)
    cv2.imshow('Raw Frame', frame)

    key = cv2.waitKey(5)
    if key == 27:  # Esc key
        break

    frameidx += 1
    pbar.update(1)  # Update the progress bar

    if frameidx == frame_len:
        frameidx = 0

pbar.close()  # Close the progress bar
cv2.destroyAllWindows()
