from datetime import timedelta

import transit_data
from utils.parsing import parse_or_default, str_to_bool
from utils.time import parse_timedelta


class StopTime:
    def __init__(self, transit_data, trip_id, arrival_time, departure_time, stop_id, stop_sequence, pickup_type=None,
                 drop_off_type=None, shape_dist_traveled=None, stop_headsign=None, timepoint=None, **kwargs):
        """
        :type transit_data: transit_data.TransitData
        :type trip_id: str
        :type arrival_time: str | timedelta
        :type departure_time: str | timedelta
        :type stop_id: str | int
        :type stop_sequence: str | int
        :type pickup_type: str | int | bool | None
        :type drop_off_type: str | int | bool | None
        :type shape_dist_traveled: str | int | float | None
        :type stop_headsign: str
        :type timepoint: str | int | None
        """

        self.trip = transit_data.trips[trip_id]
        self.arrival_time = parse_timedelta(arrival_time)
        self.departure_time = parse_timedelta(departure_time)
        self.stop = transit_data.stops[int(stop_id)]
        self.stop_sequence = int(stop_sequence)
        self.pickup_type = parse_or_default(pickup_type, True, lambda v: not bool(int(v)))
        self.drop_off_type = parse_or_default(drop_off_type, True, lambda v: not bool(int(v)))
        self.shape_dist_traveled = parse_or_default(shape_dist_traveled, 0.0, float)
        self.stop_headsign = stop_headsign
        self.timepoint = parse_or_default(timepoint, None, int)

        assert len(kwargs) == 0
