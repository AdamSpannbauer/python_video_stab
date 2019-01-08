from .auto_border_utils import auto_border_crop


def functional_border_sizes(border_size):
    """Calculate border sizing used in process to gen user specified border size

    If border_size is negative then a stand-in border size is used to allow better keypoint tracking (i think... ?);
    negative border is then applied at end.

    :param border_size: user supplied border size
    :return: (border_size, neg_border_size) tuple of functional border sizes

    >>> functional_border_sizes(100)
    (100, 0)
    >>> functional_border_sizes(-10)
    (100, 110)
    """
    if border_size < 0:
        neg_border_size = 100 + abs(border_size)
        border_size = 100
    else:
        neg_border_size = 0

    return border_size, neg_border_size


def crop_frame(frame, border_size, neg_border_size, extreme_frame_corners, auto_border=False):
    """Handle frame cropping for auto border size and negative border size

    if auto_border is False and neg_border_size == 0 then frame is returned as is

    :param frame: frame to be cropped
    :param border_size: functional border size determined by functional_border_sizes
    :param neg_border_size: functional negative border size determined by functional_border_sizes
    :param extreme_frame_corners: VidStab.extreme_frame_corners attribute
    :param auto_border: VidStab.auto_border_flag attribute
    :return: cropped frame
    """
    if not auto_border and neg_border_size == 0:
        return frame

    if auto_border:
        cropped_frame = auto_border_crop(frame, extreme_frame_corners, border_size)

    else:
        frame_h, frame_w = frame.shape[:2]
        cropped_frame = frame[neg_border_size:(frame_h - neg_border_size),
                              neg_border_size:(frame_w - neg_border_size)]

    return cropped_frame


if __name__ == '__main__':
    import doctest
    doctest.testmod()
