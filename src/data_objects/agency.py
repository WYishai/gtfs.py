import data_objects.line


class Agency:
    def __init__(self, agency_id, agency_name, agency_url, agency_timezone, agency_lang, agency_phone, agency_fare_url,
                 **kwargs):
        self.agency_id = int(agency_id)
        self.agency_name = agency_name
        self.agency_url = agency_url
        self.agency_timezone = agency_timezone
        self.agency_lang = agency_lang
        self.agency_phone = agency_phone
        self.agency_fare_url = agency_fare_url

        self.lines = {}

        assert len(kwargs) == 0

    def get_line(self, route):
        line_number = route.route_short_name

        if line_number not in self.lines:
            line = data_objects.line.Line(self, line_number)
            self.lines[line_number] = line
        else:
            line = self.lines[line_number]

        line.add_route(route)

        return line
