
Install Options
=====================

Install ``vidstab`` without installing OpenCV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you’ve already built OpenCV with python bindings on your machine it
is recommended to install ``vidstab`` without installing the pypi
versions of OpenCV. The ``opencv-python`` python module can cause issues
if you’ve already built OpenCV from source in your environment.

The below commands will install ``vidstab`` without OpenCV included.

From PyPi
^^^^^^^^^

.. code:: bash

   pip install vidstab

From Github
^^^^^^^^^^^

.. code:: bash

   pip install git+https://github.com/AdamSpannbauer/python_video_stab.git

Install ``vidstab`` & OpenCV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you don’t have OpenCV installed already there are a couple options.

1. You can build OpenCV using one of the great online tutorials from
   `PyImageSearch <https://www.pyimagesearch.com/>`__,
   `LearnOpenCV <https://www.learnopencv.com/>`__, or
   `OpenCV <https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_setup/py_table_of_contents_setup/py_table_of_contents_setup.html#py-table-of-content-setup>`__
   themselves. When building from source you have more options (e.g.
   `platform
   optimization <https://www.pyimagesearch.com/2017/10/09/optimizing-opencv-on-the-raspberry-pi/>`__),
   but more responsibility. Once installed you can use the pip install
   command shown above.
2. You can install a pre-built distribution of OpenCV from pypi as a
   dependency for ``vidstab`` (see commands below)

The below commands will install ``vidstab`` with
``opencv-contrib-python`` as dependencies.

.. _from-pypi-1:

From PyPi
^^^^^^^^^

.. code:: bash

   pip install vidstab[cv2]

.. _from-github-1:

From Github
^^^^^^^^^^^

.. code:: bash

    pip install -e git+https://github.com/AdamSpannbauer/python_video_stab.git#egg=vidstab[cv2]