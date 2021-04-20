class NoSuchElementError(Exception):
    def __init__(self, err=""):
        self.err = err

    def __str__(self):
        if self.err == "":
            return "No such element was found"
        else:
            return self.err