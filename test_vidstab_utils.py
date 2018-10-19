import pytest
import numpy as np
import cv2
import vidstab.vidstab_utils as utils
import imutils.feature.factories as kp_factory

kp_detector = kp_factory.FeatureDetector_create('GFTT')
frame_1 = np.zeros((200, 200, 3), dtype='uint8')
frame_2 = np.zeros((200, 200, 3), dtype='uint8')

cv2.rectangle(frame_1, (20, 50), (100, 100), (255, 0, 0), -1)
cv2.rectangle(frame_2, (50, 80), (130, 130), (255, 0, 0), -1)

frame_1_gray = cv2.cvtColor(frame_1, cv2.COLOR_BGR2GRAY)
frame_2_gray = cv2.cvtColor(frame_2, cv2.COLOR_BGR2GRAY)
frame_1_kps = kp_detector.detect(frame_1_gray)
frame_1_kps = np.array([kp.pt for kp in frame_1_kps], dtype='float32').reshape(-1, 1, 2)

optical_flow = cv2.calcOpticalFlowPyrLK(frame_1_gray,
                                        frame_2_gray,
                                        frame_1_kps,
                                        None)


def test_build_transformation_matrix():
    expected = np.array([[-0.83907153, -0.54402111,  1.0],
                         [0.54402111, -0.83907153,  2.0]])
    assert np.allclose(utils.build_transformation_matrix([1, 2, -10]), expected)

    expected = np.array([[1.0, 0.0,  0.0],
                         [0.0, 1.0,  0.0]])
    assert np.allclose(utils.build_transformation_matrix([0, 0, 0]), expected)


def test_border_frame():
    frame = np.zeros((10, 10, 3), dtype='uint8')

    bordered_frame, border_mode = utils.border_frame(frame, border_size=100, border_type='black')
    assert bordered_frame.shape == (210, 210, 4)
    assert border_mode == 0

    bordered_frame, border_mode = utils.border_frame(frame, border_size=100, border_type='replicate')
    assert bordered_frame.shape == (210, 210, 4)
    assert border_mode == 1

    bordered_frame, border_mode = utils.border_frame(frame, border_size=100, border_type='reflect')
    assert bordered_frame.shape == (210, 210, 4)
    assert border_mode == 2

    with pytest.raises(KeyError) as err:
        utils.border_frame(frame, border_size=100, border_type='fake')

    assert 'fake' in str(err.value)


def test_match_keypoints():
    cur_matched_kps, prev_matched_kps = utils.match_keypoints(optical_flow, frame_1_kps)

    cur_matched_kps = [np.rint(x).astype('int').tolist() for x in cur_matched_kps]
    prev_matched_kps = [np.rint(x).astype('int').tolist() for x in prev_matched_kps]

    assert cur_matched_kps == [[[130, 130]], [[50, 130]], [[130, 80]], [[50, 80]]]
    assert prev_matched_kps == [[[100, 100]], [[20, 100]], [[100, 50]], [[20, 50]]]


def test_estimate_partial_transform():
    expected = [29.999978200505126, 29.999898169013868, 1.0278229229761564e-06]

    matched_keypoints = utils.match_keypoints(optical_flow, frame_1_kps)
    partial_transform = utils.estimate_partial_transform(matched_keypoints)

    assert np.allclose(partial_transform, expected)


if __name__ == '__main__':
    test_border_frame()
