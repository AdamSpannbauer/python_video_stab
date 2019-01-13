import numpy as np
import cv2
import vidstab.auto_border_utils as utils
import vidstab.vidstab_utils as vidstab_utils


WHITE_FRAME = 255 * np.ones((100, 200, 3), dtype='uint8')
TEST_TRANSFORMS = np.array([[-69.67148996, 67.21674617, -0.16193986]])
TEST_EXTREME_CORNERS = utils.extreme_corners(WHITE_FRAME, TEST_TRANSFORMS)


def demo_auto_border_crop():
    min_border = utils.min_auto_border_size(TEST_EXTREME_CORNERS)
    h, w = WHITE_FRAME.shape[:2]

    og_frame_corners = np.array([[min_border, min_border],
                                 [min_border + w, min_border],
                                 [min_border, min_border + h],
                                 [min_border + w, min_border + h]])

    transformed_frame_corners = [(min_border - 69, min_border + 67),
                                 (min_border - 53, min_border + 164),
                                 (min_border + 126, min_border + 35),
                                 (min_border + 142, min_border + 132)]

    transformed_frame = vidstab_utils.transform_frame(WHITE_FRAME, TEST_TRANSFORMS[0], min_border, 'black')

    for xy in og_frame_corners:
        cv2.circle(transformed_frame, tuple(xy), 3, (0, 0, 255), -1)

    for xy in transformed_frame_corners:
        cv2.circle(transformed_frame, tuple(xy), 3, (255, 0, 255), -1)

    cropped_transformed_frame = utils.auto_border_crop(transformed_frame, TEST_EXTREME_CORNERS, min_border)

    cv2.imshow('pre-crop (red dots = original frame corners)', transformed_frame)
    cv2.imshow('cropped (red dots = original corners)', cropped_transformed_frame)
    cv2.waitKey(0)


def test_extreme_corners():
    extreme_corners = {k: int(v) for k, v in TEST_EXTREME_CORNERS.items()}

    expected_corners = {
        'min_x': -72,
        'min_y': 0,
        'max_x': 0,
        'max_y': 67
    }

    assert extreme_corners == expected_corners


def test_auto_border_start():
    start = utils.auto_border_start(40.4, 100.6)
    assert isinstance(start, int)
    assert start == 60


def test_auto_border_length():
    length = utils.auto_border_length(400, 42.0, 100.6)
    assert isinstance(length, int)
    assert length == 342


def test_auto_border_crop():
    extreme_frame_corners = {
        'min_x': 0,
        'min_y': 0,
        'max_x': 0,
        'max_y': 0
    }

    cropped_frame = utils.auto_border_crop(WHITE_FRAME, extreme_frame_corners, 0)
    assert cropped_frame.shape == WHITE_FRAME.shape

    extreme_frame_corners = {
        'min_x': -10,
        'min_y': -20,
        'max_x': 5,
        'max_y': 10
    }
    min_border_size = utils.min_auto_border_size(extreme_frame_corners)
    cropped_frame = utils.auto_border_crop(WHITE_FRAME, extreme_frame_corners, min_border_size)
    assert cropped_frame.shape == (90, 175, 3)


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


if __name__ == '__main__':
    demo_auto_border_crop()
