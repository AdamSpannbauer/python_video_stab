# Python Video Stabilization 

<img src='https://github.com/AdamSpannbauer/python_video_stab/blob/master/readme/vidstab_logo.png?raw=true' width=125 align='right'/>

![](https://img.shields.io/badge/Lifecycle-Maturing-yellow.svg) [![Build Status](https://travis-ci.org/AdamSpannbauer/python_video_stab.svg?branch=master)](https://travis-ci.org/AdamSpannbauer/python_video_stab) [![PyPi version](https://pypip.in/v/vidstab/badge.png)](https://crate.io/packages/vidstab/)

 Python video stabilization using OpenCV. 
 
 This module contains a single class (`VidStab`) used for video stabilization. This class is based on the work presented by Nghia Ho in [SIMPLE VIDEO STABILIZATION USING OPENCV](http://nghiaho.com/?p=2093). The foundation code was found in a comment on Nghia Ho's post by the commenter with username koala.
 
 Input                           |  Output
:-------------------------------:|:-------------------------:
![](https://github.com/AdamSpannbauer/python_video_stab/blob/master/readme/input_ostrich.gif?raw=true)    |  ![](https://github.com/AdamSpannbauer/python_video_stab/blob/master/readme/stable_ostrich.gif?raw=true)
 
## Installation

> ```diff
> + Please report issues if you install/try to install and run into problems!
> ```

### Install `vidstab` without installing OpenCV

If you've already built OpenCV with python bindings on your machine it is recommended to install `vidstab` without installing the pypi versions of OpenCV.  The `opencv-python` python module can cause issues if you've already built OpenCV from source in your environment.

The below commands will install `vidstab` without OpenCV included.

#### From PyPi

```bash
pip install vidstab
```

#### From Github

```bash
pip install git+https://github.com/AdamSpannbauer/python_video_stab.git
```

### Install `vidstab` & OpenCV

If you don't have OpenCV installed already there are a couple options.  

1. You can build OpenCV using one of the great online tutorials from [PyImageSearch](https://www.pyimagesearch.com/), [LearnOpenCV](https://www.learnopencv.com/), or [OpenCV](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_setup/py_table_of_contents_setup/py_table_of_contents_setup.html#py-table-of-content-setup) themselves.  When building from source you have more options (e.g. [platform optimization](https://www.pyimagesearch.com/2017/10/09/optimizing-opencv-on-the-raspberry-pi/)), but more responsibility.  Once installed you can use the pip install command shown above.
2. You can install a pre-built distribution of OpenCV from pypi as a dependency for `vidstab` (see command below)

The below commands will install `vidstab` with `opencv-contrib-python` as dependencies.

#### From PyPi

```bash
pip install vidstab[cv2]
```

#### From Github

```bash
 pip install -e git+https://github.com/AdamSpannbauer/python_video_stab.git#egg=vidstab[cv2]
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
![](https://github.com/AdamSpannbauer/python_video_stab/blob/master/readme/trajectory_plot.png?raw=true)  |  ![](https://github.com/AdamSpannbauer/python_video_stab/blob/master/readme/transforms_plot.png?raw=true)

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
![](https://github.com/AdamSpannbauer/python_video_stab/blob/master/readme/stable_ostrich.gif?raw=true)   |  ![](https://github.com/AdamSpannbauer/python_video_stab/blob/master/readme/wide_stable_ostrich.gif?raw=true)

`border_type='reflect'`                 |  `border_type='replicate'`
:--------------------------------------:|:-------------------------:
![](https://github.com/AdamSpannbauer/python_video_stab/blob/master/readme/reflect_stable_ostrich.gif?raw=true)  |  ![](https://github.com/AdamSpannbauer/python_video_stab/blob/master/readme/replicate_stable_ostrich.gif?raw=true)

### Using Frame Layering

```python
from vidstab import VidStab, layer_overlay, layer_blend

# init vid stabilizer
stabilizer = VidStab()

# use vidstab.layer_overlay for generating a trail effect
stabilizer.stabilize(input_path=input_vid,
                     output_path='trail_stable_video.avi',
                     border_type='black',
                     border_size=100,
                     layer_func=layer_overlay)


# create custom overlay function
# here we use vidstab.layer_blend with custom alpha
#   layer_blend will generate a fading trail effect with some motion blur
def layer_custom(foreground, background):
    return layer_blend(foreground, background, foreground_alpha=.8)

# use custom overlay function
stabilizer.stabilize(input_path=input_vid,
                     output_path='blend_stable_video.avi',
                     border_type='black',
                     border_size=100,
                     layer_func=layer_custom)
```

`layer_func=vidstab.layer_overlay`     |  `layer_func=vidstab.layer_blend`
:--------------------------------------:|:-------------------------:
![](https://discourse-cdn-sjc2.com/standard16/uploads/pyimagesearch/original/2X/b/bf2996f1d2ae18801e40838c89c08ad0d30cfdc9.gif)  |  ![](https://discourse-cdn-sjc2.com/standard16/uploads/pyimagesearch/original/2X/f/f688787217fac5f1b5e7597a55ff063cc1fbd544.gif)
