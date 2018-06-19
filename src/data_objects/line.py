import data_objects.agency
from data_objects.base_object import BaseGtfsObjectCollection


class Line:
    def __init__(self, agency, line_number):
        """
        :type agency: data_objects.agency.Agency
        :type line_number: str
        """

        self.agency = agency
        self.line_number = line_number

        self.routes = {}

    def add_route(self, route):
        # TODO: check if the route id exists
        self.routes[route.route_id] = route


class LineCollection(BaseGtfsObjectCollection):
    def __init__(self, transit_data, agency):
        BaseGtfsObjectCollection.__init__(self, transit_data)
        self._agency = agency

    def get_line(self, route):
        line_number = route.route_short_name

        if line_number not in self:
            line = data_objects.line.Line(self._agency, line_number)
            self._objects[line_number] = line
        else:
            line = self[line_number]

        line.add_route(route)

        return line

    def add_line(self, **kwargs):
        line = Line(**kwargs)

        assert line.line_number not in self._objects
        self._objects[line.line_number] = line
        return line