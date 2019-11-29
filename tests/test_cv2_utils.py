import builtins
import sys
import pytest
import numpy as np
from vidstab.cv2_utils import safe_import_cv2, cv2_estimateRigidTransform


@pytest.fixture
def missing_cv2(monkeypatch):
    """Monkey patch import to test missing cv2"""
    import_og = builtins.__import__

    # noinspection PyShadowingBuiltins, PyUnusedLocal
    def mocked_import(name, globals, locals, fromlist, level):
        if name == 'cv2':
            raise ModuleNotFoundError()
        return import_og(name, locals, fromlist, level)

    monkeypatch.setattr(builtins, '__import__', mocked_import)


@pytest.fixture(autouse=True)
def cleanup_imports():
    yield
    sys.modules.pop('cv2', None)


@pytest.mark.usefixtures('missing_cv2')
def test_missing_cv2():
    with pytest.raises(ModuleNotFoundError) as err:
        safe_import_cv2()

    assert 'pip install vidstab[cv2]' in str(err.value)


# noinspection PyPep8Naming
def test_cv2_estimateRigidTransform():
    missing_kps = np.empty((0,))
    transform = cv2_estimateRigidTransform(missing_kps, missing_kps)

    assert transform is None
