
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

+---------------------------+-----------------------------+
| ``border_type='reflect'`` | ``border_type='replicate'`` |
+===========================+=============================+
| |image7|                  | |image8|                    |
+---------------------------+-----------------------------+

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

.. |image3| image:: https://github.com/AdamSpannbauer/python_video_stab/blob/master/readme/trajectory_plot.png?raw=true
.. |image4| image:: https://github.com/AdamSpannbauer/python_video_stab/blob/master/readme/transforms_plot.png?raw=true
.. |image5| image:: https://github.com/AdamSpannbauer/python_video_stab/blob/master/readme/stable_ostrich.gif?raw=true
.. |image6| image:: https://github.com/AdamSpannbauer/python_video_stab/blob/master/readme/wide_stable_ostrich.gif?raw=true
.. |image7| image:: https://github.com/AdamSpannbauer/python_video_stab/blob/master/readme/reflect_stable_ostrich.gif?raw=true
.. |image8| image:: https://github.com/AdamSpannbauer/python_video_stab/blob/master/readme/replicate_stable_ostrich.gif?raw=true
.. |image9| image:: https://github.com/AdamSpannbauer/python_video_stab/blob/master/readme/trail_stable_ostrich.gif?raw=true
.. |image10| image:: https://github.com/AdamSpannbauer/python_video_stab/blob/master/readme/blend_stable_ostrich.gif?raw=true
