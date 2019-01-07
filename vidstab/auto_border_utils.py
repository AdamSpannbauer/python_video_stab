import math


def auto_border_start(min_corner_point, buffer):
    """Determine upper-right corner coords for auto border crop

    :param min_corner_point: extreme corner component either 'min_x' or 'min_y'
    :param buffer: determined by vidstab process
    :return: adjusted extreme corner for cropping
    """
    return math.floor(buffer - abs(min_corner_point))


def auto_border_size(frame_dim, extreme_corner, buffer):
    """Determine height/width auto border crop

    :param frame_dim: height/width of frame to be auto border cropped (corresponds to extreme_corner)
    :param extreme_corner: extreme corner component either 'min_x' or 'min_y' (corresponds to frame_dim)
    :param buffer: determined by vidstab process
    :return: adjusted extreme corner for cropping
    """
    # Frame dims are counted from 1 but subset is done by indexing at 0
    # Offset by 1 to avoid indexing out of range
    frame_dim = frame_dim - 1
    return math.ceil(frame_dim - (buffer - extreme_corner))


def auto_border_crop(frame, extreme_frame_corners, buffer):
    """Crop frame for auto border in vidstab process

    :param frame: frame to be cropped
    :param extreme_frame_corners: extreme_frame_corners attribute of vidstab object
    :param buffer: determined by vidstab process bordering
    :return: cropped frame determined by auto border process
    """
    frame_h, frame_w = frame.shape[:2]

    x = auto_border_start(extreme_frame_corners['min_x'], buffer)
    y = auto_border_start(extreme_frame_corners['min_y'], buffer)

    w = auto_border_size(frame_w, extreme_frame_corners['max_x'], buffer)
    h = auto_border_size(frame_h, extreme_frame_corners['max_y'], buffer)

    return frame[y:y + h, x:x + w]
