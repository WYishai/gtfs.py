from datetime import timedelta

import gtfspy
from gtfspy.utils.time import parse_timedelta, str_timedelta
from gtfspy.utils.validating import not_none_or_empty, validate_true_false


class StopTime(object):
    def __init__(self, transit_data, trip_id, arrival_time, departure_time, stop_id, stop_sequence, pickup_type=None,
                 drop_off_type=None, shape_dist_traveled=None, stop_headsign=None, timepoint=None, **kwargs):
        """
        :type transit_data: gtfspy.transit_data_object.TransitData
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

        self.attributes = {k: v for k, v in kwargs.iteritems() if not_none_or_empty(v)}
        if not_none_or_empty(pickup_type):
            self.attributes["pickup_type"] = int(pickup_type)
        if not_none_or_empty(drop_off_type):
            self.attributes["drop_off_type"] = int(drop_off_type)
        if not_none_or_empty(shape_dist_traveled):
            self.attributes["shape_dist_traveled"] = float(shape_dist_traveled)
        if not_none_or_empty(stop_headsign):
            self.attributes["stop_headsign"] = str(stop_headsign)
        if not_none_or_empty(timepoint):
            self.attributes["timepoint"] = int(timepoint)

    @property
    def pickup_type(self):
        """
        :rtype: int
        """

        return self.attributes.get("pickup_type", 0)

    @pickup_type.setter
    def pickup_type(self, value):
        """
        :type value: int
        """

        self.attributes["pickup_type"] = int(value)

    @property
    def drop_off_type(self):
        """
        :rtype: int
        """

        return self.attributes.get("drop_off_type", 0)

    @drop_off_type.setter
    def drop_off_type(self, value):
        """
        :type value: int
        """

        self.attributes["drop_off_type"] = int(value)

    @property
    def allow_pickup(self):
        """
        :rtype: bool
        """

        return self.pickup_type != 1

    @allow_pickup.setter
    def allow_pickup(self, value):
        """
        :type value: bool
        """

        self.pickup_type = int(not value)

    @property
    def allow_drop_off(self):
        """
        :rtype: bool
        """

        return self.drop_off_type != 1

    @allow_drop_off.setter
    def allow_drop_off(self, value):
        """
        :type value: bool
        """

        self.drop_off_type = int(not value)

    @property
    def shape_dist_traveled(self):
        """
        :rtype: float | None
        """

        return self.attributes.get("shape_dist_traveled", None)

    @shape_dist_traveled.setter
    def shape_dist_traveled(self, value):
        """
        :type value: float | None
        """

        self.attributes["shape_dist_traveled"] = value

    @property
    def stop_headsign(self):
        """
        :rtype: str | None
        """

        return self.attributes.get("stop_headsign", None)

    @stop_headsign.setter
    def stop_headsign(self, value):
        """
        :type value: str | None
        """

        self.attributes["stop_headsign"] = value

    @property
    def is_exact_time(self):
        """
        :rtype: int | None
        """

        return bool(self.attributes.get("timepoint", 1))

    @is_exact_time.setter
    def is_exact_time(self, value):
        """
        :type value: bool | None
        """

        self.attributes["timepoint"] = int(value)

    def get_csv_fields(self):
        return ["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence"] + self.attributes.keys()

    def to_csv_line(self):
        result = dict(trip_id=self.trip.id,
                      arrival_time=str_timedelta(self.arrival_time),
                      departure_time=str_timedelta(self.departure_time),
                      stop_id=self.stop.id,
                      stop_sequence=self.stop_sequence,
                      **self.attributes)
        return result

    def validate(self, transit_data):
        """
        :type transit_data: gtfspy.transit_data_object.TransitData
        """

        assert transit_data.trips[self.trip.id] is self.trip
        assert transit_data.stops[self.stop.id] is self.stop

        assert self.allow_pickup or self.allow_drop_off
        assert validate_true_false(self.attributes.get("pickup_type", 0))
        assert validate_true_false(self.attributes.get("drop_off_type", 0))
        assert self.arrival_time is not None or self.departure_time is not None
        assert self.arrival_time is None or self.departure_time is None or self.arrival_time <= self.departure_time

    def __eq__(self, other):
        if not isinstance(other, StopTime):
            return False

        return self.trip == other.trip and self.arrival_time == other.arrival_time and \
               self.departure_time == other.departure_time and self.stop == other.stop and \
               self.stop_sequence == other.stop_sequence and self.attributes == other.attributes

    def __ne__(self, other):
        return not (self == other)
