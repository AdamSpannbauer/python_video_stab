import cv2
import numpy as np


def layer_overlay(foreground, background):
    """put an image over the top of another

    Intended for use in VidStab class to create a trail of previous frames in the stable video output.
    (example output of using trail: https://www.linkedin.com/feed/update/urn:li:activity:6396794976134524928/)

    :param foreground: image to be laid over top of background image
    :param background: image to over laid with foreground image
    :return: return combined image where foreground is laid over background
    """
    # convert top image to grayscale
    gray = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)

    # inv threshold grayscale top image
    _, threshed = cv2.threshold(gray, 3, 255, cv2.THRESH_BINARY_INV)

    # lessen thresholded image area
    # (alleviates black border around top im in overlay)
    threshed = cv2.dilate(threshed, None, iterations=2)

    # mask locations of background that overlap with foreground
    masked = cv2.bitwise_and(background, background, mask=threshed)

    # take max pixel values to perform overlay
    overlayed = np.maximum(masked, foreground)
    return overlayed


def layer_blend(foreground, background, foreground_alpha=.6):
    """blend a foreground image over background (wrapper for cv2.addWeighted)

    :param foreground: image to be laid over top of background image
    :param background: image to over laid with foreground image
    :param foreground_alpha: alpha to apply to foreground; (1 - foreground_alpha) applied to background
    :return: return combined image where foreground is laid over background with alpha
    """
    cv2.addWeighted(foreground, foreground_alpha,
                    background, 1 - foreground_alpha, 0, background)

    return background
