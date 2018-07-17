import itertools

import gtfspy
from gtfspy.data_objects.base_object import BaseGtfsObjectCollection


class Line:
    def __init__(self, agency, line_number):
        """
        :type agency: gtfspy.data_objects.agency.Agency
        :type line_number: str
        """

        self.agency = agency
        self.line_number = line_number

        self.routes = {}

    @property
    def id(self):
        return self.line_number

    def add_route(self, route):
        # TODO: check if the route id exists
        self.routes[route.id] = route

    def get_trips_calendar(self, from_date, to_date=None, sort=True):
        res = itertools.chain.from_iterable(route.get_trips_calendar(from_date, to_date=to_date, sort=False)
                                            for route in self.routes.itervalues())

        if sort:
            res = list(res)
            res.sort()

        return res

    def validate(self, transit_data):
        """
        :type transit_data: gtfspy.transit_data_object.TransitData
        """

        assert transit_data.agencies[self.agency.id] is self.agency


class LineCollection(BaseGtfsObjectCollection):
    def __init__(self, transit_data, agency):
        BaseGtfsObjectCollection.__init__(self, transit_data, Line)
        self._agency = agency

    def get_line(self, route):
        line_number = route.route_short_name

        self._transit_data._changed()

        if line_number not in self:
            line = Line(self._agency, line_number)
            self._objects[line_number] = line
        else:
            line = self[line_number]

        return line

    def add_line(self, ignore_errors=False, condition=None, **kwargs):
        try:
            line = Line(**kwargs)

            if condition is not None and not condition(line):
                return None

            assert line.line_number not in self._objects
            self._objects[line.line_number] = line
            return line
        except:
            if not ignore_errors:
                raise

    def remove(self, line, recursive=False, clean_after=True):
        if not isinstance(line, Line):
            line = self[line]
        else:
            assert self[line.line_number] is line

        if recursive:
            for route in line.routes.values():
                self._transit_data.routes.remove(route, recursive=True, clean_after=False)
        else:
            assert len(line.routes) == 0

        del self._objects[line.line_number]

        if clean_after:
            self._transit_data.clean()

    def clean(self):
        to_clean = []
        for line in self:
            if len(line.routes) == 0:
                to_clean.append(line)

        for line in to_clean:
            del self._objects[line.line_number]
