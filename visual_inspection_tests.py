"""Playback tests for visual inspection of output"""
import tempfile
import matplotlib.pyplot as plt

from vidstab import VidStab, layer_overlay
import vidstab.download_videos as dl

tmp_dir = tempfile.TemporaryDirectory()
download_to_path = f'{tmp_dir.name}/test_video.mp4'

dl.download_ostrich_video(download_to_path)
# dl.download_skateline_video(download_to_path)

stabilizer = VidStab()
stabilizer.stabilize(download_to_path,
                     'stable.avi',
                     border_type='black',
                     border_size='auto',
                     layer_func=layer_overlay,
                     playback=True)

stabilizer.plot_transforms()
plt.show()

stabilizer.plot_transforms(radians=True)
plt.show()
