# Python Video Stabilization

![](https://img.shields.io/badge/STATUS-UNSTABLE%20(in%20development)-red.svg)

 Python video stabilization using OpenCV. 
 
 This module contains a single class (`VidStab`) used for video stabilization. This class is based on the work presented by Nghia Ho in [SIMPLE VIDEO STABILIZATION USING OPENCV](http://nghiaho.com/?p=2093). The foundation code was found in a comment on Nghia Ho's post by the commenter with username koala.
 
 Input                           |  Output
:-------------------------------:|:-------------------------:
![](readme/input_ostrich.gif)    |  ![](readme/stable_ostrich.gif)
 
## Installation

> ```diff
> - Warning: Code still in development. 
> - 
> - If you install: 
> -      * expect 🐛s
> -      * interface is subject to change
> ```

Currently only available from this repo.  Plan to publish to pypi once stable.

### Install `vidstab` without installing OpenCV

If you've already built OpenCV with python bindings on your machine it is recommended to install `vidstab` without installing the pypi versions of OpenCV.  The `opencv-python` python module can cause issues if you've already built OpenCV from source in your environment.

The below command will install `vidstab` without OpenCV included.

```bash
pip3 install git+https://github.com/AdamSpannbauer/python_video_stab.git
```

### Install `vidstab` & OpenCV

If you don't have OpenCV installed already there are a couple options.  

1. You can build OpenCV using one of the great online tutorials from [PyImageSearch](https://www.pyimagesearch.com/), [LearnOpenCV](https://www.learnopencv.com/), or [OpenCV](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_setup/py_table_of_contents_setup/py_table_of_contents_setup.html#py-table-of-content-setup) themselves.  When building from source you have more options (e.g. [platform optimization](https://www.pyimagesearch.com/2017/10/09/optimizing-opencv-on-the-raspberry-pi/)), but more responsibility.  Once installed you can use the pip install command shown above.
2. You can install a pre-built distribution of OpenCV from pypi as a dependency for `vidstab` (see command below)

The below command will install `vidstab` with `opencv-python` & `opencv-contrib-python` as dependencies.

```bash
 pip3 install -e git+https://github.com/AdamSpannbauer/python_video_stab.git#egg=vidstab[cv2]
```

## Usage

The `VidStab` class can be used as a command line script or in your own custom python code.

### Using from command line

```bash
# Using defaults
python3 -m vidstab --input input_video.mov --output stable_video.avi
```

```bash
# Using a specific keypoint detector
python3 -m vidstab -i input_video.mov -o stable_video.avi -k GFTT
```

### Using `VidStab` class

```python
from vidstab import VidStab

# Using defaults
stabilizer = VidStab()
stabilizer.stabilize(input_path='input_video.mov', output_path='stable_video.avi')

# Using a specific keypoint detector
stabilizer = VidStab(kp_method='ORB')
stabilizer.stabilize(input_path='input_video.mp4', output_path='stable_video.avi')

# Using a specific keypoint detector and customizing keypoint parameters
stabilizer = VidStab(kp_method='FAST', threshold=42, nonmaxSuppression=False)
stabilizer.stabilize(input_path='input_video.mov', output_path='stable_video.avi')
```

### Plotting frame to frame transformations

```python
from vidstab import VidStab
import matplotlib.pyplot as plt

stabilizer = VidStab()
stabilizer.stabilize(input_path='input_video.mov', output_path='stable_video.avi')

stabilizer.plot_trajectory()
plt.show()

stabilizer.plot_transforms()
plt.show()
```

Trajectories                     |  Transforms
:-------------------------------:|:-------------------------:
![](readme/trajectory_plot.png)  |  ![](readme/transforms_plot.png)

### Using borders

```python
from vidstab import VidStab

stabilizer = VidStab()

# black borders
stabilizer.stabilize(input_path='input_video.mov', 
                     output_path='stable_video.avi', 
                     border_type='black')
stabilizer.stabilize(input_path='input_video.mov', 
                     output_path='wide_stable_video.avi', 
                     border_type='black', 
                     border_size=100)

# filled in borders
stabilizer.stabilize(input_path='input_video.mov', 
                     output_path='ref_stable_video.avi', 
                     border_type='reflect')
stabilizer.stabilize(input_path='input_video.mov', 
                     output_path='rep_stable_video.avi', 
                     border_type='replicate')
```

`border_size=0`                  |  `border_size=100`
:-------------------------------:|:-------------------------:
![](readme/stable_ostrich.gif)   |  ![](readme/wide_stable_ostrich.gif)

`border_type='reflect'`                 |  `border_type='replicate'`
:--------------------------------------:|:-------------------------:
![](readme/reflect_stable_ostrich.gif)  |  ![](readme/replicate_stable_ostrich.gif)
