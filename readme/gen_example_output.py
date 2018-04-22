from vidstab import VidStab
import matplotlib.pyplot as plt

stabilizer = VidStab()
stabilizer.gen_transforms(input_path='input_video.mov')

stabilizer.plot_trajectory()
plt.savefig('readme/trajectory_plot.png')

stabilizer.plot_transforms()
plt.savefig('readme/transforms_plot.png')

stabilizer.stabilize(input_path='input_video.mov', output_path='stable_video.avi')
