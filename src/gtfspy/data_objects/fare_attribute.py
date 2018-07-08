import csv

import gtfspy
from gtfspy.data_objects.base_object import BaseGtfsObjectCollection
from gtfspy.utils.parsing import parse_or_default


class FareAttribute:
    def __init__(self, fare_id, price, currency_type, payment_method, transfers, transfer_duration=None, **kwargs):
        self.fare_id = fare_id
        self.price = float(price)
        self.currency_type = currency_type
        self.payment_method = int(payment_method)
        self.transfers = int(transfers)
        self.transfer_duration = parse_or_default(transfer_duration, None, int)

        self.args = kwargs

    def get_csv_fields(self):
        return ["fare_id", "price", "currency_type", "payment_method", "transfers",
                "transfer_duration"] + self.args.keys()

    def to_csv_line(self):
        return dict(fare_id=self.fare_id,
                    price="%.2f" % (self.price,),
                    currency_type=self.currency_type,
                    payment_method=self.payment_method,
                    transfers=self.transfers,
                    transfer_duration=self.transfer_duration,
                    **self.args)

    def validate(self, transit_data):
        """
        :type transit_data: gtfspy.transit_data_object.TransitData
        """

        # TODO: validate ISO4217 codes
        assert self.price >= 0
        assert self.payment_method in xrange(0, 2)
        assert self.transfers in xrange(0, 3)
        assert self.transfer_duration is None or self.transfer_duration >= 0

    def __eq__(self, other):
        if not isinstance(other, FareAttribute):
            return False

        return self.fare_id == other.fare_id and self.price == other.price and \
               self.currency_type == other.currency_type and self.payment_method == other.payment_method and \
               self.transfers == other.transfers and self.transfer_duration == other.transfer_duration

    def __ne__(self, other):
        return not (self == other)


class FareAttributeCollection(BaseGtfsObjectCollection):
    def __init__(self, transit_data, csv_file=None):
        BaseGtfsObjectCollection.__init__(self, transit_data)

        if csv_file is not None:
            self._load_file(csv_file)

    def add_fare_attribute(self, **kwargs):
        fare_attribute = FareAttribute(**kwargs)

        self._transit_data._changed()

        assert fare_attribute.fare_id not in self._objects
        self._objects[fare_attribute.fare_id] = fare_attribute
        return fare_attribute

    def remove(self, fare_attribute, recursive=False, clean_after=True):
        if not isinstance(fare_attribute, FareAttribute):
            fare_attribute = self[fare_attribute]
        else:
            assert self[fare_attribute.fare_id] is fare_attribute

        if recursive:
            fare_rules_to_clean = [fare_rule for fare_rule in self._transit_data.fare_rules
                                   if fare_rule.fare is fare_attribute]
            for fare_rule in fare_rules_to_clean:
                self._transit_data.fare_rules.remove(fare_rule, recursive=True, clean_after=False)
        else:
            assert next((fare_rule for fare_rule in self._transit_data.fare_rules if fare_rule.fare is fare_attribute),
                        None) is None

        del self._objects[fare_attribute.fare_id]

        if clean_after:
            self._transit_data.clean()

    def clean(self):
        fares_with_rules = {fare_rule.fare.fare_id for fare_rule in self._transit_data.fare_rules}
        to_clean = [fare_attribute for fare_attribute in self if fare_attribute.fare_id not in fares_with_rules]

        for fare_attribute in to_clean:
            del self._objects[fare_attribute.fare_id]

    def _load_file(self, csv_file):
        if isinstance(csv_file, str):
            with open(csv_file, "rb") as f:
                self._load_file(f)
        else:
            reader = csv.DictReader(csv_file)
            self._objects = {fare_attribute.fare_id: fare_attribute for fare_attribute in
                             (FareAttribute(**row) for row in reader)}

    def has_data(self):
        return len(self._objects) > 0

    def validate(self):
        for i, obj in self._objects.iteritems():
            assert i == obj.fare_id
            obj.validate(self._transit_data)
