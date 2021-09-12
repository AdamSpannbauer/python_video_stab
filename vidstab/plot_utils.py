import matplotlib.pyplot as plt
import numpy as np


def plot_trajectory(transforms, trajectory, smoothed_trajectory):
    """Plot video trajectory

    Create a plot of the video's trajectory & smoothed trajectory.
    Separate subplots are used to show the x and y trajectory.

    :param transforms: VidStab transforms attribute
    :param trajectory: VidStab trajectory attribute
    :param smoothed_trajectory: VidStab smoothed_trajectory attribute
    :return: tuple of matplotlib objects ``(Figure, (AxesSubplot, AxesSubplot))``

    >>> from vidstab import VidStab
    >>> import matplotlib.pyplot as plt
    >>> stabilizer = VidStab()
    >>> stabilizer.gen_transforms(input_path='input_video.mov')
    >>> stabilizer.plot_trajectory()
    >>> plt.show()
    """
    if transforms is None:
        raise AttributeError('No trajectory to plot. '
                             'Use methods: gen_transforms or stabilize to generate the trajectory attributes')

    with plt.style.context('ggplot'):
        fig, (ax1, ax2) = plt.subplots(2, sharex='all')

        # x trajectory
        ax1.plot(trajectory[:, 0], label='Trajectory')
        ax1.plot(smoothed_trajectory[:, 0], label='Smoothed Trajectory')
        ax1.set_ylabel('dx')

        # y trajectory
        ax2.plot(trajectory[:, 1], label='Trajectory')
        ax2.plot(smoothed_trajectory[:, 1], label='Smoothed Trajectory')
        ax2.set_ylabel('dy')

        handles, labels = ax2.get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper right')

        plt.xlabel('Frame Number')

        fig.suptitle('Video Trajectory', x=0.15, y=0.96, ha='left')
        fig.canvas.manager.set_window_title('Trajectory')

        return fig, (ax1, ax2)


def plot_transforms(transforms, radians=False):
    """Plot stabilizing transforms

    Create a plot of the transforms used to stabilize the input video.
    Plots x & y transforms (dx & dy) in a separate subplot than angle transforms (da).

    :param transforms: VidStab transforms attribute
    :param radians: Should angle transforms be plotted in radians?  If ``false``, transforms are plotted in degrees.
    :return: tuple of matplotlib objects ``(Figure, (AxesSubplot, AxesSubplot))``

    >>> from vidstab import VidStab
    >>> import matplotlib.pyplot as plt
    >>> stabilizer = VidStab()
    >>> stabilizer.gen_transforms(input_path='input_video.mov')
    >>> stabilizer.plot_transforms()
    >>> plt.show()
    """
    if transforms is None:
        raise AttributeError('No transforms to plot. '
                             'Use methods: gen_transforms or stabilize to generate the transforms attribute')

    with plt.style.context('ggplot'):
        fig, (ax1, ax2) = plt.subplots(2, sharex='all')

        ax1.plot(transforms[:, 0], label='delta x', color='C0')
        ax1.plot(transforms[:, 1], label='delta y', color='C1')
        ax1.set_ylabel('Delta Pixels', fontsize=10)

        if radians:
            ax2.plot(transforms[:, 2], label='delta angle', color='C2')
            ax2.set_ylabel('Delta Radians', fontsize=10)
        else:
            ax2.plot(np.rad2deg(transforms[:, 2]), label='delta angle', color='C2')
            ax2.set_ylabel('Delta Degrees', fontsize=10)

        handles1, labels1 = ax1.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        fig.legend(handles1 + handles2,
                   labels1 + labels2,
                   loc='upper right',
                   ncol=1)

        plt.xlabel('Frame Number')

        fig.suptitle('Transformations for Stabilizing', x=0.15, y=0.96, ha='left')
        fig.canvas.manager.set_window_title('Transforms')

        return fig, (ax1, ax2)
