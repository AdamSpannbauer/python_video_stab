"""Playback tests for visual inspection of output

PROFILING PIPELINE:
$ python -m cProfile -o temp.dat visual_inspection_tests.py
$ snakeviz temp.dat
"""
import tempfile
from vidstab import VidStab, layer_overlay
import vidstab.download_videos as dl

tmp_dir = tempfile.TemporaryDirectory()

##################################################################
# TEST APPLYING OSTRICH TRANSFORMS TO DIFFERENT VIDEO
##################################################################
# download_to_path = f'{tmp_dir.name}/test_video.mp4'
# dl.download_ostrich_video(download_to_path)
# stabilizer = VidStab()
# stabilizer.gen_transforms(download_to_path)
# download_to_path = f'{tmp_dir.name}/test_video.mp4'
# dl.download_skateline_video(download_to_path)
# stabilizer.apply_transforms(download_to_path,
#                             'stable.avi',
#                             border_size='auto',
#                             playback=True)


##################################################################
# TEST TYPICAL STABILIZATION PROCESS
##################################################################
download_to_path = f'{tmp_dir.name}/test_video.mp4'
dl.download_ostrich_video(download_to_path)
# dl.download_skateline_video(download_to_path)

stabilizer = VidStab()
stabilizer.stabilize(download_to_path,
                     'stable.avi',
                     # max_frames=30,
                     border_type='black',
                     border_size='auto',
                     layer_func=layer_overlay,
                     playback=True)

##################################################################
# TEST PLOT OUTPUT
##################################################################
# import matplotlib.pyplot as plt
#
# download_to_path = f'{tmp_dir.name}/test_video.mp4'
# dl.download_ostrich_video(download_to_path)
# stabilizer = VidStab()
# stabilizer.gen_transforms(download_to_path)
#
# stabilizer.plot_transforms()
# plt.show()
#
# stabilizer.plot_transforms(radians=True)
# plt.show()
