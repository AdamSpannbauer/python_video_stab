import cv2
import numpy as np


def layer_overlay(foreground, background):
    """put an image over the top of another

    Intended for use in VidStab class to create a trail of previous frames in the stable video output.

    :param foreground: image to be laid over top of background image
    :param background: image to over laid with foreground image
    :return: return combined image where foreground is laid over background
    """
    overlaid = foreground.copy()
    negative_space = np.where(foreground[:, :, 3] == 0)

    overlaid[negative_space] = background[negative_space]

    overlaid[:, :, 3] = 255

    return overlaid


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
