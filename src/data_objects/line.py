class Line:
    def __init__(self, agency, line_number):
        self.agency = agency
        self.line_number = line_number

        self.routes = {}

    def add_route(self, route):
        # TODO: check if the route id exists
        self.routes[route.route_id] = route