import imutils
import cv2


def safe_import_cv2():
    """Gracefully fail ModuleNotFoundError due to cv2

    :return: None
    """
    try:
        import cv2
    except ModuleNotFoundError:
        raise ModuleNotFoundError("""
        No python bindings for OpenCV found when attempting to `import cv2`.
        If you have not installed OpenCV you can install with:

            pip install vidstab[cv2]

        If you'd prefer to install OpenCV from source you can see the docs here:
            https://docs.opencv.org/3.4.1/da/df6/tutorial_py_table_of_contents_setup.html
        """)


# noinspection PyPep8Naming
def cv2_estimateRigidTransform(from_pts, to_pts, full=False):
    """Estimate transforms in OpenCV 3 or OpenCV 4"""
    if not from_pts.shape[0] or not to_pts.shape[0]:
        return None

    if imutils.is_cv4():
        transform = cv2.estimateAffinePartial2D(from_pts, to_pts)[0]
    else:
        # noinspection PyUnresolvedReferences
        transform = cv2.estimateRigidTransform(from_pts, to_pts, full)

    return transform
