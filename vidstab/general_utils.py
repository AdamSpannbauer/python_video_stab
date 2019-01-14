import warnings
import cv2
import numpy as np
import imutils
from progress.bar import IncrementalBar


def bfill_rolling_mean(arr, n=30):
    """Helper to perform trajectory smoothing

    :param arr: Numpy array of frame trajectory to be smoothed
    :param n: window size for rolling mean
    :return: smoothed input arr

    >>> arr = np.array([[1, 2, 3], [4, 5, 6]])
    >>> bfill_rolling_mean(arr, n=2)
    array([[2.5, 3.5, 4.5],
           [2.5, 3.5, 4.5]])
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


def init_progress_bar(frame_count, max_frames, show_progress=True, gen_all=False):
    """Helper to create progress bar for stabilizing processes

    :param frame_count: input video's cv2.CAP_PROP_FRAME_COUNT
    :param max_frames: user provided max number of frames to process
    :param show_progress: user input if bar should be created
    :param gen_all: if False progress message is 'Stabilizing'; otherwise 'Generating Transforms'
    :return: a progress.bar.IncrementalBar

    >>> progress_bar = init_progress_bar(30, float('inf'))
    >>> # Stabilizing |█████████████████████████▋      | 80%
    """
    if not show_progress:
        return None

    # frame count is negative during some cv2.CAP_PROP_FRAME_COUNT failures
    bad_frame_count = frame_count <= 0
    use_max_frames = bad_frame_count or frame_count > max_frames

    if bad_frame_count and max_frames == float('inf'):
        warnings.warn('No progress bar will be shown. (Unable to grab frame count & no max_frames provided.)')
        return None

    max_bar = max_frames if use_max_frames else frame_count
    message = progress_message(gen_all)

    return IncrementalBar(message, max=max_bar, suffix='%(percent)d%%')


def progress_message(gen_all):
    """Decide progress bar message based on gen_all flag"""
    if gen_all:
        return 'Generating Transforms'
    else:
        return 'Stabilizing'


def update_progress_bar(bar, show_progress=True, finish=False):
    """helper to handle progress bar updates in vidstab process

    :param bar: progress bar to be updated
    :param show_progress: user set flag of whether or not to display progress bar
    :param finish: finish progress bar
    :return: updated progress bar
    """
    if show_progress and bar is not None:
        bar.next()

        if finish:
            bar.finish()


def playback_video(display_frame, playback_flag, delay, max_display_width=750):
    if not playback_flag:
        return False

    if display_frame.shape[1] > max_display_width:
        display_frame = imutils.resize(display_frame, width=max_display_width)

    cv2.imshow('VidStab Playback ({} frame delay if using live video;'
               ' press Q or ESC to quit)'.format(delay),
               display_frame)
    key = cv2.waitKey(1)

    if key == ord("q") or key == 27:
        return True
