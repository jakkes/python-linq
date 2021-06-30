from .base import Base


class Count(Base):

    def aggregate(self, data):
        return sum(1 for _ in data)
