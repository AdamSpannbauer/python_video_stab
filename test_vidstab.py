import unittest
from vidstab import VidStab

kp_methods = ["GFTT", "BRISK", "DENSE", "FAST", "HARRIS",
              "MSER", "ORB", "SIFT", "SURF", "STAR"]


class KeyPointMethods(unittest.TestCase):

    # test that all keypoint detection methods load without error
    def test_loading_kp_methods(self):
        for kp in kp_methods:
            print('testing kp method {}'.format(kp))
            self.assertEqual(VidStab(kp_method=kp).kp_method, kp)


if __name__ == '__main__':
    unittest.main()
