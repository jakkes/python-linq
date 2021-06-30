from .base import Base


class Flatten(Base):
    def iterator(self, data):
        for x in data:
            yield from x
