import transit_data


class Trip:
    def __init__(self, transit_data, trip_id, route_id, service_id, trip_headsign, direction_id, shape_id, **kwargs):
        """
        :type transit_data: transit_data.TransitData
        :type trip_id: str
        :type route_id: str
        :type service_id: str
        :type trip_headsign: str
        :type direction_id: str
        :type shape_id: str
        """

        self.trip_id = trip_id
        self.route = transit_data.routes[route_id]
        self.service = transit_data.calendar[service_id]
        self.trip_headsign = trip_headsign
        self.direction_id = direction_id
        self.shape = None if shape_id == '' else transit_data.shapes[shape_id]

        self.stop_times = []

        assert len(kwargs) == 0
