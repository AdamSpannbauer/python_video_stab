import cv2


class Frame:
    """Utility for easier color format conversions.

    :param image: OpenCV image as numpy array.
    :param color_format: Name of input color format or None.
         If str, the input must use the format that is used in OpenCV's cvtColor code parameter.
         For example, if an image is bgr then input 'BGR' as seen in the cvtColor codes:
        [cv2.COLOR_BGR2GRAY, COLOR_Luv2BGR].
        If None, the color format will be assumed from shape of the image.
        The only possible outcomes of this assumption are: ['GRAY', 'BGR', 'BGRA'].

    :ivar image: input image with possible color format conversions applied
    :ivar color_format: str containing the current color format of image attribute.
    """
    def __init__(self, image, color_format=None):
        self.image = image

        if color_format is None:
            self.color_format = self._guess_color_format()
        else:
            self.color_format = color_format

    def _guess_color_format(self):
        if len(self.image.shape) == 2:
            return 'GRAY'

        elif self.image.shape[2] == 3:
            return 'BGR'

        elif self.image.shape[2] == 4:
            return 'BGRA'

        else:
            raise ValueError(f'Unexpected frame image shape: {self.image.shape}')

    @staticmethod
    def _lookup_color_conversion(from_format, to_format):
        return getattr(cv2, f'COLOR_{from_format}2{to_format}')

    def cvt_color(self, to_format):
        if not self.color_format == to_format:
            color_conversion = self._lookup_color_conversion(from_format=self.color_format,
                                                             to_format=to_format)

            return cv2.cvtColor(self.image, color_conversion)
        else:
            return self.image

    @property
    def gray_image(self):
        return self.cvt_color('GRAY')

    @property
    def bgr_image(self):
        return self.cvt_color('BGR')

    @property
    def bgra_image(self):
        return self.cvt_color('BGRA')
