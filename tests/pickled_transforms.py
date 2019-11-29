import os
import pickle
from urllib.request import urlopen
import imutils


def download_pickled_transforms(window_size=30, cv4=False):
    base_url = 'https://s3.amazonaws.com/python-vidstab'

    window_size = str(window_size) + '_cv4' if cv4 else window_size

    base_urls = [
        f'{base_url}/ostrich_transforms_{window_size}.pickle',
        f'{base_url}/np_ostrich_trajectory_{window_size}.pickle',
        f'{base_url}/np_ostrich_smooth_trajectory_{window_size}.pickle'
    ]

    objs = [pickle_load_from_url(url) for url in base_urls]

    return tuple(objs)


def pickle_load_from_url(url):
    with urlopen(url) as f:
        unpickled_obj = pickle.load(f)

    return unpickled_obj


def pickle_dump(obj, file_path):
    with open(file_path, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)


def pickle_test_transforms(vidstab_obj, path):
    suffix = '_cv4.pickle' if imutils.is_cv4() else '.pickle'

    if not os.path.exists(path):
        os.makedirs(path)

    base_paths = [
        '{}/ostrich_transforms_{}{}',
        '{}/np_ostrich_trajectory_{}{}',
        '{}/np_ostrich_smooth_trajectory_{}{}'
    ]

    # noinspection PyProtectedMember
    paths = [p.format(path, vidstab_obj._smoothing_window, suffix) for p in base_paths]

    pickle_dump(vidstab_obj.transforms, paths[0])
    pickle_dump(vidstab_obj.trajectory, paths[1])
    pickle_dump(vidstab_obj.smoothed_trajectory, paths[2])
