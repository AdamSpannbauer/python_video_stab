"""Playback tests for visual inspection of output
"""
from urllib.request import urlretrieve
import tempfile
from vidstab import VidStab, layer_overlay
import matplotlib.pyplot as plt

# download videos for testing
tmp_dir = tempfile.TemporaryDirectory()

remote_ostrich_vid = 'https://s3.amazonaws.com/python-vidstab/ostrich.mp4'
local_ostrich_vid = '{}/ostrich.mp4'.format(tmp_dir.name)
urlretrieve(remote_ostrich_vid, local_ostrich_vid)
local_vid = local_ostrich_vid

# remote_skateline_vid = 'https://s3.amazonaws.com/python-vidstab/thrasher.mp4'
# local_skateline_vid = '{}/skateline.mp4'.format(tmp_dir.name)
# urlretrieve(remote_skateline_vid, local_skateline_vid)
# local_vid = local_skateline_vid


# set params for test stabilization
input_path = local_vid
border_type = 'black'
border_size = 50
layer_func = layer_overlay
playback = True


stabilizer = VidStab()
stabilizer.stabilize(input_path,
                     '{}/stable.avi'.format(tmp_dir.name),
                     border_type=border_type,
                     border_size=border_size,
                     layer_func=layer_func,
                     playback=playback)

stabilizer.plot_transforms()
plt.show()

stabilizer.plot_transforms(radians=True)
plt.show()
