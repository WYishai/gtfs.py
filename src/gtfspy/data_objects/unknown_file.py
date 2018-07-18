class UnknownFile(object):
    def __init__(self, f):
        # TODO: check if csv file
        self.data = f.read()
