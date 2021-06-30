from .base import Base


class Min(Base):
    def aggregate(self, data):
        return min(data)
