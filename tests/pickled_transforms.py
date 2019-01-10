from urllib.request import urlopen
import pickle


def download_pickled_transforms(window_size):
    base_url = 'https://s3.amazonaws.com/python-vidstab'

    transform_file = '{}/ostrich_transforms_{}.pickle'.format(base_url, window_size)
    trajectory_file = '{}/np_ostrich_trajectory_{}.pickle'.format(base_url, window_size)
    smooth_trajectory_file = '{}/np_ostrich_smooth_trajectory_{}.pickle'.format(base_url, window_size)

    with urlopen(transform_file) as f:
        transforms = pickle.load(f)
    with urlopen(trajectory_file) as f:
        trajectory = pickle.load(f)
    with urlopen(smooth_trajectory_file) as f:
        smooth_trajectory = pickle.load(f)

    return transforms, trajectory, smooth_trajectory
