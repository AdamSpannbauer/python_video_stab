# TODO: write legitimate tests

import tempfile
import unittest
import pickle
from urllib.request import urlopen, urlretrieve
import numpy as np
from vidstab import VidStab

kp_methods = ["GFTT", "BRISK", "DENSE", "FAST", "HARRIS",
              "MSER", "ORB", "SIFT", "SURF", "STAR"]

tmp_dir = tempfile.TemporaryDirectory()

remote_trunc_vid = 'https://s3.amazonaws.com/python-vidstab/trunc_video.avi'
remote_vid = 'https://s3.amazonaws.com/python-vidstab/ostrich.mp4'

local_trunc_vid = '{}/trunc_vid.avi'.format(tmp_dir.name)
local_vid = '{}/vid.avi'.format(tmp_dir.name)

urlretrieve(remote_trunc_vid, local_trunc_vid)
urlretrieve(remote_vid, local_vid)


class KeyPointMethods(unittest.TestCase):

    # test that all keypoint detection methods load without error
    def test_default_init(self):
        for kp in kp_methods:
            print('testing kp method {}'.format(kp))
            self.assertEqual(VidStab(kp_method=kp).kp_method, kp, '{} kp init'.format(kp))

    def test_kp_options(self):
        stabilizer = VidStab(kp_method='FAST', threshold=42, nonmaxSuppression=False)
        self.assertFalse(stabilizer.kp_detector.getNonmaxSuppression(), 'FAST kp non-max suppression flag')
        self.assertEqual(stabilizer.kp_detector.getThreshold(), 42, 'FAST kp custom threshold')

        with self.assertRaises(TypeError) as err:
            VidStab(kp_method='FAST', fake='fake')
        self.assertTrue(isinstance(err.exception, TypeError), 'reject bad kwargs')

    def test_video_dep_funcs_run(self):
        # just tests to check functions run
        # input_vid = 'https://s3.amazonaws.com/python-vidstab/trunc_video.avi'
        input_vid = local_trunc_vid

        stabilizer = VidStab()
        stabilizer.gen_transforms(input_vid, smoothing_window=1, show_progress=True)

        self.assertEqual(stabilizer.smoothed_trajectory.shape, stabilizer.trajectory.shape,
                         'trajectory/transform obj shapes')
        self.assertEqual(stabilizer.transforms.shape, stabilizer.trajectory.shape,
                         'trajectory/transform obj shapes')

        with tempfile.TemporaryDirectory() as tmpdir:
            output_vid = '{}/test_output.avi'.format(tmpdir)
            try:
                stabilizer.apply_transforms(input_vid, output_vid)
            except Exception as e:
                self.fail("stabilizer.apply_transforms ran into {}".format(e))

            try:
                stabilizer.stabilize(input_vid, output_vid, smoothing_window=1)
            except Exception as e:
                self.fail("stabilizer.stabilize ran into {}".format(e))

    def test_trajectory_transform_values(self):
        # input_vid = 'https://s3.amazonaws.com/python-vidstab/ostrich.mp4'
        input_vid = local_vid
        base_url = 'https://s3.amazonaws.com/python-vidstab'
        stabilizer = VidStab()

        for window in [15, 30, 60]:
            stabilizer.gen_transforms(input_path=input_vid, smoothing_window=window)

            transform_file = '{}/ostrich_transforms_{}.pickle'.format(base_url, window)
            trajectory_file = '{}/ostrich_trajectory_{}.pickle'.format(base_url, window)
            smooth_trajectory_file = '{}/ostrich_smooth_trajectory_{}.pickle'.format(base_url, window)

            with urlopen(transform_file) as f:
                expected_transforms = pickle.load(f)
            with urlopen(trajectory_file) as f:
                expected_trajectory = pickle.load(f)
            with urlopen(smooth_trajectory_file) as f:
                expected_smooth_trajectory = pickle.load(f)

            self.assertTrue(np.allclose(stabilizer.transforms, expected_transforms))
            self.assertTrue(np.allclose(stabilizer.trajectory, expected_trajectory))
            self.assertTrue(np.allclose(stabilizer.smoothed_trajectory, expected_smooth_trajectory))


if __name__ == '__main__':
    unittest.main()
