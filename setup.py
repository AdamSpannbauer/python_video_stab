from setuptools import setup

setup(name='vidstab',
      version='0.1.0',
      description='Video Stabilization using OpenCV',
      author='Adam Spannbauer',
      author_email='spannbaueradam@gmail.com',
      url='https://github.com/AdamSpannbauer/python_video_stab',
      packages=['vidstab'],
      license='MIT',
      install_requires=[
          'numpy',
          'pandas',
          'imutils',
          'progress',
          'matplotlib',
      ],
      extras_require={
        'cv2':  ['opencv-contrib-python >= 3.4.0']
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      keywords=['video stabilization', 'computer vision', 'image processing', 'opencv']
      )
