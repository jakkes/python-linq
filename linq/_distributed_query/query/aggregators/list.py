from .base import Base


class List(Base):
    def aggregate(self, data):
        return list(data)
