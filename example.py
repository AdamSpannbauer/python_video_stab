from vidstab import VidStab

# init stabilizer
stabilizer = VidStab()

# stabilize video and write stabilized video to file
stabilizer.stabilize(input_path='readme/input_video.mov', output_path='stable_video.avi')
