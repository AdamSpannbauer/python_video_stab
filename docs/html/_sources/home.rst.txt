
.. image:: _static/vidstab_logo_small.png
    :alt: vidstab: Python Video Stabilization
    :align: right

.. image:: https://img.shields.io/badge/Lifecycle-Maturing-yellow.svg
    :target: https://github.com/AdamSpannbauer/python_video_stab

.. image:: https://travis-ci.org/AdamSpannbauer/python_video_stab.svg?branch=master
    :target: https://travis-ci.org/AdamSpannbauer/python_video_stab

.. image:: https://img.shields.io/codecov/c/github/AdamSpannbauer/python_video_stab/master.svg
    :target: https://codecov.io/github/AdamSpannbauer/python_video_stab?branch=master

.. image:: https://api.codeclimate.com/v1/badges/f3a17d211a2a437d21b1/maintainability
   :target: https://codeclimate.com/github/AdamSpannbauer/python_video_stab/maintainability

.. image:: https://pypip.in/v/vidstab/badge.png
    :target: https://crate.io/packages/vidstab/

Python video stabilization using OpenCV.

This module contains a single class (``VidStab``) used for video
stabilization. This class is based on the work presented by Nghia Ho in
`SIMPLE VIDEO STABILIZATION USING
OPENCV <http://nghiaho.com/?p=2093>`__.

+----------+----------+
| Input    | Output   |
+==========+==========+
| |image1| | |image2| |
+----------+----------+

|VideoLink|_ *used with permission from* |HappyLivingLink|_

.. |image1| image:: https://s3.amazonaws.com/python-vidstab/readme/input_ostrich.gif
.. |image2| image:: https://s3.amazonaws.com/python-vidstab/readme/stable_ostrich.gif

.. _VideoLink: https://www.youtube.com/watch?v=9pypPqbV_GM
.. _HappyLivingLink: https://www.facebook.com/happylivinginfl/
.. |VideoLink| replace:: *Video*
.. |HappyLivingLink| replace:: *HappyLiving*
