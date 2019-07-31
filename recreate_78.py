import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', required=True,
                help='Test to mimic vidstab __main__ input')
args = vars(ap.parse_args())

print(args)
print(ap.parse_args())
