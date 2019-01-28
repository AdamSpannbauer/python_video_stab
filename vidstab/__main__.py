"""Use VidStab as command line script

usage: python -m vidstab [-h] -i INPUT -o OUTPUT [-p PLAYBACK] [-k KEYPOINTMETHOD]
                   [-s SMOOTHWINDOW] [-m MAXFRAMES] [-b BORDERTYPE]
                   [-z BORDERSIZE] [-l LAYERFRAMES]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to input video to stabilize.
  -o OUTPUT, --output OUTPUT
                        Path to save stabilized video.
  -p PLAYBACK, --playback PLAYBACK
                        Should stabilization be played to screen? (y/n)
  -k KEYPOINTMETHOD, --keyPointMethod KEYPOINTMETHOD
                        Name of keypoint detector to use.
  -s SMOOTHWINDOW, --smoothWindow SMOOTHWINDOW
                        Smoothing window to use while smoothing frame
                        transforms.
  -m MAXFRAMES, --maxFrames MAXFRAMES
                        Max frames to process in video. Negative values will
                        not apply limit.
  -b BORDERTYPE, --borderType BORDERTYPE
                        How to fill in empty border caused by frame shifting.
                        Options: ['black', 'reflect', 'replicate']
  -z BORDERSIZE, --borderSize BORDERSIZE
                        If positive, borderType is added equal to borderSize.
                        If negative, cropping is applied. If 'auto', auto
                        sizing is used to fit transformations.
  -l LAYERFRAMES, --layerFrames LAYERFRAMES
                        Should frame layering effect be applied to output
                        video? (y/n)
"""

if __name__ == '__main__':
    import argparse
    from .main_utils import cli_stabilizer, str_int, str_2_bool

    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input', type=str_int, required=True,
                    help='Path to input video to stabilize.')
    ap.add_argument('-o', '--output', required=True,
                    help='Path to save stabilized video.')
    ap.add_argument('-p', '--playback', type=str_2_bool, default='false',
                    help='Should stabilization be played to screen? (y/n)')
    ap.add_argument('-k', '--keyPointMethod', default='GFTT',
                    help='Name of keypoint detector to use.')

    ap.add_argument('-s', '--smoothWindow', default=30, type=int,
                    help='Smoothing window to use while smoothing frame transforms.')
    ap.add_argument('-m', '--maxFrames', default=-1, type=int,
                    help='Max frames to process in video. Negative values will not apply limit.')
    ap.add_argument('-b', '--borderType', default='black',
                    help="How to fill in empty border caused by frame shifting. "
                         "Options: ['black', 'reflect', 'replicate']")
    ap.add_argument('-z', '--borderSize', default=0, type=str_int,
                    help="If positive, borderType is added equal to borderSize. "
                         "If negative, cropping is applied. "
                         "If 'auto', auto sizing is used to fit transformations.")
    ap.add_argument('-l', '--layerFrames', type=str_2_bool, default='false',
                    help='Should frame layering effect be applied to output video? (y/n)')
    args = vars(ap.parse_args())

    cli_stabilizer(args)
