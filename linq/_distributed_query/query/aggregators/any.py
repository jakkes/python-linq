from .base import Base


class Any(Base):
    def aggregate(self, data):
        return any(data)
