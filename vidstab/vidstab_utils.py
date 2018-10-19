import cv2
import numpy as np


def build_transformation_matrix(transform):
    """Convert transform list to transformation matrix

    :param transform: transform list as [dx, dy, da]
    :return: transform matrix as 2d (2, 3) numpy array
    """
    transform_matrix = np.zeros((2, 3))

    transform_matrix[0, 0] = np.cos(transform[2])
    transform_matrix[0, 1] = -np.sin(transform[2])
    transform_matrix[1, 0] = np.sin(transform[2])
    transform_matrix[1, 1] = np.cos(transform[2])
    transform_matrix[0, 2] = transform[0]
    transform_matrix[1, 2] = transform[1]

    return transform_matrix


def border_frame(frame, border_size, border_type):
    """Convenience wrapper of cv2.copyMakeBorder for how vidstab applies borders

    :param frame: frame to apply border to
    :param border_size: int border size in number of pixels
    :param border_type: one of the following ['black', 'reflect', 'replicate']
    :return: bordered version of frame
    """
    border_modes = {'black': cv2.BORDER_CONSTANT,
                    'reflect': cv2.BORDER_REFLECT,
                    'replicate': cv2.BORDER_REPLICATE}
    border_mode = border_modes[border_type]

    bordered_frame = cv2.copyMakeBorder(frame,
                                        top=border_size,
                                        bottom=border_size,
                                        left=border_size,
                                        right=border_size,
                                        borderType=border_mode,
                                        value=[0, 0, 0])

    alpha_bordered_frame = cv2.cvtColor(bordered_frame, cv2.COLOR_BGR2BGRA)
    alpha_bordered_frame[:, :, 3] = 0
    h, w = frame.shape[:2]
    alpha_bordered_frame[border_size:border_size + h, border_size:border_size + w, 3] = 255

    return alpha_bordered_frame, border_mode


def match_keypoints(optical_flow, prev_kps):
    """Match optical flow keypoints

    :param optical_flow: output of cv2.calcOpticalFlowPyrLK
    :param prev_kps: keypoints that were passed to cv2.calcOpticalFlowPyrLK to create optical_flow
    :return: tuple of (cur_matched_kp, prev_matched_kp)
    """
    cur_kps, status, err = optical_flow

    # storage for keypoints with status 1
    prev_matched_kp = []
    cur_matched_kp = []
    for i, matched in enumerate(status):
        # store coords of keypoints that appear in both
        if matched:
            prev_matched_kp.append(prev_kps[i])
            cur_matched_kp.append(cur_kps[i])

    return cur_matched_kp, prev_matched_kp


def estimate_partial_transform(matched_keypoints):
    """Wrapper of cv2.estimateRigidTransform for convenience in vidstab process

    :param matched_keypoints: output of match_keypoints util function; tuple of (cur_matched_kp, prev_matched_kp)
    :return: transform as list of [dx, dy, da]
    """
    cur_matched_kp, prev_matched_kp = matched_keypoints

    transform = cv2.estimateRigidTransform(np.array(prev_matched_kp),
                                           np.array(cur_matched_kp),
                                           False)
    if transform is not None:
        # translation x
        dx = transform[0, 2]
        # translation y
        dy = transform[1, 2]
        # rotation
        da = np.arctan2(transform[1, 0], transform[0, 0])
    else:
        dx = dy = da = 0

    return [dx, dy, da]
