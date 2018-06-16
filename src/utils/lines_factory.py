from collections import defaultdict

from data_objects import Line, Route


class LinesFactory:
    def __init__(self):
        self.lines = defaultdict(dict)

    def get_line(self, route):
        """
        :rtype: Line
        :type route: Route
        """

        line_number = route.route_short_name
        agency_id = route.agency.agency_id

        if line_number not in self.lines[agency_id]:
            line = Line(route.agency, line_number)
            self.lines[agency_id][line_number] = line
        else:
            line = self.lines[agency_id][line_number]

        line.add_route(route)
        return line
