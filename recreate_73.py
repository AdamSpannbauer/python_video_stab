from vidstab.VidStab import VidStab
import cv2

filename = 'y2mate_video.mp4'

stabilizer = VidStab()
vidcap = cv2.VideoCapture(filename)
i = 0
while True:
    print(i)
    i += 1

    grabbed_frame, frame = vidcap.read()

    if frame is not None:
        cv2.imshow('input_frame', frame)
        pass

    stabilized_frame = stabilizer.stabilize_frame(input_frame=frame, smoothing_window=15)

    if stabilized_frame is None:
        break

    cv2.imshow('stabilized_frame', stabilized_frame)
    cv2.waitKey(1)
