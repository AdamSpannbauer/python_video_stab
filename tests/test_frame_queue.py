import pytest
import numpy as np

from vidstab.frame import Frame
from vidstab.frame_queue import FrameQueue


def test_reset_queue():
    frame_queue = FrameQueue(max_len=10, max_frames=20)
    frame_queue.i = 42

    frame_queue.reset_queue(max_len=30, max_frames=40)

    assert frame_queue.max_len == 30
    assert frame_queue.max_frames == 40
    assert len(frame_queue.frames) == 0
    assert len(frame_queue.inds) == 0
    assert frame_queue.i is None


def test_set_frame_source():
    frame_queue = FrameQueue()

    with pytest.raises(TypeError) as err:
        frame_queue.set_frame_source('fake')

    assert 'Not yet support for non cv2.VideoCapture frame source.' in str(err.value)


def test_read_frame():
    frame_queue = FrameQueue(max_len=1)
    black_frame_image = np.zeros((3, 3, 3), dtype='uint8')

    i, frame, break_flag = frame_queue.read_frame(array=black_frame_image, pop_ind=False)

    assert i is None
    assert frame is None
    assert break_flag is None

    i, frame, break_flag = frame_queue.read_frame(array=black_frame_image)

    assert i == 0
    assert isinstance(frame, Frame)
    assert break_flag is None
