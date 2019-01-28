import argparse
import warnings
from . import layer_overlay, VidStab


def str_int(v):
    """Handle argparse inputs to that could be str or int

    :param v: value to convert
    :return: v as int if int(v) does not raise ValueError

    >>> str_int('test')
    test
    >>> str_int(1)
    1
    """
    try:
        int_v = int(v)
        return int_v
    except ValueError:
        return v


def str_2_bool(v):
    """Convert string to bool from different possible strings

    :param v: value to convert
    :return: string converted to bool

    >>> str_2_bool('y')
    True
    >>> str_2_bool('0')
    False
    """
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def process_max_frames_arg(max_frames_arg):
    """Handle maxFrames arg in vidstab.__main__

    Convert negative values to inf

    :param max_frames_arg: maxFrames arg in vidstab.__main__
    :return: max_frames as is or inf

    >>> process_max_frames_arg(-1)
    inf
    >>> process_max_frames_arg(1)
    1
    """
    if max_frames_arg > 0:
        return max_frames_arg
    return float('inf')


def process_layer_frames_arg(layer_frames_arg):
    """Handle layerFrames arg in vidstab.__main__

    :param layer_frames_arg: layerFrames arg in vidstab.__main__
    :return: vidstab.layer_overlay if True else None

    >>> process_layer_frames_arg(False)

    """
    if layer_frames_arg:
        return layer_overlay
    return None


def process_border_size_arg(border_size_arg):
    """Handle borderSize arg in vidstab.__main__

    Convert strings that aren't 'auto' to 0

    :param border_size_arg: borderSize arg in vidstab.__main__
    :return: int or 'auto'

    >>> process_border_size_arg('a')
    0
    >>> process_border_size_arg('auto')
    'auto'
    >>> process_border_size_arg(0)
    0
    """
    if isinstance(border_size_arg, str):
        if not border_size_arg == 'auto':
            warnings.warn('Invalid borderSize provided; converting to 0.')
            border_size_arg = 0

    return border_size_arg


def cli_stabilizer(args):
    """Handle CLI vidstab processing

    :param args: result of vars(ap.parse_args()) from vidstab.__main__
    :return: None
    """

    max_frames = process_max_frames_arg(args['maxFrames'])
    border_size = process_border_size_arg(args['borderSize'])
    layer_func = process_layer_frames_arg(args['layerFrames'])

    # init stabilizer with user specified keypoint detector
    stabilizer = VidStab(kp_method=args['keyPointMethod'].upper())
    # stabilize input video and write to specified output file
    stabilizer.stabilize(input_path=args['input'],
                         output_path=args['output'],
                         smoothing_window=args['smoothWindow'],
                         max_frames=max_frames,
                         border_type=args['borderType'],
                         border_size=border_size,
                         layer_func=layer_func,
                         playback=args['playback'])
