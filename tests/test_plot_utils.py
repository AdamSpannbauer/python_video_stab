from matplotlib.testing.decorators import image_comparison

from vidstab.plot_utils import plot_transforms, plot_trajectory
from .download_pickled_transforms import download_pickled_transforms

transforms, trajectory, smooth_trajectory = download_pickled_transforms(window_size=30)


@image_comparison(baseline_images=['plot_trajectory'], extensions=['png'])
def test_plot_trajectory():
    plot_trajectory(transforms, trajectory, smooth_trajectory)


@image_comparison(baseline_images=['plot_transforms'], extensions=['png'])
def test_plot_transforms():
    plot_transforms(transforms, radians=False)


@image_comparison(baseline_images=['plot_transforms_radians'], extensions=['png'])
def test_plot_transforms_radians():
    plot_transforms(transforms, radians=True)
