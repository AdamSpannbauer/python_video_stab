import tempfile
import argparse
import pytest
from vidstab import layer_overlay
import vidstab.main_utils as utils
from vidstab.download_videos import download_truncated_ostrich_video


def test_str_int():
    assert utils.str_int('test') == 'test'
    assert utils.str_int(1) == 1


def test_str_2_bool():
    assert utils.str_2_bool('y')
    assert not utils.str_2_bool('0')

    with pytest.raises(argparse.ArgumentTypeError) as err:
        utils.str_2_bool('foo')

    assert 'Boolean value expected.' in str(err.value)


def test_process_max_frames_arg():
    assert utils.process_max_frames_arg(-1) == float('inf')
    assert utils.process_max_frames_arg(1) == 1


def test_process_layer_frames_arg():
    assert utils.process_layer_frames_arg(False) is None
    assert utils.process_layer_frames_arg(True) == layer_overlay


def test_process_border_size_arg():
    with pytest.warns(UserWarning, match='Invalid borderSize provided; converting to 0.'):
        test_value = utils.process_border_size_arg('a')
    assert test_value == 0
    assert utils.process_border_size_arg('auto') == 'auto'
    assert utils.process_border_size_arg(100) == 100


def test_cli_stabilizer():
    """just tests that function runs"""
    tmp_dir = tempfile.TemporaryDirectory()
    truncated_ostrich_video = '{}/trunc_vid.avi'.format(tmp_dir.name)
    download_truncated_ostrich_video(truncated_ostrich_video)

    args = {
        'input': truncated_ostrich_video,
        'output': '{}/output.avi'.format(tmp_dir),
        'playback': False,
        'keyPointMethod': 'GFTT',
        'smoothWindow': 1,
        'maxFrames': -1,
        'borderType': 'black',
        'borderSize': 0,
        'layerFrames': False
    }

    utils.cli_stabilizer(args)
