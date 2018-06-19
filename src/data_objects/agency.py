import data_objects.line
from utils.parsing import parse_or_default


class Agency:
    def __init__(self, agency_id, agency_name, agency_url, agency_timezone, agency_lang=None, agency_phone=None,
                 agency_email=None, agency_fare_url=None, **kwargs):
        """
        :type agency_id: str | int
        :type agency_name: str
        :type agency_url: str
        :type agency_timezone: str
        :type agency_lang: str | None
        :type agency_phone: str | None
        :type agency_email: str | None
        :type agency_fare_url: str | None
        """

        self.agency_id = int(agency_id)
        self.agency_name = agency_name
        self.agency_url = agency_url
        self.agency_timezone = agency_timezone
        self.agency_lang = parse_or_default(agency_lang, None, str)
        self.agency_phone = parse_or_default(agency_phone, None, str)
        self.agency_email = parse_or_default(agency_email, None, str)
        self.agency_fare_url = parse_or_default(agency_fare_url, None, str)

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
