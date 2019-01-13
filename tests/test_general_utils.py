import pytest
import numpy as np

import vidstab.general_utils as utils


def test_bfill_rolling_mean():
    test_arr = np.array([[1, 2, 3], [4, 5, 6]])

    assert np.allclose(utils.bfill_rolling_mean(test_arr, n=1), test_arr)
    assert np.allclose(utils.bfill_rolling_mean(test_arr, n=2),
                       np.array([[2.5, 3.5, 4.5],
                                 [2.5, 3.5, 4.5]]))

    with pytest.raises(ValueError) as err:
        utils.bfill_rolling_mean(test_arr, n=3)

    assert 'arr.shape[0] cannot be less than n' in str(err.value)


def test_init_progress_bar():
    bar = utils.init_progress_bar(100, float('inf'), show_progress=True, gen_all=False)
    assert bar.suffix == '%(percent)d%%'
    assert bar.max == 100
    assert bar.message == 'Stabilizing'

    bar = utils.init_progress_bar(100, 50, show_progress=True, gen_all=True)
    assert bar.max == 50
    assert bar.message == 'Generating Transforms'

    bar = utils.init_progress_bar(100, 50, show_progress=False)
    assert bar is None

    with pytest.warns(UserWarning, match='No progress bar will be shown.'):
        bar = utils.init_progress_bar(-1, float('inf'), show_progress=True)
    assert bar is None


def update_progress_bar():
    bar = utils.init_progress_bar(100, float('inf'))

    utils.update_progress_bar(bar)
    assert bar.percent == 1.0

    utils.update_progress_bar(bar, show_progress=False)
    assert bar.percent == 1.0

    utils.update_progress_bar(bar, finish=True)
    assert bar.percent == 2.0


def test_playback_video():
    break_playback = utils.playback_video(display_frame=None,
                                          playback_flag=False,
                                          delay=None)

    assert not break_playback
