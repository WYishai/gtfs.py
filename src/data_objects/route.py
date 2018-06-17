import transit_data


class Route:
    def __init__(self, transit_data, route_id, route_long_name, route_type, agency_id, route_color, route_desc,
                 route_short_name, **kwargs):
        """
        :type transit_data: transit_data.TransitData
        :type route_id: str
        :type route_long_name: str
        :type route_type: str | int
        :type agency_id: str | int
        :type route_color: str
        :type route_desc: str
        :type route_short_name: str
        """

        self.route_id = route_id
        self.route_long_name = route_long_name
        self.route_type = int(route_type)
        self.agency = transit_data.agencies[int(agency_id)]
        # TODO: find type for the route color
        self.route_color = route_color
        self.route_desc = route_desc
        self.route_short_name = route_short_name

        self.line = transit_data._lines_factory.get_line(self)
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
