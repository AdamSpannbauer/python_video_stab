from urllib.request import urlretrieve


REMOTE_OSTRICH_VID_PATH = 'https://s3.amazonaws.com/python-vidstab/ostrich.mp4'
REMOTE_TRUNCATED_OSTRICH_VID_PATH = 'https://s3.amazonaws.com/python-vidstab/trunc_video.avi'
REMOTE_SKATELINE_VID_PATH = 'https://s3.amazonaws.com/python-vidstab/thrasher.mp4'


def download_ostrich_video(download_to_path):
    """Download example shaky clip of ostrich used in README (mp4)

    Video used with permission the HappyLiving YouTube channel.
    Original video: https://www.youtube.com/watch?v=9pypPqbV_GM

    :param download_to_path: path to save video to
    :return: None

    >>> from vidstab import VidStab, download_ostrich_video
    >>> path = 'ostrich.mp4'
    >>> download_ostrich_video(path)
    >>>
    >>> stabilizer = VidStab()
    >>> stabilizer.stabilize(path, 'output_path.avi')
    """
    urlretrieve(REMOTE_OSTRICH_VID_PATH, download_to_path)


def download_skateline_video(download_to_path=None):
    """Download additional testing video

    NOT FOR GENERAL USE; VIDEO MIGHT BE REMOVED WITHOUT WARNING

    :param download_to_path: path to save video to
    :return: None
    """
    urlretrieve(REMOTE_SKATELINE_VID_PATH, download_to_path)


def download_truncated_ostrich_video(download_to_path=None):
    """Download additional testing video

    NOT FOR GENERAL USE; VIDEO MIGHT BE REMOVED WITHOUT WARNING

    :param download_to_path: path to save video to
    :return: None
    """
    urlretrieve(REMOTE_TRUNCATED_OSTRICH_VID_PATH, download_to_path)
