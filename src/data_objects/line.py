import data_objects.agency


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
