import unittest
import numpy as np
import vidstab.utils as utils


class UtilTests(unittest.TestCase):
    def test_bfill_rolling_mean(self):
        test_arr = np.array([[1, 2, 3], [4, 5, 6]])

        self.assertTrue(np.allclose(utils.bfill_rolling_mean(test_arr, n=1), test_arr))
        self.assertTrue(np.allclose(utils.bfill_rolling_mean(test_arr, n=2),
                                    np.array([[2.5, 3.5, 4.5],
                                              [2.5, 3.5, 4.5]])))

        with self.assertRaises(ValueError) as err:
            utils.bfill_rolling_mean(test_arr, n=3)
        self.assertTrue(isinstance(err.exception, ValueError), 'reject when n > arr.shape[0]')

    def test_init_progress_bar(self):
        bar = utils.init_progress_bar(100, float('inf'), show_progress=True, message='Stabilizing')
        self.assertEqual(bar.suffix, '%(percent)d%%')
        self.assertEqual(bar.max, 100)
        self.assertEqual(bar.message, 'Stabilizing')

        bar = utils.init_progress_bar(100, 50, show_progress=True, message='Test')
        self.assertEqual(bar.max, 50)
        self.assertEqual(bar.message, 'Test')

        bar = utils.init_progress_bar(100, 50, show_progress=False, message='Stabilizing')
        self.assertEqual(bar, None)

        bar = utils.init_progress_bar(-1, float('inf'), show_progress=True, message='Stabilizing')
        self.assertEqual(bar, None)


if __name__ == '__main__':
    unittest.main()
