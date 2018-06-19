import sys


class BaseGtfsObjectCollection(object):
    def __init__(self, transit_data):
        self._transit_data = transit_data
        self._objects = {}

    def __len__(self):
        return len(self._objects)

    def __getitem__(self, key):
        return self._objects[key]

    def __iter__(self):
        return self._objects.itervalues()

    def __contains__(self, item):
        return item in self._objects

    def __sizeof__(self):
        size = object.__sizeof__(self)
        for k, v in self.__dict__.iteritems():
            # TODO: change it to check if it's not a weak reference
            if k not in ["_transit_data"]:
                size += sys.getsizeof(v)
        return size
