"""Playback tests for visual inspection of output
"""

import tempfile
from vidstab import VidStab
import matplotlib.pyplot as plt

input_path = 'readme/ostrich.mp4'

border_type = 'reflect'
border_size = 'auto'
layer_func = None
playback = False


tmp_dir = tempfile.TemporaryDirectory()
output_path = '{}/stable.avi'.format(tmp_dir.name)


stabilizer = VidStab()
stabilizer.stabilize(input_path,
                     output_path,
                     border_type=border_type,
                     border_size=border_size,
                     layer_func=layer_func,
                     playback=playback)

stabilizer.plot_transforms()
plt.show()

stabilizer.plot_transforms(radians=True)
plt.show()
