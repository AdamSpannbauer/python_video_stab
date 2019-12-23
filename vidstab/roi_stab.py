from .frame_queue import FrameQueue
from .VidStab import VidStab
from .pop_deque import PopDeque
from .frame import Frame


class ROIFrameQueue(FrameQueue):
    def __init__(self, max_len=None, max_frames=None):
        self.roi_bb = None
        self.rois = PopDeque(maxlen=max_len)
        self._frames = PopDeque(maxlen=max_len)

        self.use_frames = True
        super().__init__(max_len=max_len, max_frames=max_frames)
        self.use_frames = False

    @property
    def frames(self):
        if self.use_frames:
            return self._frames
        return self.rois

    @frames.setter
    def frames(self, x):
        if self.use_frames:
            self._frames = x
        self.rois = x

    def _append_frame(self, frame, pop_ind=True):
        old_value = self.use_frames
        self.use_frames = True

        i, popped_frame, break_flag = super()._append_frame(frame, pop_ind=pop_ind)
        self.use_frames = old_value

        if self.roi_bb is None:
            x = y = 0
            h, w = frame.shape[:2]
        else:
            x, y, w, h = self.roi_bb

        roi = frame[y:y+h, x:x+w]
        popped_roi = self.rois.pop_append(Frame(roi))

        if self.use_frames:
            return i, popped_frame, break_flag

        return i, popped_roi, break_flag


class ROIStab(VidStab):
    def __init__(self, roi_bb=None, kp_method='GFTT', *args, **kwargs):
        super().__init__(kp_method=kp_method, *args, **kwargs)
        self.roi = None
        self.frame_queue = ROIFrameQueue()
        self.frame_queue.roi_bb = roi_bb

    @property
    def roi_bb(self):
        return self.frame_queue.roi_bb

    @roi_bb.setter
    def roi_bb(self, x):
        self.frame_queue.roi_bb = x

    def _process_first_frame(self, array=None):
        self.frame_queue.use_frames = False
        super()._process_first_frame(array=array)

    def _gen_next_raw_transform(self):
        self.frame_queue.use_frames = False
        super()._gen_next_raw_transform()

    def _init_trajectory(self, smoothing_window, max_frames, gen_all=False, show_progress=False):
        self.frame_queue.use_frames = False
        bar = super()._init_trajectory(smoothing_window, max_frames, gen_all=gen_all, show_progress=show_progress)
        return bar

    def _apply_next_transform(self, i, frame_i, use_stored_transforms=False):
        self.frame_queue.use_frames = True
        transformed = super()._apply_next_transform(i, frame_i, use_stored_transforms=use_stored_transforms)
        return transformed
