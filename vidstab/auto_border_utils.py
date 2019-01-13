import math
import cv2
import numpy as np
from . import vidstab_utils


def extreme_corners(frame, transforms):
    """Calculate max drift of each frame corner caused by stabilizing transforms

    :param frame: frame from video being stabilized
    :param transforms: VidStab transforms attribute
    :return: dictionary of most extreme x and y values caused by transformations
    """
    h, w = frame.shape[:2]
    frame_corners = np.array([[0, 0],  # top left
                              [0, h - 1],  # bottom left
                              [w - 1, 0],  # top right
                              [w - 1, h - 1]],  # bottom right
                             dtype='float32')
    frame_corners = np.array([frame_corners])

    min_x = min_y = max_x = max_y = 0
    for i in range(transforms.shape[0]):
        transform = transforms[i, :]
        transform_mat = vidstab_utils.build_transformation_matrix(transform)
        transformed_frame_corners = cv2.transform(frame_corners, transform_mat)

        delta_corners = transformed_frame_corners - frame_corners

        delta_y_corners = delta_corners[0][:, 1].tolist()
        delta_x_corners = delta_corners[0][:, 0].tolist()
        min_x = min([min_x] + delta_x_corners)
        min_y = min([min_y] + delta_y_corners)
        max_x = max([max_x] + delta_x_corners)
        max_y = max([max_y] + delta_y_corners)

    return {'min_x': min_x, 'min_y': min_y, 'max_x': max_x, 'max_y': max_y}


def auto_border_start(min_corner_point, border_size):
    """Determine upper-right corner coords for auto border crop

    :param min_corner_point: extreme corner component either 'min_x' or 'min_y'
    :param border_size: min border_size determined by extreme_frame_corners in vidstab process
    :return: adjusted extreme corner for cropping
    """
    return math.floor(border_size - abs(min_corner_point))


def auto_border_length(frame_dim, extreme_corner, border_size):
    """Determine height/width auto border crop

    :param frame_dim: height/width of frame to be auto border cropped (corresponds to extreme_corner)
    :param extreme_corner: extreme corner component either 'min_x' or 'min_y' (corresponds to frame_dim)
    :param border_size: min border_size determined by extreme_frame_corners in vidstab process
    :return: adjusted extreme corner for cropping
    """
    return math.ceil(frame_dim - (border_size - extreme_corner))


def auto_border_crop(frame, extreme_frame_corners, border_size):
    """Crop frame for auto border in vidstab process

    :param frame: frame to be cropped
    :param extreme_frame_corners: extreme_frame_corners attribute of vidstab object
    :param border_size: min border_size determined by extreme_frame_corners in vidstab process
    :return: cropped frame determined by auto border process
    """
    if border_size == 0:
        return frame

    frame_h, frame_w = frame.shape[:2]

    x = auto_border_start(extreme_frame_corners['min_x'], border_size)
    y = auto_border_start(extreme_frame_corners['min_y'], border_size)

    w = auto_border_length(frame_w, extreme_frame_corners['max_x'], border_size)
    h = auto_border_length(frame_h, extreme_frame_corners['max_y'], border_size)

    return frame[y:h, x:w]


def min_auto_border_size(extreme_frame_corners):
    """Calc minimum border size to accommodate most extreme transforms

    :param extreme_frame_corners: extreme_frame_corners attribute of vidstab object
    :return: minimum border size as int
    """
    abs_extreme_corners = [abs(x) for x in extreme_frame_corners.values()]
    return math.ceil(max(abs_extreme_corners))
