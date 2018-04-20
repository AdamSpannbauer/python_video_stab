# Python Video Stabilization
 Python video stabilization using OpenCV. 
 
 This module contains a single class (`VidStab`) used for video stabilization. This class is based on the work presented by Nghia Ho in [SIMPLE VIDEO STABILIZATION USING OPENCV](http://nghiaho.com/?p=2093). The foundation code was found in a comment on Nghia Ho's post by the commenter with username koala.
 
### Installation

Currently only available from this repo.  Planned to publish to pypi after testing.

##### From repo
```bash
git clone https://github.com/AdamSpannbauer/python_video_stab
cd python_video_stab
pip install .
```

### Example Usage

The `VidStab` class can be used as a command line script or in your own custom python code.

#### Using from command line

```bash
# Using defaults
python3 -m vidstab --input input_video.mov --output stable_video.avi
```

```bash
# Using a specific keypoint detector
python3 -m vidstab -i input_video.mov -o stable_video.avi -k GFTT
```

#### Using `VidStab` class

```python
from vidstab import VidStab

# Using defaults
stabilizer = VidStab()
stabilizer.stabilize(input_path='input_video.mov', output_path='stable_video.avi')

# Using a specific keypoint detector
stabilizer = VidStab(kp_method='ORB')
stabilizer.stabilize(input_path='input_video.mov', output_path='stable_video.avi')

# Using a specific keypoint detector and customizing keypoint parameters
stabilizer = VidStab(kp_method='FAST', threshold=42, nonmaxSuppression=False)
stabilizer.stabilize(input_path='input_video.mov', output_path='stable_video.avi')
```
 
### Example output
<sub>(too shaky for good example, but you get the idea)</sub>

![](readme/example_stab.gif)

video source: [Insane First Person Parkour! (POV/GoPro/Headcam)](https://www.youtube.com/watch?v=_XTPS9hoJRo&t=20s) by [★ EpicMetalPiece / Best Compilations ➥](https://www.youtube.com/channel/UC3jGLyiJS2_Nm1fMfAThdjQ) on [YouTube](https://www.youtube.com/)
