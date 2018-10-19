import tempfile
from urllib.request import urlretrieve
import cv2
import numpy as np
from vidstab import layer_overlay
from vidstab.vidstab_utils import border_frame
import imutils


tmp_dir = tempfile.TemporaryDirectory()
remote_expected_result = 'https://s3.amazonaws.com/python-vidstab/overlay_2_test.jpg'
overlay_2_test_file = '{}/overlay_2_test.jpg'.format(tmp_dir.name)
urlretrieve(remote_expected_result, overlay_2_test_file)


def add_random_circles(img, n=50, seed=None):
    if seed:
        np.random.seed(seed)

    for _ in range(n):
        color = tuple(np.random.randint(256) for _ in range(3))
        center = (np.random.randint(img.shape[1]), np.random.randint(img.shape[0]))
        radius = np.random.randint(3, 30)
        cv2.circle(img, center, radius, color, -1)


def test_layer_overlay():
    black_frame = np.zeros((100, 200, 3), dtype='uint8')
    rand_frame = black_frame.copy()
    add_random_circles(rand_frame)

    black_frame, _ = border_frame(black_frame, border_size=0, border_type='black')
    rand_frame, _ = border_frame(rand_frame, border_size=0, border_type='black')

    overlay_rand = layer_overlay(rand_frame, black_frame)
    overlay_black = layer_overlay(black_frame, rand_frame)

    assert np.allclose(overlay_black, black_frame)
    assert np.allclose(overlay_rand, rand_frame)


def test_layer_overlay_rotated():
    black_frame = np.zeros((100, 200, 3), dtype='uint8')
    rand_frame_1 = black_frame.copy()
    rand_frame_2 = black_frame.copy()
    add_random_circles(rand_frame_1, seed=42)
    add_random_circles(rand_frame_2, seed=8675309)

    rand_frame_1, _ = border_frame(rand_frame_1, border_size=0, border_type='black')
    rand_frame_2, _ = border_frame(rand_frame_2, border_size=0, border_type='black')

    rand_frame_2 = imutils.rotate(rand_frame_2, 90)

    overlay_1 = layer_overlay(rand_frame_1, rand_frame_2)
    overlay_2 = layer_overlay(rand_frame_2, rand_frame_1)

    overlay_2_expected = cv2.imread(overlay_2_test_file)
    overlay_1 = overlay_1[:, :, :3]
    overlay_2 = overlay_2[:, :, :3]

    # write/read as jpg to match expected
    cv2.imwrite(overlay_2_test_file, overlay_2)
    overlay_2 = cv2.imread(overlay_2_test_file)

    assert np.allclose(overlay_1, overlay_1)
    assert np.allclose(overlay_2, overlay_2_expected)
