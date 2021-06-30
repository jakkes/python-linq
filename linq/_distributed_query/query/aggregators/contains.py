from .base import Base


class Contains(Base):
    def __init__(self, obj):
        super().__init__()
        self.obj = obj

    def aggregate(self, data):
        return self.obj in data
