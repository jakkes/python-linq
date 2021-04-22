class NoSuchElementError(Exception):
    """Raised whenever a requested element was not retrievable."""

    def __init__(self, err=""):
        self.err = err

    def __str__(self):
        if self.err == "":
            return "No such element was found"
        else:
            return self.err