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
