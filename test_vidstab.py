# TODO: implement test to check output values

import unittest
import matplotlib
matplotlib.use('Agg')

from vidstab import VidStab

kp_methods = ["GFTT", "BRISK", "DENSE", "FAST", "HARRIS",
              "MSER", "ORB", "SIFT", "SURF", "STAR"]


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
        input_vid = 'readme/trunc_video.avi'
        output_vid = 'readme/test_output.avi'

        stabilizer = VidStab()
        stabilizer.gen_transforms(input_vid, smoothing_window=1, show_progress=True)

        self.assertEqual(stabilizer.smoothed_trajectory.shape, stabilizer.trajectory.shape,
                         'trajectory/transform obj shapes')
        self.assertEqual(stabilizer.transforms.shape, stabilizer.trajectory.shape,
                         'trajectory/transform obj shapes')

        fig, (ax1, ax2) = stabilizer.plot_transforms()
        self.assertTrue(isinstance(fig, matplotlib.figure.Figure))
        self.assertTrue(isinstance(ax1, matplotlib.axes._subplots.Axes))
        self.assertTrue(isinstance(ax2, matplotlib.axes._subplots.Axes))

        fig, (ax1, ax2) = stabilizer.plot_trajectory()
        self.assertTrue(isinstance(fig, matplotlib.figure.Figure))
        self.assertTrue(isinstance(ax1, matplotlib.axes._subplots.Axes))
        self.assertTrue(isinstance(ax2, matplotlib.axes._subplots.Axes))

        try:
            stabilizer.apply_transforms(input_vid, output_vid)
        except Exception as e:
            self.fail("stabilizer.apply_transforms ran into {}".format(e))

        try:
            stabilizer.stabilize(input_vid, output_vid, smoothing_window=1)
        except Exception as e:
            self.fail("stabilizer.stabilize ran into {}".format(e))


if __name__ == '__main__':
    unittest.main()
