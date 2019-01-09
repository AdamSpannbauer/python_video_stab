# TODO: add test for vidstab.auto_border_utils.extreme_corners

import numpy as np
import vidstab.auto_border_utils as utils


def test_auto_border_start():
    start = utils.auto_border_start(40.4, 100.6)
    assert isinstance(start, int)
    assert start == 60


def test_auto_border_length():
    length = utils.auto_border_length(400, 42.0, 100.6)
    assert isinstance(length, int)
    assert length == 342


def test_auto_border_crop():
    black_frame = np.zeros((100, 200, 3), dtype='uint8')
    extreme_frame_corners = {
        'min_x': 0,
        'min_y': 0,
        'max_x': 0,
        'max_y': 0
    }

    cropped_frame = utils.auto_border_crop(black_frame, extreme_frame_corners, 0)
    assert cropped_frame.shape == black_frame.shape

    extreme_frame_corners = {
        'min_x': -10,
        'min_y': -20,
        'max_x': 5,
        'max_y': 10
    }
    min_border_size = utils.min_auto_border_size(extreme_frame_corners)
    cropped_frame = utils.auto_border_crop(black_frame, extreme_frame_corners, min_border_size)
    assert cropped_frame.shape == (90, 185, 3)


def test_min_auto_border_size():
    extreme_frame_corners = {
        'min_x': 0,
        'min_y': 0,
        'max_x': 0,
        'max_y': 0
    }

    min_size = utils.min_auto_border_size(extreme_frame_corners)
    assert min_size == 0

    extreme_frame_corners['min_y'] = 10
    min_size = utils.min_auto_border_size(extreme_frame_corners)
    assert min_size == 10

    extreme_frame_corners['min_x'] = -20
    min_size = utils.min_auto_border_size(extreme_frame_corners)
    assert min_size == 20
