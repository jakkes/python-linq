class NoSuchElementError(Exception):
    """Raised whenever a requested element was not retrievable."""

    def __init__(self):
        super().__init__("No such element was found.")
