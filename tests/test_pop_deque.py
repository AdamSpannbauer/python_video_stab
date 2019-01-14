from vidstab.pop_deque import PopDeque


def test_pop_append():
    x = PopDeque([0], maxlen=2)

    assert x.pop_append(1) is None
    assert x.pop_append(2) == 0


def test_increment_append():
    x = PopDeque([0, 1, 2], maxlen=3)

    popped = x.increment_append()

    assert popped == 0
    assert list(x) == [1, 2, 3]

    popped = x.increment_append(pop_append=False)
    assert popped is None

    x.increment_append(increment=2, pop_append=False)
    assert list(x) == [3, 4, 6]
