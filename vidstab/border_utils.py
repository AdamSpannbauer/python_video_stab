from .auto_border_utils import auto_border_crop
from .frame import Frame


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


def crop_frame(frame, border_options):
    """Handle frame cropping for auto border size and negative border size

    if auto_border is False and neg_border_size == 0 then frame is returned as is

    :param frame: frame to be cropped
    :param border_options: dictionary of border options including keys for:
        * 'border_size': functional border size determined by functional_border_sizes
        * 'neg_border_size': functional negative border size determined by functional_border_sizes
        * 'extreme_frame_corners': VidStab.extreme_frame_corners attribute
        * 'auto_border': VidStab.auto_border_flag attribute
    :return: cropped frame
    """
    if not border_options['auto_border_flag'] and border_options['neg_border_size'] == 0:
        return frame

    if border_options['auto_border_flag']:
        cropped_frame_image = auto_border_crop(frame.image,
                                               border_options['extreme_frame_corners'],
                                               border_options['border_size'])

    else:
        frame_h, frame_w = frame.image.shape[:2]
        cropped_frame_image = frame.image[
                              border_options['neg_border_size']:(frame_h - border_options['neg_border_size']),
                              border_options['neg_border_size']:(frame_w - border_options['neg_border_size'])
                              ]

    cropped_frame = Frame(cropped_frame_image, color_format=frame.color_format)

    return cropped_frame
