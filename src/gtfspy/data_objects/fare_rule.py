import csv
import sys

import gtfspy
from gtfspy.utils.parsing import parse_or_default


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
        self.route = parse_or_default(route_id, None, lambda x: transit_data.routes[route_id])
        self.origin_id = parse_or_default(origin_id, None, int)
        self.destination_id = parse_or_default(destination_id, None, int)
        self.contains_id = parse_or_default(contains_id, None, int)

        assert len(kwargs) == 0

    def get_csv_fields(self):
        return ["fare_id", "route_id", "origin_id", "destination_id", "contains_id"]

    def to_csv_line(self):
        return {"fare_id": self.fare.fare_id,
                "route_id": self.route.route_id,
                "origin_id": self.origin_id,
                "destination_id": self.destination_id,
                "contains_id": self.contains_id}

    def validate(self, transit_data):
        """
        :type transit_data: gtfspy.transit_data_object.TransitData
        """

        pass

    def __eq__(self, other):
        if not isinstance(other, FareRule):
            return False

        return self.fare.fare_id == other.fare.fare_id and self.route.route_id == other.route.route_id and \
               self.origin_id == other.origin_id and self.destination_id == other.destination_id and \
               self.contains_id == other.contains_id

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

    def add_fare_rule(self, **kwargs):
        fare_rule = FareRule(transit_data=self._transit_data, **kwargs)

        self._transit_data._changed()

        self._objects.append(fare_rule)
        return fare_rule

    def remove(self, fare_rule, recursive=False, clean_after=True):
        self._objects.remove(fare_rule)

        if clean_after:
            self._transit_data.clean()

    def clean(self):
        zone_ids = {stop.zone_id for stop in self._transit_data.stops}
        fare_rules_to_clean = [fare_rule for fare_rule in self
                               if (fare_rule.origin_id is not None and fare_rule.origin_id not in zone_ids)
                               or (fare_rule.destination_id is not None and fare_rule.destination_id not in zone_ids)
                               or (fare_rule.contains_id is not None and fare_rule.contains_id not in zone_ids)]
        for fare_rule in fare_rules_to_clean:
            self._objects.remove(fare_rule)

    def _load_file(self, csv_file):
        if isinstance(csv_file, str):
            with open(csv_file, "rb") as f:
                self._load_file(f)
        else:
            reader = csv.DictReader(csv_file)
            self._objects = [FareRule(transit_data=self._transit_data, **row) for row in reader
                             if row["route_id"] in self._transit_data.routes]

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
