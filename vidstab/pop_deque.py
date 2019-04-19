from collections import deque


class PopDeque(deque):
    def deque_full(self):
        """Test if queue is full"""
        return len(self) == self.maxlen

    def pop_append(self, x):
        """deque.append helper to return popped element if deque is at ``maxlen``

        :param x: element to append
        :return: result of ``deque.popleft()`` if deque is full; else ``None``

        >>> x = PopDeque([0], maxlen=2)
        >>> x.pop_append(1)

        >>> x.pop_append(2)
        0
        """
        popped_element = None
        if self.deque_full():
            popped_element = self.popleft()

        self.append(x)

        return popped_element

    def increment_append(self, increment=1, pop_append=True):
        """Append deque[-1] + ``increment`` to end of deque

        If deque is empty then 0 is appended

        :param increment: size of increment in deque
        :param pop_append: return popped element if append forces pop?
        :return: popped_element if pop_append is True; else None
        """
        if len(self) == 0:
            popped_element = self.pop_append(0)
        else:
            popped_element = self.pop_append(self[-1] + increment)

        if not pop_append:
            return None

        return popped_element
