Basic usage
-----------

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

Advanced usage
--------------

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
| |image2|     | |image3|   |
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

.. raw:: html

   <table>

.. raw:: html

   <tr>

.. raw:: html

   <td>

.. raw:: html

   <p align="center">

border_size=0

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td>

.. raw:: html

   <p align="center">

border_size=100

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

.. raw:: html

   <p align="center">

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td>

.. raw:: html

   <p align="center">

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   </table>

+---------------------------+-----------------------------+
| ``border_type='reflect'`` | ``border_type='replicate'`` |
+===========================+=============================+
| |image4|                  | |image5|                    |
+---------------------------+-----------------------------+

`Video <https://www.youtube.com/watch?v=9pypPqbV_GM>`__\ *used with
permission
from*\ `HappyLiving <https://www.facebook.com/happylivinginfl/>`__

Using Frame Layering
~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from vidstab import VidStab, layer_overlay, layer_blend

   # init vid stabilizer
   stabilizer = VidStab()

   # use vidstab.layer_overlay for generating a trail effect
   stabilizer.stabilize(input_path=INPUT_VIDEO_PATH,
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
   stabilizer.stabilize(input_path=INPUT_VIDEO_PATH,
                        output_path='blend_stable_video.avi',
                        border_type='black',
                        border_size=100,
                        layer_func=layer_custom)

+--------------------------------------+------------------------------------+
| ``layer_func=vidstab.layer_overlay`` | ``layer_func=vidstab.layer_blend`` |
+======================================+====================================+
| |image6|                             | |image7|                           |
+--------------------------------------+------------------------------------+

`Video <https://www.youtube.com/watch?v=9pypPqbV_GM>`__\ *used with
permission
from*\ `HappyLiving <https://www.facebook.com/happylivinginfl/>`__

Automatic border sizing
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from vidstab import VidStab, layer_overlay

   stabilizer = VidStab()

   stabilizer.stabilize(input_path=INPUT_VIDEO_PATH,
                        output_path='auto_border_stable_video.avi',
                        border_size='auto',
                        # frame layering to show performance of auto sizing
                        layer_func=layer_overlay)

|image8|

Working with live video
~~~~~~~~~~~~~~~~~~~~~~~

The ``VidStab`` class can also process live video streams. The
underlying video reader is
``cv2.VideoCapture``\ (`documentation <https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html>`__).
The relevant snippet from the documentation for stabilizing live video
is:

   *Its argument can be either the device index or the name of a video
   file. Device index is just the number to specify which camera.
   Normally one camera will be connected (as in my case). So I simply
   pass 0 (or -1). You can select the second camera by passing 1 and so
   on.*

The ``input_path`` argument of the ``VidStab.stabilize`` method can
accept integers that will be passed directly to ``cv2.VideoCapture`` as
a device index. You can also pass a device index to the ``--input``
argument for command line usage.

One notable difference between live feeds and video files is that webcam
footage does not have a definite end point. The options for ending a
live video stabilization are to set the max length using the
``max_frames`` argument or to manually stop the process by pressing the
Esc key or the Q key. If ``max_frames`` is not provided then no progress
bar can be displayed for live video stabilization processes.

Example
^^^^^^^

.. code:: python

   from vidstab import VidStab

   stabilizer = VidStab()
   stabilizer.stabilize(input_path=0,
                        output_path='stable_webcam.avi',
                        max_frames=1000,
                        playback=True)

|image9|

Transform file writing & reading
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generating and saving transforms to file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   import numpy as np
   from vidstab import VidStab, download_ostrich_video

   # Download video if needed
   download_ostrich_video(INPUT_VIDEO_PATH)

   # Generate transforms and save to TRANSFORMATIONS_PATH as csv (no headers)
   stabilizer = VidStab()
   stabilizer.gen_transforms(INPUT_VIDEO_PATH)
   np.savetxt(TRANSFORMATIONS_PATH, stabilizer.transforms, delimiter=',')

File at ``TRANSFORMATIONS_PATH`` is of the form shown below. The 3
columns represent delta x, delta y, and delta angle respectively.

::

   -9.249733913760086068e+01,2.953221378387767970e+01,-2.875918912994855636e-02
   -8.801434576214279559e+01,2.741942225927152776e+01,-2.715232319470826938e-02

Reading and using transforms from file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Below example reads a file of transforms and applies to an arbitrary
video. The transform file is of the form shown in `above
section <#generating-and-saving-transforms-to-file>`__.

.. code:: python

   import numpy as np
   from vidstab import VidStab

   # Read in csv transform data, of form (delta x, delta y, delta angle):
   transforms = np.loadtxt(TRANSFORMATIONS_PATH, delimiter=',')

   # Create stabilizer and supply numpy array of transforms
   stabilizer = VidStab()
   stabilizer.transforms = transforms

   # Apply stabilizing transforms to INPUT_VIDEO_PATH and save to OUTPUT_VIDEO_PATH
   stabilizer.apply_transforms(INPUT_VIDEO_PATH, OUTPUT_VIDEO_PATH)

.. |image0| image:: https://s3.amazonaws.com/python-vidstab/readme/input_ostrich.gif
.. |image1| image:: https://s3.amazonaws.com/python-vidstab/readme/stable_ostrich.gif
.. |image2| image:: https://s3.amazonaws.com/python-vidstab/readme/trajectory_plot.png
.. |image3| image:: https://s3.amazonaws.com/python-vidstab/readme/transforms_plot.png
.. |image4| image:: https://s3.amazonaws.com/python-vidstab/readme/reflect_stable_ostrich.gif
.. |image5| image:: https://s3.amazonaws.com/python-vidstab/readme/replicate_stable_ostrich.gif
.. |image6| image:: https://s3.amazonaws.com/python-vidstab/readme/trail_stable_ostrich.gif
.. |image7| image:: https://s3.amazonaws.com/python-vidstab/readme/blend_stable_ostrich.gif
.. |image8| image:: https://s3.amazonaws.com/python-vidstab/readme/auto_border_stable_ostrich.gif
.. |image9| image:: https://s3.amazonaws.com/python-vidstab/readme/webcam_stable.gif
