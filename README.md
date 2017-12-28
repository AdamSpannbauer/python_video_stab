# Python Video Stabilization
 Python video stabilization script using OpenCV. 
 
 This is a translation of [the C++ script](http://nghiaho.com/uploads/code/videostab.cpp
) provided in [SIMPLE VIDEO STABILIZATION USING OPENCV](http://nghiaho.com/?p=2093) by NGHIAHO12.
 
 I did not write this code.  The code was found in the comments section of the linked blog entry.  The commenter who posted the code was koala.  I have made some modifications to koala's original code (i.e. formating, adding some arguments/features, commenting).
 
### Example output
too shaky for good example, but you get the idea

![](example_stab.gif)

video source: [Insane First Person Parkour! (POV/GoPro/Headcam)](https://www.youtube.com/watch?v=_XTPS9hoJRo&t=20s) by [★ EpicMetalPiece / Best Compilations ➥](https://www.youtube.com/channel/UC3jGLyiJS2_Nm1fMfAThdjQ) on [YouTube](https://www.youtube.com/)

<br><hr><br>

![](example_stab_mango.gif)

video source: [Mango vs Plup - Singles LB QF - Smash Summit 2](https://www.youtube.com/watch?v=YpQTH7b-3jg) by [Beyond the Summit - Smash](https://www.youtube.com/channel/UCKJi-4lbB3EwpLpC82OWFjA) on [YouTube](https://www.youtube.com/)

### Usage

`python python_video_stab.py --video input_video.mov --output output_dir --compareOutput 1 --maxWidth 400`

##### Arguments

 * `--video`          (`-v`) video file to stabilize (i.e. my_video.mp4)
 * `--output`         (`-o`) path to dir to save output files
 * `--compareOutput`  (`-c`) should output video be side by side comparison of input & output videos (as shown in readme). If `0` the output video will only contain the stabilized video; if `>0` the output will be the comparison
 * `--maxWidth`       (`-w`) max width of output video in pixels; if `compareOutput > 0` then output width will be `2 * maxWidth`

##### Outputs

 * Stabilzed video file as a .avi
 * .csv of the transformations used during stabilization
 * .csv of the smoothed trajectory used during stabilization
