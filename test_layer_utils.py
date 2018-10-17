import cv2
import numpy as np
from vidstab import layer_blend, layer_overlay


def add_random_circles(img, n=50):
    for _ in range(n):
        color = tuple(np.random.randint(256) for _ in range(3))
        center = (np.random.randint(img.shape[1]), np.random.randint(img.shape[0]))
        radius = np.random.randint(3, 30)
        cv2.circle(img, center, radius, color, -1)


def test_layer_overlay():
    black_frame = np.zeros((100, 200, 3), dtype='uint8')
    rand_frame = black_frame.copy()
    add_random_circles(rand_frame)

    overlay_rand = layer_overlay(black_frame, rand_frame)
    overlay_black = layer_overlay(rand_frame, black_frame)

    if __name__ == '__main__':
        cv2.imshow('rand_frame', rand_frame)
        cv2.imshow('overlay_rand', overlay_rand)
        cv2.imshow('overlay_black', overlay_black)
        cv2.waitKey(0)

    assert np.allclose(overlay_black, black_frame)
    assert np.allclose(overlay_rand, rand_frame)


if __name__ == '__main__':
    test_layer_overlay()
