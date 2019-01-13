import tempfile
import pytest
import numpy as np
import imutils

from vidstab import VidStab
from vidstab.download_videos import download_ostrich_video, download_truncated_ostrich_video
from .pickled_transforms import download_pickled_transforms, pickle_test_transforms

# excluding non-free "SIFT" & "SURF" methods do to exclusion from opencv-contrib-python
# see: https://github.com/skvark/opencv-python/issues/126
kp_methods = ["GFTT", "BRISK", "DENSE", "FAST", "HARRIS", "MSER", "ORB", "STAR"]

tmp_dir = tempfile.TemporaryDirectory()

truncated_ostrich_video = '{}/trunc_vid.avi'.format(tmp_dir.name)
ostrich_video = '{}/vid.avi'.format(tmp_dir.name)

download_truncated_ostrich_video(truncated_ostrich_video)
download_ostrich_video(ostrich_video)


# test that all keypoint detection methods load without error
def test_default_init():
    for kp in kp_methods:
        print('testing kp method {}'.format(kp))
        assert VidStab(kp_method=kp).kp_method == kp


def test_kp_options():
    stabilizer = VidStab(kp_method='FAST', threshold=42, nonmaxSuppression=False)
    assert not stabilizer.kp_detector.getNonmaxSuppression()
    assert stabilizer.kp_detector.getThreshold() == 42

    with pytest.raises(TypeError) as err:
        VidStab(kp_method='FAST', fake='fake')

    assert 'invalid keyword argument' in str(err.value)


def test_video_dep_funcs_run():
    # just tests to check functions run
    stabilizer = VidStab()
    stabilizer.gen_transforms(truncated_ostrich_video, smoothing_window=2, show_progress=True)

    assert stabilizer.smoothed_trajectory.shape == stabilizer.trajectory.shape
    assert stabilizer.transforms.shape == stabilizer.trajectory.shape

    with tempfile.TemporaryDirectory() as tmpdir:
        output_vid = '{}/test_output.avi'.format(tmpdir)
        stabilizer.apply_transforms(truncated_ostrich_video, output_vid)
        stabilizer.stabilize(truncated_ostrich_video, output_vid, smoothing_window=2)


def test_trajectory_transform_values():
    for window in [15, 30, 60]:
        stabilizer = VidStab()
        stabilizer.gen_transforms(input_path=ostrich_video, smoothing_window=window)

        pickle_test_transforms(stabilizer, 'pickled_transforms')

        unpickled_transforms = download_pickled_transforms(window, cv4=imutils.is_cv4())

        assert np.allclose(stabilizer.transforms, unpickled_transforms[0])
        assert np.allclose(stabilizer.trajectory, unpickled_transforms[1])
        assert np.allclose(stabilizer.smoothed_trajectory, unpickled_transforms[2])
