import numpy as np
import pytest

from vidstab.frame import Frame
from vidstab.border_utils import functional_border_sizes, crop_frame


def test_functional_border_sizes():
    assert (100, 0) == functional_border_sizes(100)
    assert (100, 110) == functional_border_sizes(-10)


def test_crop_frame():
    black_frame_image = np.zeros((100, 200, 3), dtype='uint8')
    black_frame = Frame(black_frame_image)
    border_options = {
        'neg_border_size': 10,
        'auto_border_flag': False
    }

    cropped_frame = crop_frame(black_frame, border_options)
    assert cropped_frame.image.shape == (80, 180, 3)

    border_options['neg_border_size'] = 0
    cropped_frame = crop_frame(black_frame, border_options)
    assert cropped_frame.image.shape == (100, 200, 3)

    border_options['auto_border_flag'] = True
    with pytest.raises(KeyError) as err:
        crop_frame(black_frame, border_options)

    assert 'extreme_frame_corners' in str(err.value)
