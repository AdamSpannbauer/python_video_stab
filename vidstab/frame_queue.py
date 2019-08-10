import cv2
from .frame import Frame
from .pop_deque import PopDeque


class FrameQueue:
    def __init__(self, max_len=None, max_frames=None):
        self.max_len = max_len
        self.max_frames = max_frames

        self.frames = PopDeque(maxlen=max_len)
        self.inds = PopDeque(maxlen=max_len)
        self.i = None

        self.source = None
        self.source_frame_count = None
        self.source_fps = 30

        self.grabbed_frame = False

    def reset_queue(self, max_len=None, max_frames=None):
        self.max_len = max_len if max_len is not None else self.max_len
        self.max_frames = max_frames if max_frames is not None else self.max_frames

        self.frames = PopDeque(maxlen=max_len)
        self.inds = PopDeque(maxlen=max_len)
        self.i = None

    def set_frame_source(self, source):
        if isinstance(source, cv2.VideoCapture):
            self.source = source
            self.source_frame_count = int(source.get(cv2.CAP_PROP_FRAME_COUNT))
            self.source_fps = int(source.get(cv2.CAP_PROP_FPS))
        else:
            raise TypeError('Not yet support for non cv2.VideoCapture frame source.')

    def read_frame(self, pop_ind=True, array=None):
        if isinstance(self.source, cv2.VideoCapture):
            self.grabbed_frame, frame = self.source.read()
        else:
            frame = array

        return self._append_frame(frame, pop_ind)

    def _append_frame(self, frame, pop_ind=True):
        popped_frame = None
        if frame is not None:
            popped_frame = self.frames.pop_append(Frame(frame))
            self.i = self.inds.increment_append()

        if pop_ind and self.i is None:
            self.i = self.inds.popleft()

        if (pop_ind
                and self.i is not None
                and self.max_frames is not None):
            break_flag = self.i >= self.max_frames
        else:
            break_flag = None

        return self.i, popped_frame, break_flag

    def populate_queue(self, smoothing_window):
        n = min([smoothing_window, self.max_frames])

        for i in range(n):
            _, _, _ = self.read_frame(pop_ind=False)
            if not self.grabbed_frame:
                break

    def frames_to_process(self):
        return len(self.frames) > 0 or self.grabbed_frame
