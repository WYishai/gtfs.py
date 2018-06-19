import transit_data
from utils.parsing import parse_or_default, str_to_bool


class Route:
    def __init__(self, transit_data, route_id, route_short_name, route_long_name, route_type, agency_id,
                 route_desc=None, route_color=None, route_text_color=None, bikes_allowed=None, **kwargs):
        """
        :type transit_data: transit_data.TransitData
        :type route_id: str
        :type route_short_name: str
        :type route_long_name: str
        :type route_type: str | int
        :type agency_id: str | int
        :type route_desc: str | None
        :type route_color: str | None
        :type route_text_color: str | None
        :type bikes_allowed: str | int | bool | None
        """

        self.route_id = route_id
        self.route_short_name = route_short_name
        self.route_long_name = route_long_name
        # TODO: create dedicated object to route type
        self.route_type = int(route_type)
        self.agency = transit_data.agencies[int(agency_id)]
        self.route_desc = parse_or_default(route_desc, None, str)
        # TODO: find type for the route color
        self.route_color = parse_or_default(route_color, None, str)
        self.route_text_color = parse_or_default(route_text_color, None, str)
        self.bikes_allowed = parse_or_default(bikes_allowed, None, str_to_bool)

        self.line = self.agency.get_line(self)
        self.trips = []

        assert len(kwargs) == 0

    @property
    def stops(self):
        return None if len(self.trips) == 0 else self.trips[0].stops

    @property
    def first_stop(self):
        return None if len(self.trips) == 0 else self.trips[0].first_stop

    @property
    def last_stop(self):
        return None if len(self.trips) == 0 else self.trips[0].last_stop
