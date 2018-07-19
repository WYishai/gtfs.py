import csv
from datetime import date, time, timedelta
from operator import attrgetter

from sortedcontainers import SortedList

import gtfspy
from gtfspy.data_objects.base_object import BaseGtfsObjectCollection
from gtfspy.utils.parsing import parse_yes_no_unknown, yes_no_unknown_to_int
from gtfspy.utils.validating import not_none_or_empty, validate_yes_no_unknown


class Trip(object):
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

        self._id = trip_id
        self.route = transit_data.routes[route_id]
        self.service = transit_data.calendar[int(service_id)]

        self.attributes = {k: v for k, v in kwargs.iteritems() if not_none_or_empty(v)}
        if not_none_or_empty(trip_headsign):
            self.attributes["trip_headsign"] = str(trip_headsign)
        if not_none_or_empty(trip_short_name):
            self.attributes["trip_short_name"] = str(trip_short_name)
        if not_none_or_empty(direction_id):
            self.attributes["direction_id"] = int(direction_id)
        if not_none_or_empty(block_id):
            self.attributes["block_id"] = int(block_id)
        if not_none_or_empty(shape_id):
            self.attributes["shape_id"] = transit_data.shapes[int(shape_id)]
        if not_none_or_empty(bikes_allowed):
            if isinstance(bikes_allowed, bool):
                self.attributes["bikes_allowed"] = yes_no_unknown_to_int(bikes_allowed)
            else:
                self.attributes["bikes_allowed"] = int(bikes_allowed)
        if not_none_or_empty(wheelchair_accessible):
            if isinstance(wheelchair_accessible, bool):
                self.attributes["wheelchair_accessible"] = yes_no_unknown_to_int(wheelchair_accessible)
            else:
                self.attributes["wheelchair_accessible"] = int(wheelchair_accessible)
        if not_none_or_empty(original_trip_id):
            self.attributes["original_trip_id"] = str(original_trip_id)

        self.stop_times = SortedList(key=attrgetter("stop_sequence"))

    @property
    def id(self):
        return self._id

    @property
    def trip_headsign(self):
        """
        :rtype: str | None
        """

        return self.attributes.get("trip_headsign", None)

    @trip_headsign.setter
    def trip_headsign(self, value):
        self.attributes["trip_headsign"] = value

    @property
    def trip_short_name(self):
        """
        :rtype: str | None
        """

        return self.attributes.get("trip_short_name", None)

    @trip_short_name.setter
    def trip_short_name(self, value):
        self.attributes["trip_short_name"] = value

    @property
    def direction_id(self):
        """
        :rtype: int | None
        """

        return self.attributes.get("direction_id", None)

    @direction_id.setter
    def direction_id(self, value):
        self.attributes["direction_id"] = value

    @property
    def block_id(self):
        """
        :rtype: int | None
        """

        return self.attributes.get("block_id", None)

    @block_id.setter
    def block_id(self, value):
        self.attributes["block_id"] = value

    @property
    def shape(self):
        """
        :rtype: gtfspy.data_objects.Shape | None
        """

        return self.attributes.get("shape_id", None)

    @shape.setter
    def shape(self, value):
        self.attributes["shape_id"] = value

    @property
    def bikes_allowed(self):
        """
        :rtype: bool | None
        """

        return parse_yes_no_unknown(self.attributes.get("bikes_allowed", None))

    @bikes_allowed.setter
    def bikes_allowed(self, value):
        self.attributes["bikes_allowed"] = yes_no_unknown_to_int(value)

    @property
    def wheelchair_accessible(self):
        """
        :rtype: bool | None
        """

        return parse_yes_no_unknown(self.attributes.get("wheelchair_accessible", None))

    @wheelchair_accessible.setter
    def wheelchair_accessible(self, value):
        self.attributes["wheelchair_accessible"] = yes_no_unknown_to_int(value)

    @property
    def original_trip_id(self):
        """
        :rtype: str | None
        """

        return self.attributes.get("original_trip_id", None)

    @original_trip_id.setter
    def original_trip_id(self, value):
        self.attributes["original_trip_id"] = value

    @property
    def start_time(self):
        arrival_time_seconds = self.stop_times[0].arrival_time.total_seconds()
        return time(hour=int(arrival_time_seconds / (60 * 60)),
                    minute=int(arrival_time_seconds / 60) % 60,
                    second=int(arrival_time_seconds) % 60)

    @property
    def stops(self):
        """
        :rtype: list[gtfspy.data_objects.Stop]
        """

        return [stop_time.stop for stop_time in self.stop_times]

    @property
    def first_stop(self):
        """
        :rtype: gtfspy.data_objects.Stop
        """

        return self.stops[0]

    @property
    def last_stop(self):
        """
        :rtype: gtfspy.data_objects.Stop
        """

        return self.stops[-1]

    def get_trip_calendar(self, from_date, to_date=None, stop_id=None):
        """
        :type from_date: date
        :type to_date: date | None
        :type stop_id: int
        """

        if to_date is None:
            to_date = from_date

        assert from_date <= to_date

        stop_time = None
        if stop_id is None:
            stop_time = self.stop_times[0]
        else:
            stop_time = (st for st in self.stop_times if st.stop.id == id).next()

        i = from_date
        day_interval = timedelta(days=1)
        while i <= to_date:
            if self.service.is_active_on(i):
                yield i + stop_time.arrival_time
            i += day_interval

    def get_csv_fields(self):
        return ["trip_id", "route_id", "service_id"] + self.attributes.keys()

    def to_csv_line(self):
        result = dict(trip_id=self.id,
                      route_id=self.route.id,
                      service_id=self.service.id,
                      **self.attributes)

        if "shape_id" in result:
            result["shape_id"] = self.shape.id

        return result

    def validate(self, transit_data):
        """
        :type transit_data: gtfspy.transit_data_object.TransitData
        """

        assert transit_data.routes[self.route.id] is self.route
        assert transit_data.calendar[self.service.id] is self.service
        assert self.shape is None or transit_data.shapes[self.shape.id] is self.shape
        assert validate_yes_no_unknown(self.attributes.get("bikes_allowed", None))
        assert validate_yes_no_unknown(self.attributes.get("wheelchair_accessible", None))

        for stop_time in self.stop_times:
            stop_time.validate(transit_data)

    def __eq__(self, other):
        if not isinstance(other, Trip):
            return False

        return self.id == other.id and self.route == other.route and self.service == other.service and \
               self.attributes == other.attributes

    def __ne__(self, other):
        return not (self == other)


