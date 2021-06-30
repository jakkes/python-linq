from .base import Base


class All(Base):
    def aggregate(self, data):
        return all(data)
