from .base import Base


class ArgMax(Base):
    def __init__(self, value_fn, invert_value=False):
        super().__init__()
        self.value_fn = value_fn
        self.invert_value = invert_value

    def aggregate(self, data):
        max_value = None
        max_arg = None
        for x in data:
            if max_value is None:
                max_value = self.value_fn(x)
                max_arg = x
                continue

            value = self.value_fn(x)
            if (value > max_value and not self.invert_value) or (value < max_value and self.invert_value):
                max_value = value
                max_arg = x
        return max_arg
