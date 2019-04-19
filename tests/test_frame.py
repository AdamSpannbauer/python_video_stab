import pytest
import numpy as np
from vidstab.frame import Frame


GRAY_FRAME_IMAGE = np.zeros((1, 1), dtype='uint8')
BGR_FRAME_IMAGE = np.zeros((1, 1, 3), dtype='uint8')
BGRA_FRAME_IMAGE = np.array([[[0, 0, 0, 255]]], dtype='uint8')


def test_set_color_format():
    frame_gray = Frame(GRAY_FRAME_IMAGE)
    frame_bgr = Frame(BGR_FRAME_IMAGE)
    frame_bgra = Frame(BGRA_FRAME_IMAGE)
    frame_fake = Frame(np.zeros((1, 2)), color_format='fake')

    assert frame_gray.color_format == 'GRAY'
    assert frame_bgr.color_format == 'BGR'
    assert frame_bgra.color_format == 'BGRA'
    assert frame_fake.color_format == 'fake'

    with pytest.raises(ValueError) as err:
        Frame(np.zeros((1, 2, 42)))

    assert 'Unexpected frame image shape: (1, 2, 42)' in str(err.value)


def test_cvt_color():
    frame_gray = Frame(GRAY_FRAME_IMAGE)
    frame_bgr = Frame(BGR_FRAME_IMAGE)
    frame_bgra = Frame(BGRA_FRAME_IMAGE)

    assert np.alltrue(frame_gray.image == frame_gray.gray_image)
    assert np.alltrue(frame_gray.image == frame_bgr.gray_image)
    assert np.alltrue(frame_gray.image == frame_bgra.gray_image)

    assert np.alltrue(frame_bgr.image == frame_gray.bgr_image)
    assert np.alltrue(frame_bgr.image == frame_bgr.bgr_image)
    assert np.alltrue(frame_bgr.image == frame_bgra.bgr_image)

    assert np.alltrue(frame_bgra.image == frame_gray.bgra_image)
    assert np.alltrue(frame_bgra.image == frame_bgr.bgra_image)
    assert np.alltrue(frame_bgra.image == frame_bgra.bgra_image)
