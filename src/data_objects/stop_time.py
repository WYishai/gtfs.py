from datetime import timedelta

import transit_data_object
from utils.parsing import parse_or_default, str_to_bool
from utils.time import parse_timedelta


class StopTime:
    _optional_arguments = {"pickup_type": (True, str_to_bool),
                           "drop_off_type": (True, str_to_bool),
                           "shape_dist_traveled": (0.0, float),
                           "stop_headsign": (None, str),
                           "timepoint": (None, int)}

    def __init__(self, transit_data, trip_id, arrival_time, departure_time, stop_id, stop_sequence, pickup_type=None,
                 drop_off_type=None, shape_dist_traveled=None, stop_headsign=None, timepoint=None, **kwargs):
        """
        :type transit_data: transit_data_object.TransitData
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
        self.allow_pickup = parse_or_default(pickup_type, True, lambda v: not bool(int(v)))
        self.allow_drop_off = parse_or_default(drop_off_type, True, lambda v: not bool(int(v)))
        self.shape_dist_traveled = parse_or_default(shape_dist_traveled, None, float)
        self.stop_headsign = parse_or_default(stop_headsign, None, str)
        self.timepoint = parse_or_default(timepoint, None, int)

        assert len(kwargs) == 0

    def get_csv_fields(self):
        return ["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence", "pickup_type", "drop_off_type",
                "shape_dist_traveled", "stop_headsign", "timepoint"]

    def to_csv_line(self):
        return {"trip_id": self.trip.trip_id,
                "arrival_time": self.arrival_time,
                "departure_time": self.departure_time,
                "stop_id": self.stop.stop_id,
                "stop_sequence": self.stop_sequence,
                "pickup_type": 0 if self.allow_pickup else 1,
                "drop_off_type": 0 if self.allow_drop_off else 1,
                "shape_dist_traveled": self.shape_dist_traveled,
                "stop_headsign": self.stop_headsign,
                "timepoint": self.timepoint}

    def validate(self, transit_data):
        """
        :type transit_data: transit_data.TransitData
        """

        assert transit_data.trips[self.trip.trip_id] is self.trip
        assert transit_data.stops[self.stop.stop_id] is self.stop

        assert self.allow_pickup or self.allow_drop_off
        assert self.arrival_time is not None or self.departure_time is not None
        assert self.arrival_time is None or self.departure_time is None or self.arrival_time <= self.departure_time

    def __eq__(self, other):
        if not isinstance(other, StopTime):
            return False

        return self.trip == other.trip and self.arrival_time == other.arrival_time and \
               self.departure_time == other.departure_time and self.stop == other.stop and \
               self.stop_sequence == other.stop_sequence and self.allow_pickup == other.allow_pickup and \
               self.allow_drop_off == other.allow_drop_off and self.shape_dist_traveled == other.shape_dist_traveled and \
               self.stop_headsign == other.stop_headsign and self.timepoint and other.timepoint
