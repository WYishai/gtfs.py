import csv
from datetime import datetime, date, time, timedelta
from operator import attrgetter

from sortedcontainers import SortedList

import gtfspy
from gtfspy.data_objects.base_object import BaseGtfsObjectCollection
from gtfspy.utils.parsing import parse_or_default


class Trip:
    def __init__(self, transit_data, trip_id, route_id, service_id, trip_headsign=None, trip_short_name=None,
                 direction_id=None, block_id=None, shape_id=None, bikes_allowed=None, wheelchair_accessible=None,
                 original_trip_id=None, **kwargs):
        """
        :type transit_data: gtfspy.transit_data_object.TransitData
        :type trip_id: str
        :type route_id: str
        :type service_id: str | int
        :type trip_headsign: str | None
        :type trip_short_name: str | None
        :type direction_id: str | int | None
        :type block_id: str | None
        :type shape_id: str | int | None
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

        self.stop_times = SortedList(key=attrgetter("stop_sequence"))

        assert len(kwargs) == 0

    @property
    def start_time(self):
        arrival_time_seconds = self.stop_times[0].arrival_time.total_seconds()
        return time(hour=int(arrival_time_seconds / (60 * 60)),
                    minute=int(arrival_time_seconds / 60) % 60,
                    second=int(arrival_time_seconds) % 60)

    @property
    def stops(self):
        return [stop_time.stop for stop_time in self.stop_times]

    @property
    def first_stop(self):
        return self.stops[0]

    @property
    def last_stop(self):
        return self.stops[-1]

    def get_trip_calendar(self, from_date, to_date=None, stop_id=None):
        """
        :type from_date: date
        :type to_date: date | None
        :type stop_id: int
        """

        from_date = datetime.combine(from_date, time())
        if to_date is None:
            to_date = from_date
        else:
            to_date = datetime.combine(to_date, time())

        assert from_date <= to_date

        stop_time = None
        if stop_id is None:
            stop_time = self.stop_times[0]
        else:
            stop_time = (st for st in self.stop_times if st.stop.stop_id == stop_id).next()

        i = from_date
        day_interval = timedelta(days=1)
        while i <= to_date:
            if self.service.is_active_on(i):
                yield i + stop_time.arrival_time
            i += day_interval

    def get_csv_fields(self):
        return ["trip_id", "route_id", "service_id", "trip_headsign", "trip_short_name", "direction_id", "block_id",
                "shape_id", "bikes_allowed", "wheelchair_accessible", "original_trip_id"]

    def to_csv_line(self):
        return {"trip_id": self.trip_id,
                "route_id": self.route.route_id,
                "service_id": self.service.service_id,
                "trip_headsign": self.trip_headsign,
                "trip_short_name": self.trip_short_name,
                "direction_id": self.direction_id,
                "block_id": self.block_id,
                "shape_id": self.shape.shape_id if self.shape is not None else None,
                "bikes_allowed": self.bikes_allowed,
                "wheelchair_accessible": self.wheelchair_accessible,
                "original_trip_id": self.original_trip_id}

    def validate(self, transit_data):
        """
        :type transit_data: gtfspy.transit_data_object.TransitData
        """

        assert transit_data.routes[self.route.route_id] is self.route
        assert transit_data.calendar[self.service.service_id] is self.service
        assert self.shape is None or transit_data.shapes[self.shape.shape_id] is self.shape
        assert self.bikes_allowed is None or self.bikes_allowed in xrange(0, 3)
        assert self.wheelchair_accessible is None or self.wheelchair_accessible in xrange(0, 3)

        for stop_time in self.stop_times:
            stop_time.validate(transit_data)

    def __eq__(self, other):
        if not isinstance(other, Trip):
            return False

        return self.trip_id == other.trip_id and self.route == other.route and self.service == other.service and \
               self.trip_headsign == other.trip_headsign and self.trip_short_name == other.trip_short_name and \
               self.direction_id == other.direction_id and self.block_id == other.block_id and \
               self.shape == other.shape and self.bikes_allowed == other.bikes_allowed and \
               self.wheelchair_accessible == other.wheelchair_accessible and \
               self.original_trip_id == other.original_trip_id


class TripCollection(BaseGtfsObjectCollection):
    def __init__(self, transit_data, csv_file=None):
        BaseGtfsObjectCollection.__init__(self, transit_data)

        if csv_file is not None:
            self._load_file(csv_file)

    def add_trip(self, **kwargs):
        trip = Trip(transit_data=self._transit_data, **kwargs)

        self._transit_data._changed()

        assert trip.trip_id not in self._objects
        self._objects[trip.trip_id] = trip
        trip.route.trips.append(trip)
        return trip

    def remove(self, trip, recursive=False, clean_after=True):
        if not isinstance(trip, Trip):
            trip = self[trip]
        else:
            assert self[trip.trip_id] is trip

        if recursive:
            for stop_time in trip.stop_times:
                stop_time.stop.stop_times.remove(stop_time)

        else:
            assert len(trip.stop_times) == 0

        del self._objects[trip.trip_id]

        if clean_after:
            self._transit_data.clean()

    def clean(self):
        to_clean = []
        for trip in self:
            if len(trip.stop_times) == 0:
                to_clean.append(trip)

        for trip in to_clean:
            del self._objects[trip.trip_id]

    def _load_file(self, csv_file):
        if isinstance(csv_file, str):
            with open(csv_file, "rb") as f:
                self._load_file(f)
        else:
            reader = csv.DictReader(csv_file)
            self._objects = {trip.trip_id: trip for trip in
                             (Trip(transit_data=self._transit_data, **row) for row in reader)}
            for trip in self:
                trip.route.trips.append(trip)

    def validate(self):
        for i, obj in self._objects.iteritems():
            assert i == obj.trip_id
            obj.validate(self._transit_data)
