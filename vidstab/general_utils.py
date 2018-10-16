import numpy as np
from progress.bar import IncrementalBar


def bfill_rolling_mean(arr, n=30):
    """Helper to perform trajectory smoothing

    :param arr: Numpy array of frame trajectory to be smoothed
    :param n: window size for rolling mean
    :return: smoothed input arr

    >>> arr = np.array([[1, 2, 3], [4, 5, 6]])
    >>> bfill_rolling_mean(arr, n=2)
    array([[ 2.5,  3.5,  4.5],
           [ 2.5,  3.5,  4.5]])
    """
    if arr.shape[0] < n:
        raise ValueError('arr.shape[0] cannot be less than n')
    if n == 1:
        return arr

    pre_buffer = np.zeros(3).reshape(1, 3)
    post_buffer = np.zeros(3 * n).reshape(n, 3)
    arr_cumsum = np.cumsum(np.vstack((pre_buffer, arr, post_buffer)), axis=0)
    buffer_roll_mean = (arr_cumsum[n:, :] - arr_cumsum[:-n, :]) / float(n)
    trunc_roll_mean = buffer_roll_mean[:-n, ]

    bfill_size = arr.shape[0] - trunc_roll_mean.shape[0]
    bfill = np.tile(trunc_roll_mean[0, :], (bfill_size, 1))

    return np.vstack((bfill, trunc_roll_mean))


def init_progress_bar(frame_count, max_frames, show_progress=True, message='Stabilizing'):
    """Helper to create progress bar for stabilizing processes

    :param frame_count: input video's cv2.CAP_PROP_FRAME_COUNT
    :param max_frames: user provided max number of frames to process
    :param show_progress: user input if bar should be created
    :param message: progress bar label
    :return: a progress.bar.IncrementalBar

    >>> init_progress_bar(30, float('inf'))
    >>> # use bar methods...
    Stabilizing |█████████████████████████▋      | 80%
    """
    if show_progress:
        # frame count is negative during some cv2.CAP_PROP_FRAME_COUNT failures
        if frame_count <= 0 and max_frames == float('inf'):
            bar = None
            print('No progress bar will be shown. (Unable to grab frame count & no max_frames provided.)')
        else:
            if frame_count <= 0 or frame_count > max_frames:
                max_bar = max_frames
            else:
                max_bar = frame_count
            bar = IncrementalBar(message,
                                 max=max_bar,
                                 suffix='%(percent)d%%')
    else:
        bar = None

    return bar
