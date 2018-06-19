import data_objects.shape
import transit_data
from utils.parsing import parse_or_default


class Trip:
    def __init__(self, transit_data, trip_id, route_id, service_id, trip_headsign=None, trip_short_name=None,
                 direction_id=None, block_id=None, shape_id=None, bikes_allowed=None, wheelchair_accessible=None,
                 original_trip_id=None, **kwargs):
        """
        :type transit_data: transit_data.TransitData
        :type trip_id: str
        :type route_id: str
        :type service_id: str | int
        :type trip_headsign: str | None
        :type trip_short_name: str | None
        :type direction_id: str | int | None
        :type block_id: str | None
        :type shape_id: data_objects.shape.Shape | str | int | None
        :type bikes_allowed: str | int | None
        :type wheelchair_accessible: str | int | None
        :type original_trip_id: str | None
        """

        self.trip_id = trip_id
        self.route = transit_data.routes[route_id]
        self.service = transit_data.calendar[int(service_id)]
        self.trip_headsign = parse_or_default(trip_headsign, None, str)
        self.trip_short_name = parse_or_default(trip_short_name, None, str)
        self.direction_id = parse_or_default(direction_id, None, int)
        self.block_id = parse_or_default(block_id, None, str)
        self.shape = parse_or_default(shape_id, None, lambda s: transit_data.shapes[int(shape_id)])
        self.bikes_allowed = parse_or_default(bikes_allowed, None, int)
        self.wheelchair_accessible = parse_or_default(wheelchair_accessible, None, int)
        self.original_trip_id = parse_or_default(original_trip_id, None, str)

        self.stop_times = []

        assert len(kwargs) == 0

    @property
    def stops(self):
        return [stop_time.stop for stop_time in self.stop_times]

    @property
    def first_stop(self):
        return self.stops[0]

    @property
    def last_stop(self):
        return self.stops[-1]
