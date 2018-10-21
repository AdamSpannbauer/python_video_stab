
Usage Examples
===============

The ``VidStab`` class can be used as a command line script or in your
own custom python code.

Using from command line
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   # Using defaults
   python3 -m vidstab --input input_video.mov --output stable_video.avi

.. code:: bash

   # Using a specific keypoint detector
   python3 -m vidstab -i input_video.mov -o stable_video.avi -k GFTT

Using ``VidStab`` class
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

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

Plotting frame to frame transformations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from vidstab import VidStab
   import matplotlib.pyplot as plt

   stabilizer = VidStab()
   stabilizer.stabilize(input_path='input_video.mov', output_path='stable_video.avi')

   stabilizer.plot_trajectory()
   plt.show()

   stabilizer.plot_transforms()
   plt.show()

+--------------+------------+
| Trajectories | Transforms |
+==============+============+
| |image3|     | |image4|   |
+--------------+------------+

Using borders
~~~~~~~~~~~~~

.. code:: python

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

+-------------------+---------------------+
| ``border_size=0`` | ``border_size=100`` |
+===================+=====================+
| |image5|          | |image6|            |
+-------------------+---------------------+

+----------------------------------------+
| ``border_size='auto'``                 |
+========================================+
| |image11|                              |
+----------------------------------------+

|

+---------------------------+-----------------------------+
| ``border_type='reflect'`` | ``border_type='replicate'`` |
+===========================+=============================+
| |image7|                  | |image8|                    |
+---------------------------+-----------------------------+

|VideoLink|_ *used with permission from* |HappyLivingLink|_

Using Frame Layering
~~~~~~~~~~~~~~~~~~~~

.. code:: python

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

+--------------------------------------+------------------------------------+
| ``layer_func=vidstab.layer_overlay`` | ``layer_func=vidstab.layer_blend`` |
+======================================+====================================+
| |image9|                             | |image10|                          |
+--------------------------------------+------------------------------------+

|VideoLink|_ *used with permission from* |HappyLivingLink|_

Working with live video
~~~~~~~~~~~~~~~~~~~~~~~

The ``VidStab`` class can also process live video streams.  The underlying video reader is |cv2.VideoCapture|_ (documentation linked).
The relevant snippet from the documentation for stabilizing live video is:

     *Its argument can be either the device index or the name of a video file. Device index is just the number to specify which camera. Normally one camera will be connected (as in my case). So I simply pass 0 (or -1). You can select the second camera by passing 1 and so on.*

The ``input_path`` argument of the ``VidStab.stabilize`` method can accept integers that will be passed directly to ``cv2.VideoCapture`` as a device index.  You can also pass a device index to the ``--input`` argument for command line usage.

One notable difference between live feeds and video files is that webcam footage does not have a definite end point.
The options for ending a live video stabilization are to set the max length using the ``max_frames`` argument or to manually stop the process by pressing the ``Esc`` key or the ``Q`` key.
If ``max_frames`` is not provided then no progress bar can be displayed for live video stabilization processes.

Example
-------

.. code:: python

   from vidstab import VidStab

   stabilizer = VidStab()
   stabilizer.stabilize(input_path=0,
                        output_path='stable_webcam.avi',
                        max_frames=1000,
                        playback=True)

.. image:: https://s3.amazonaws.com/python-vidstab/readme/webcam_stable.gif
    :width: 50%
    :align: center

.. _VideoLink: https://www.youtube.com/watch?v=9pypPqbV_GM
.. _HappyLivingLink: https://www.facebook.com/happylivinginfl/
.. |VideoLink| replace:: *Video*
.. |HappyLivingLink| replace:: *HappyLiving*

.. |cv2.VideoCapture| replace:: ``cv2.VideoCapture``
.. _cv2.VideoCapture: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html

.. |image3| image:: https://s3.amazonaws.com/python-vidstab/readme/trajectory_plot.png
.. |image4| image:: https://s3.amazonaws.com/python-vidstab/readme/transforms_plot.png
.. |image5| image:: https://s3.amazonaws.com/python-vidstab/readme/stable_ostrich.gif
.. |image6| image:: https://s3.amazonaws.com/python-vidstab/readme/wide_stable_ostrich.gif
.. |image7| image:: https://s3.amazonaws.com/python-vidstab/readme/reflect_stable_ostrich.gif
.. |image8| image:: https://s3.amazonaws.com/python-vidstab/readme/replicate_stable_ostrich.gif
.. |image9| image:: https://s3.amazonaws.com/python-vidstab/readme/trail_stable_ostrich.gif
.. |image10| image:: https://s3.amazonaws.com/python-vidstab/readme/blend_stable_ostrich.gif
.. |image11| image:: https://s3.amazonaws.com/python-vidstab/readme/auto_border_stable_ostrich.gif
  :width: 45%
