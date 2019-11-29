"""
`@image_comparison` was removed in matplotlib 3.2
Tests now a bit looser
"""
import matplotlib
import pytest
from vidstab.plot_utils import plot_transforms, plot_trajectory
from .pickled_transforms import download_pickled_transforms

transforms, trajectory, smooth_trajectory = download_pickled_transforms(window_size=30)


def int_axes_lims(axes):
    x_lims = axes.get_xlim()
    y_lims = axes.get_ylim()

    return [int(x) for x in x_lims + y_lims]


def check_vidstab_plot(plot, expected_axes1, expected_axes2):
    fig, (axes1, axes2) = plot

    axes1_lims = int_axes_lims(axes1)
    axes2_lims = int_axes_lims(axes2)

    # noinspection PyUnresolvedReferences
    fig_check = isinstance(fig, matplotlib.figure.Figure)
    axes1_check = axes1_lims == expected_axes1
    axes2_check = axes2_lims == expected_axes2

    return all([fig_check, axes1_check, axes2_check])


def test_plot_trajectory_exception():
    with pytest.raises(AttributeError) as err:
        plot_trajectory(None, None, None)

    assert 'No trajectory to plot' in str(err.value)


def test_plot_transforms_exception():
    with pytest.raises(AttributeError) as err:
        plot_transforms(None)

    assert 'No transforms to plot' in str(err.value)


def test_plot_trajectory():
    plot = plot_trajectory(transforms, trajectory, smooth_trajectory)

    expected_axes1 = [-15, 325, -384, 173]
    expected_axes2 = [-15, 325, -17, 450]

    assert check_vidstab_plot(plot, expected_axes1, expected_axes2)


def test_plot_transforms():
    plot = plot_transforms(transforms, radians=False)

    expected_axes1 = [-15, 325, -204, 113]
    expected_axes2 = [-15, 325, -10, 5]

    assert check_vidstab_plot(plot, expected_axes1, expected_axes2)


def test_plot_transforms_radians():
    plot = plot_transforms(transforms, radians=True)

    expected_axes1 = [-15, 325, -204, 113]
    expected_axes2 = [-15, 325, 0, 0]

    assert check_vidstab_plot(plot, expected_axes1, expected_axes2)
