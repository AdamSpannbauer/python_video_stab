"""Use VidStab as command line script

Arguments:
  -i --input
        Path to input video to stabilize.
  -o --output
        Path to save stabilized video.
  -k --keyPointMethod
        Name of keypoint detector to use.

Usage:
    python -m vidstab -i input_video.mov -o stable_video.avi -k GFTT
"""

if __name__ == '__main__':
    import argparse
    from .VidStab import VidStab

    def cvt_input_path(v):
        try:
            int_v = int(v)
            return int_v
        except ValueError:
            return v

    def str_2_bool(v):
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    # construct argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input', type=cvt_input_path, required=True,
                    help='Path to input video to stabilize.')
    ap.add_argument('-o', '--output', required=True,
                    help='Path to save stabilized video.')
    ap.add_argument('-p', '--playback', type=str_2_bool, default='false',
                    help='Should stabilization be played to screen?')
    ap.add_argument('-k', '--keyPointMethod', default='GFTT',
                    help='Name of keypoint detector to use.')
    args = vars(ap.parse_args())

    # init stabilizer with user specified keypoint detector
    stabilizer = VidStab(kp_method=args['keyPointMethod'].upper())
    # stabilize input video and write to specified output file
    stabilizer.stabilize(input_path=args['input'],
                         output_path=args['output'],
                         playback=args['playback'])
