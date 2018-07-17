import csv
import sys

import gtfspy
from gtfspy.utils.validating import not_none_or_empty


class FareRule:
    def __init__(self, transit_data, fare_id, route_id=None, origin_id=None, destination_id=None, contains_id=None,
                 **kwargs):
        """
        :type transit_data: gtfspy.transit_data_object.TransitData
        :type fare_id: str
        :type route_id: str | None
        :type origin_id: str | None
        :type destination_id: str | None
        :type contains_id: str | None
        """

        self.fare = transit_data.fare_attributes[fare_id]

        self.attributes = {k: v for k, v in kwargs.iteritems() if not_none_or_empty(v)}
        if not_none_or_empty(route_id):
            self.attributes["route_id"] = transit_data.routes[route_id]
        if not_none_or_empty(origin_id):
            self.attributes["origin_id"] = int(origin_id)
        if not_none_or_empty(destination_id):
            self.attributes["destination_id"] = int(destination_id)
        if not_none_or_empty(contains_id):
            self.attributes["contains_id"] = int(contains_id)

    @property
    def route(self):
        """
        :rtype: gtfspy.data_objects.Route | None
        """

        return self.attributes.get("route_id", None)

    @route.setter
    def route(self, value):
        """
        :type value: gtfspy.data_objects.Route | None
        """

        self.attributes["route_id"] = value

    @property
    def origin_id(self):
        """
        :rtype: int | None
        """

        return self.attributes.get("origin_id", None)

    @origin_id.setter
    def origin_id(self, value):
        """
        :type value: int | None
        """

        self.attributes["origin_id"] = value

    @property
    def destination_id(self):
        """
        :rtype: int | None
        """

        return self.attributes.get("destination_id", None)

    @destination_id.setter
    def destination_id(self, value):
        """
        :type value: int | None
        """

        self.attributes["destination_id"] = value

    @property
    def contains_id(self):
        """
        :rtype: int | None
        """

        return self.attributes.get("contains_id", None)

    @contains_id.setter
    def contains_id(self, value):
        """
        :type value: int | None
        """

        self.attributes["contains_id"] = value

    def get_csv_fields(self):
        return ["fare_id"] + self.attributes.keys()

    def to_csv_line(self):
        result = dict(fare_id=self.fare.fare_id,
                      **self.attributes)

        if "route_id" in result:
            result["route_id"] = self.route.route_id

        return result

    def validate(self, transit_data):
        """
        :type transit_data: gtfspy.transit_data_object.TransitData
        """

        assert transit_data.fare_attributes[self.fare.fare_id] is self.fare
        assert self.route is None or transit_data.routes[self.route.route_id] is self.route

    def __eq__(self, other):
        if not isinstance(other, FareRule):
            return False

        return self.fare.fare_id == other.fare.fare_id and self.attributes == other.attributes

    def __ne__(self, other):
        return not (self == other)


class FareRuleCollection:
    def __init__(self, transit_data, csv_file=None):
        """
        :type transit_data: gtfspy.transit_data_object.TransitData
        """

        self._transit_data = transit_data
        self._objects = []

        if csv_file is not None:
            self._load_file(csv_file)

    def add_fare_rule(self, ignore_errors=False, condition=None, **kwargs):
        try:
            fare_rule = FareRule(transit_data=self._transit_data, **kwargs)

            if condition is not None and not condition(fare_rule):
                return None

            self._transit_data._changed()

            self._objects.append(fare_rule)
            return fare_rule
        except:
            if not ignore_errors:
                raise

    def remove(self, fare_rule, recursive=False, clean_after=True):
        self._objects.remove(fare_rule)

        if clean_after:
            self._transit_data.clean()

    def clean(self):
        zone_ids = {stop.zone_id for stop in self._transit_data.stops}
        fare_rules_to_clean = [fare_rule for fare_rule in self
                               if (fare_rule.route is not None
                                   and fare_rule.route.route_id not in self._transit_data.routes)
                               or (fare_rule.origin_id is not None and fare_rule.origin_id not in zone_ids)
                               or (fare_rule.destination_id is not None and fare_rule.destination_id not in zone_ids)
                               or (fare_rule.contains_id is not None and fare_rule.contains_id not in zone_ids)]
        for fare_rule in fare_rules_to_clean:
            self._objects.remove(fare_rule)

    def _load_file(self, csv_file, ignore_errors=False, filter=None):
        if isinstance(csv_file, str):
            with open(csv_file, "rb") as f:
                self._load_file(f, ignore_errors=ignore_errors, filter=filter)
        else:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.add_fare_rule(ignore_errors=ignore_errors, condition=filter, **row)

    def has_data(self):
        return len(self._objects) > 0

    def save(self, csv_file):
        if isinstance(csv_file, str):
            with open(csv_file, "wb") as f:
                self.save(f)
        else:
            fields = []
            for obj in self:
                fields += (field for field in obj.get_csv_fields() if field not in fields)

            writer = csv.DictWriter(csv_file, fieldnames=fields, restval=None)
            writer.writeheader()
            writer.writerows(obj.to_csv_line() for obj in self)

    def validate(self):
        for obj in self._objects:
            obj.validate(self._transit_data)

    def __len__(self):
        return len(self._objects)

    def __iter__(self):
        return iter(self._objects)

    def __contains__(self, item):
        return item in self._objects

    def __eq__(self, other):
        if not isinstance(other, FareRuleCollection):
            return False

        return self._objects == other._objects

    def __ne__(self, other):
        return not (self == other)

    def __sizeof__(self):
        size = object.__sizeof__(self)
        for k, v in self.__dict__.iteritems():
            if k not in ["_transit_data"]:
                size += sys.getsizeof(v)
        return size
