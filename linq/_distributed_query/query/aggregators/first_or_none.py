from .base import Base


class FirstOrNone(Base):
    def __init__(self, condition_fn):
        super().__init__()
        self.condition_fn = condition_fn

    def aggregate(self, data):
        for x in data:
            if self.condition_fn(x):
                return x
        return None
