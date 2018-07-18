import csv

import gtfspy
from gtfspy.data_objects.base_object import BaseGtfsObjectCollection
from gtfspy.utils.parsing import parse_yes_no_unknown, yes_no_unknown_to_int
from gtfspy.utils.validating import not_none_or_empty, validate_yes_no_unknown


class Route(object):
    def __init__(self, transit_data, route_id, route_short_name, route_long_name, route_type, agency_id,
                 route_desc=None, route_color=None, route_text_color=None, bikes_allowed=None, **kwargs):
        """
        :type transit_data: gtfspy.transit_data_object.TransitData
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

        self._id = route_id
        self.route_short_name = route_short_name
        self.route_long_name = route_long_name
        # TODO: create dedicated object to route type
        self.route_type = int(route_type)
        self.agency = transit_data.agencies[int(agency_id)]

        self.attributes = {k: v for k, v in kwargs.iteritems() if not_none_or_empty(v)}
        if not_none_or_empty(route_desc):
            self.attributes["route_desc"] = str(route_desc)
        if not_none_or_empty(route_color):
            # TODO: find type for the route color
            self.attributes["route_color"] = str(route_color)
        if not_none_or_empty(route_text_color):
            self.attributes["route_text_color"] = str(route_text_color)
        if not_none_or_empty(bikes_allowed):
            if isinstance(bikes_allowed, bool):
                self.attributes["bikes_allowed"] = yes_no_unknown_to_int(bikes_allowed)
            else:
                self.attributes["bikes_allowed"] = int(bikes_allowed)

        self.line = self.agency.get_line(self)
        self.trips = []

    @property
    def id(self):
        return self._id

    @property
    def route_desc(self):
        """
        :rtype: str | None
        """

        return self.attributes.get("route_desc", None)

    @route_desc.setter
    def route_desc(self, value):
        """
        :type value: str | None
        """

        self.attributes["route_desc"] = value

    @property
    def route_color(self):
        """
        :rtype: str | None
        """

        return self.attributes.get("route_color", None)

    @route_color.setter
    def route_color(self, value):
        """
        :type value: str | None
        """

        self.attributes["route_color"] = value

    @property
    def route_text_color(self):
        """
        :rtype: str | None
        """

        return self.attributes.get("route_text_color", None)

    @route_text_color.setter
    def route_text_color(self, value):
        """
        :type value: str | None
        """

        self.attributes["route_text_color"] = value

    @property
    def bikes_allowed(self):
        """
        :rtype: bool | None
        """

        return parse_yes_no_unknown(self.attributes.get("bikes_allowed", None))

    @bikes_allowed.setter
    def bikes_allowed(self, value):
        """
        :type value: bool | None
        """

        self.attributes["bikes_allowed"] = yes_no_unknown_to_int(value)

    @property
    def stops(self):
        """
        :rtype: list[gtfspy.data_objects.Stop] | None
        """

        return None if len(self.trips) == 0 else self.trips[0].stops

    @property
    def first_stop(self):
        """
        :rtype: gtfspy.data_objects.Stop | None
        """

        return None if len(self.trips) == 0 else self.trips[0].first_stop

    @property
    def last_stop(self):
        """
        :rtype: gtfspy.data_objects.Stop | None
        """

        return None if len(self.trips) == 0 else self.trips[0].last_stop

    def get_trips_calendar(self, from_date, to_date=None, stop_id=None, sort=True):
        res = ((t, trip)
               for trip in self.trips
               for t in trip.get_trip_calendar(from_date, to_date=to_date, stop_id=stop_id))

        if sort:
            res = list(res)
            res.sort()

        return res

    def get_csv_fields(self):
        return ["route_id", "route_short_name", "route_long_name", "route_type", "agency_id"] + self.attributes.keys()

    def to_csv_line(self):
        result = dict(route_id=self.id,
                      route_short_name=self.route_short_name,
                      route_long_name=self.route_long_name,
                      route_type=self.route_type,
                      agency_id=self.agency.id,
                      **self.attributes)
        return result

    def validate(self, transit_data):
        """
        :type transit_data: gtfspy.transit_data_object.TransitData
        """

        assert transit_data.agencies[self.agency.id] is self.agency
        assert self.route_type in xrange(0, 8)
        assert validate_yes_no_unknown(self.attributes.get("bikes_allowed", None))

    def __eq__(self, other):
        if not isinstance(other, Route):
            return False

        return self.id == other.id and self.route_short_name == other.route_short_name and \
               self.route_long_name == other.route_long_name and self.route_type == other.route_type and \
               self.agency == other.agency and self.attributes == other.attributes

    def __ne__(self, other):
        return not (self == other)


class RouteCollection(BaseGtfsObjectCollection):
    def __init__(self, transit_data, csv_file=None):
        BaseGtfsObjectCollection.__init__(self, transit_data, Route)

        if csv_file is not None:
            self._load_file(csv_file)

    def add_route(self, ignore_errors=False, condition=None, **kwargs):
        try:
            route = Route(transit_data=self._transit_data, **kwargs)

            if condition is not None and not condition(route):
                return None

            self._transit_data._changed()

            assert route.id not in self._objects
            self._objects[route.id] = route
            route.line.add_route(route)
            return route
        except:
            if not ignore_errors:
                raise

    def add_route_object(self, route, recursive=False):
        assert isinstance(route, Route)

        if route.id not in self:
            if recursive:
                self._transit_data.add_agency_object(route.agency, recursive=True)
            else:
                assert route.agency in self._transit_data.agencies
            self.add_route(**route.to_csv_line())
        else:
            assert route == self[route.id]

    def remove(self, route, recursive=False, clean_after=True):
        if not isinstance(route, Route):
            route = self[route]
        else:
            assert self[route.id] is route

        if recursive:
            for trip in route.trips:
                self._transit_data.trips.remove(trip, recursive=True, clean_after=False)

            fare_rules_to_remove = [fare_rule for fare_rule in self._transit_data.fare_rules
                                    if fare_rule.route is route]
            for fare_rule in fare_rules_to_remove:
                self._transit_data.fare_rules.remove(fare_rule, recursive=True, clean_after=False)
        else:
            assert len(route.trips) == 0

        del route.line.routes[route.id]
        del self._objects[route.id]

        if clean_after:
            self._transit_data.clean()

    def clean(self):
        to_clean = []
        for route in self:
            if len(route.trips) == 0:
                to_clean.append(route)

        for route in to_clean:
            del route.line.routes[route.id]
            del self._objects[route.id]

    def _load_file(self, csv_file, ignore_errors=False, filter=None):
        if isinstance(csv_file, str):
            with open(csv_file, "rb") as f:
                self._load_file(f, ignore_errors=ignore_errors, filter=filter)
        else:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.add_route(ignore_errors=ignore_errors, condition=filter, **row)
