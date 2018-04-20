from distutils.core import setup

setup(name='vidstab',
      version='0.0.5',
      description='Video Stabilization using OpenCV',
      author='Adam Spannbauer',
      author_email='spannbaueradam@gmail.com',
      url='https://github.com/AdamSpannbauer/python_video_stab',
      packages=['vidstab'],
      license='MIT',
      install_requires=[
          'opencv-python',
          'numpy',
          'pandas',
          'imutils',
          'progress',
      ],
      keywords=['video stabilization', 'computer vision', 'image processing', 'opencv']
      )
