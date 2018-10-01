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
    bar = utils.init_progress_bar(100, float('inf'), show_progress=True, message='Stabilizing')
    assert bar.suffix == '%(percent)d%%'
    assert bar.max == 100
    assert bar.message == 'Stabilizing'

    bar = utils.init_progress_bar(100, 50, show_progress=True, message='Test')
    assert bar.max == 50
    assert bar.message == 'Test'

    bar = utils.init_progress_bar(100, 50, show_progress=False, message='Stabilizing')
    assert bar is None

    bar = utils.init_progress_bar(-1, float('inf'), show_progress=True, message='Stabilizing')
    assert bar is None
