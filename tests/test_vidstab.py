import os
import tempfile
import cv2
import imutils
import imutils.video
import numpy as np
import pytest

from vidstab import VidStab
from vidstab.download_videos import download_ostrich_video, download_truncated_ostrich_video
from .pickled_transforms import download_pickled_transforms, pickle_test_transforms

# atol value to use when comparing results using np.allclose
NP_ALLCLOSE_ATOL = 1e-3

# excluding non-free 'SIFT' & 'SURF' methods due to exclusion from opencv-contrib-python
# see: https://github.com/skvark/opencv-python/issues/126
KP_METHODS = ['GFTT', 'BRISK', 'DENSE', 'FAST', 'HARRIS', 'MSER', 'ORB', 'STAR']

tmp_dir = tempfile.TemporaryDirectory()
TRUNCATED_OSTRICH_VIDEO = '{}/trunc_vid.avi'.format(tmp_dir.name)
OSTRICH_VIDEO = '{}/vid.avi'.format(tmp_dir.name)

download_truncated_ostrich_video(TRUNCATED_OSTRICH_VIDEO)
download_ostrich_video(OSTRICH_VIDEO)


# test that all keypoint detection methods load without error
def test_default_init():
    for kp in KP_METHODS:
        print('testing kp method {}'.format(kp))
        assert VidStab(kp_method=kp).kp_method == kp


def test_kp_options():
    stabilizer = VidStab(kp_method='FAST', threshold=42, nonmaxSuppression=False)
    assert not stabilizer.kp_detector.getNonmaxSuppression()
    assert stabilizer.kp_detector.getThreshold() == 42

    with pytest.raises(TypeError) as err:
        VidStab(kp_method='FAST', fake='fake')

    assert 'invalid keyword argument' in str(err.value)


def test_invalid_input_path():
    stabilizer = VidStab(kp_method='FAST', threshold=42, nonmaxSuppression=False)
    with pytest.raises(FileNotFoundError) as err:
        stabilizer.gen_transforms('fake_input_path.mp4')

    assert 'fake_input_path.mp4 does not exist' in str(err.value)

    with pytest.raises(FileNotFoundError) as err:
        stabilizer.stabilize('fake_input_path.mp4', 'output.avi')

    assert 'fake_input_path.mp4 does not exist' in str(err.value)

    with pytest.raises(ValueError) as err:
        tmp_file = tempfile.NamedTemporaryFile(suffix='.mp4')
        with pytest.warns(UserWarning, match='No progress bar will be shown'):
            stabilizer.stabilize(tmp_file.name, 'output.avi')

    assert 'First frame is None' in str(err.value)


def test_video_dep_funcs_run():
    # just tests to check functions run
    stabilizer = VidStab()
    stabilizer.gen_transforms(TRUNCATED_OSTRICH_VIDEO, smoothing_window=2, show_progress=True)

    assert stabilizer.smoothed_trajectory.shape == stabilizer.trajectory.shape
    assert stabilizer.transforms.shape == stabilizer.trajectory.shape

    with tempfile.TemporaryDirectory() as tmpdir:
        output_vid = '{}/test_output.avi'.format(tmpdir)
        stabilizer.apply_transforms(TRUNCATED_OSTRICH_VIDEO, output_vid)
        stabilizer.stabilize(TRUNCATED_OSTRICH_VIDEO, output_vid, smoothing_window=2)


def check_transforms(stabilizer, is_cv4=True):
    # noinspection PyProtectedMember
    unpickled_transforms = download_pickled_transforms(stabilizer._smoothing_window, cv4=is_cv4)

    assert np.allclose(stabilizer.transforms, unpickled_transforms[0], atol=NP_ALLCLOSE_ATOL)
    assert np.allclose(stabilizer.trajectory, unpickled_transforms[1], atol=NP_ALLCLOSE_ATOL)
    assert np.allclose(stabilizer.smoothed_trajectory, unpickled_transforms[2], atol=NP_ALLCLOSE_ATOL)


def test_trajectory_transform_values():
    for window in [15, 30, 60]:
        stabilizer = VidStab(processing_max_dim=float('inf'))
        stabilizer.stabilize(input_path=OSTRICH_VIDEO, output_path='stable.avi', smoothing_window=window)

        pickle_test_transforms(stabilizer, 'pickled_transforms')

        check_transforms(stabilizer, is_cv4=imutils.is_cv4())


def test_stabilize_frame():
    # Init stabilizer and video reader
    stabilizer = VidStab(processing_max_dim=float('inf'))
    vidcap = cv2.VideoCapture(OSTRICH_VIDEO)

    window_size = 30
    while True:
        _, frame = vidcap.read()

        # Pass frame to stabilizer even if frame is None
        stabilized_frame = stabilizer.stabilize_frame(input_frame=frame,
                                                      smoothing_window=window_size,
                                                      border_size=10)

        if stabilized_frame is None:
            break

    check_transforms(stabilizer, is_cv4=imutils.is_cv4())


def test_resize():
    # Init stabilizer and video reader
    max_dim = 30
    stabilizer = VidStab(processing_max_dim=max_dim)
    assert stabilizer.processing_max_dim == max_dim

    # noinspection PyProtectedMember
    assert stabilizer._processing_resize_kwargs == {}

    vidcap = cv2.VideoCapture(OSTRICH_VIDEO)

    _, frame = vidcap.read()
    _ = stabilizer.stabilize_frame(input_frame=frame, smoothing_window=1)

    _, frame = vidcap.read()
    stabilized_frame = stabilizer.stabilize_frame(input_frame=frame, smoothing_window=1)

    assert stabilized_frame.shape == (446, 876, 3)
    assert max(stabilizer.prev_gray.shape) <= max_dim

    # noinspection PyProtectedMember
    assert stabilizer._processing_resize_kwargs == {'width': max_dim}


def test_writer_reset():
    with tempfile.TemporaryDirectory() as tmpdir:
        path_1 = '{}/stable_1.avi'.format(tmpdir)
        path_2 = '{}/stable_2.avi'.format(tmpdir)

        stabilizer = VidStab()
        stabilizer.stabilize(OSTRICH_VIDEO, path_1, max_frames=16, smoothing_window=1)
        stabilizer.stabilize(OSTRICH_VIDEO, path_2, max_frames=16, smoothing_window=1)

        assert os.path.exists(path_1)
        assert os.path.exists(path_2)

        imutils.video.count_frames(path_1)


def test_output_fps():
    force_fps = 10
    with tempfile.TemporaryDirectory() as tmpdir:
        output_vid = '{}/test_output.avi'.format(tmpdir)

        stabilizer = VidStab()
        stabilizer.stabilize(
            OSTRICH_VIDEO,
            output_vid,
            max_frames=16,
            smoothing_window=1,
            output_fps=force_fps
        )

        output_fps = cv2.VideoCapture(output_vid).get(cv2.CAP_PROP_FPS)
        assert force_fps == output_fps


def test_max_frames():
    max_frames = 16
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = '{}/stable_1.avi'.format(tmpdir)

        stabilizer = VidStab()
        stabilizer.stabilize(OSTRICH_VIDEO, output_path, max_frames=max_frames, smoothing_window=1)

        output_frame_count = imutils.video.count_frames(output_path)
        assert max_frames == output_frame_count