class TripCollection(BaseGtfsObjectCollection):
    def __init__(self, transit_data, csv_file=None):
        BaseGtfsObjectCollection.__init__(self, transit_data, Trip)

        if csv_file is not None:
            self._load_file(csv_file)

    def add_trip(self, ignore_errors=False, condition=None, **kwargs):
        try:
            trip = Trip(transit_data=self._transit_data, **kwargs)

            if condition is not None and not condition(trip):
                return None

            self._transit_data._changed()

            assert trip.id not in self._objects
            self._objects[trip.id] = trip
            trip.route.trips.append(trip)
            return trip
        except:
            if not ignore_errors:
                raise

    def add_trip_object(self, trip, recursive=False):
        assert isinstance(trip, Trip)

        if trip.id not in self._transit_data.trips:
            if recursive:
                self._transit_data.add_route_object(trip.route, recursive=True)
                self._transit_data.add_service_object(trip.service, recursive=True)
                if trip.shape is not None:
                    self._transit_data.add_shape_object(trip.shape, recursive=True)
            else:
                assert trip.route in self._transit_data.routes
                assert trip.service in self._transit_data.calendar
                assert trip.shape is None or trip.shape in self._transit_data.shapes
            return self.add_trip(**trip.to_csv_line())
        else:
            old_trip = self[trip.id]
            assert trip == old_trip
            return old_trip

    def remove(self, trip, recursive=False, clean_after=True):
        if not isinstance(trip, Trip):
            trip = self[trip]
        else:
            assert self[trip.id] is trip

        if recursive:
            for stop_time in trip.stop_times:
                stop_time.stop.stop_times.remove(stop_time)
        else:
            assert len(trip.stop_times) == 0

        trip.route.trips.remove(trip)
        del self._objects[trip.id]

        if clean_after:
            self._transit_data.clean()

    def clean(self):
        to_clean = []
        for trip in self:
            if len(trip.stop_times) == 0:
                to_clean.append(trip)

        for trip in to_clean:
            trip.route.trips.remove(trip)
            del self._objects[trip.id]

    def _load_file(self, csv_file, ignore_errors=False, filter=None):
        if isinstance(csv_file, str):
            with open(csv_file, "rb") as f:
                self._load_file(f, ignore_errors=ignore_errors, filter=filter)
        else:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.add_trip(ignore_errors=ignore_errors, condition=filter, **row)
