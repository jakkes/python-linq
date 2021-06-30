from .base import Base


class Max(Base):
    def aggregate(self, data):
        return max(data)
