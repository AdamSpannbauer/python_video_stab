from vidstab import VidStab, layer_overlay, layer_blend
import matplotlib.pyplot as plt

input_vid = 'ostrich.mp4'

stabilizer = VidStab()
stabilizer.gen_transforms(input_path=input_vid)

stabilizer.plot_trajectory()
plt.savefig('trajectory_plot.png')

stabilizer.plot_transforms()
plt.savefig('transforms_plot.png')

# USING AND SIZING BORDERS

# # default (0 width border)
# stabilizer.stabilize(input_path=input_vid,
#                      output_path='stable_video.avi',
#                      border_type='black')
#
# # wide black border
# stabilizer.stabilize(input_path=input_vid,
#                      output_path='wide_stable_video.avi',
#                      border_type='black',
#                      border_size=100)
#
# # crop with negative border
# stabilizer.stabilize(input_path=input_vid,
#                      output_path='crop_stable_video.avi',
#                      border_type='black',
#                      border_size=-100)
#
# # replicated border
# stabilizer.stabilize(input_path=input_vid,
#                      output_path='rep_stable_video.avi',
#                      border_type='replicate',
#                      border_size=100)
#
# # reflected border
# stabilizer.stabilize(input_path=input_vid,
#                      output_path='ref_stable_video.avi',
#                      border_type='reflect',
#                      border_size=100)

# USING LAYERING FUNCTIONS

# trail of frames
stabilizer.stabilize(input_path=input_vid,
                     output_path='trail_stable_video.avi',
                     border_type='black',
                     border_size=100,
                     layer_func=layer_overlay)


def layer_custom(foreground, background):
    return layer_blend(foreground, background, foreground_alpha=.8)


stabilizer.stabilize(input_path=input_vid,
                     output_path='blend_stable_video.avi',
                     border_type='black',
                     border_size=100,
                     layer_func=layer_custom)
