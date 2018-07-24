import gtfspy
from gtfspy.data_objects import Agency
from gtfspy.data_objects.base_object import BaseGtfsObjectCollection
from gtfspy.utils.parsing import parse_or_default
from gtfspy.utils.validating import not_none_or_empty


class FareAttribute(object):
    def __init__(self, transit_data, fare_id, price, currency_type, payment_method, transfers, agency_id=None,
                 transfer_duration=None,
                 **kwargs):
        self._id = fare_id
        self.price = float(price)
        self.currency_type = currency_type
        self.payment_method = int(payment_method)
        self.transfers = parse_or_default(transfers, None, int)

        self.attributes = {k: v for k, v in kwargs.iteritems() if not_none_or_empty(v)}
        if not_none_or_empty(agency_id):
            self.attributes["agency_id"] = transit_data.agencies[int(agency_id)]
        if not_none_or_empty(transfer_duration):
            self.attributes["transfer_duration"] = int(transfer_duration)

    @property
    def id(self):
        return self._id

    @property
    def is_prepaid_needed(self):
        """
        :rtype: bool | None
        """

        return bool(self.payment_method)

    @is_prepaid_needed.setter
    def is_prepaid_needed(self, value):
        """
        :type value: bool | None
        """

        self.payment_method = int(value)

    @property
    def agency(self):
        """
        :rtype: Agency | None
        """

        return self.attributes.get("agency_id", None)

    @agency.setter
    def agency(self, value):
        """
        :type value: Agency | None
        """

        self.attributes["agency_id"] = value

    @property
    def transfer_duration(self):
        """
        :rtype: int | None
        """

        return self.attributes.get("transfer_duration", None)

    @transfer_duration.setter
    def transfer_duration(self, value):
        """
        :type value: int | None
        """

        self.attributes["transfer_duration"] = value

    def get_csv_fields(self):
        return ["fare_id", "price", "currency_type", "payment_method", "transfers"] + self.attributes.keys()

    def to_csv_line(self):
        result = dict(fare_id=self.id,
                      price="%.2f" % (self.price,),
                      currency_type=self.currency_type,
                      payment_method=self.payment_method,
                      transfers=self.transfers,
                      **self.attributes)

        if "agency_id" in result:
            result["agency_id"] = self.agency.id

        return result

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

        return self.id == other.id and self.price == other.price and \
               self.currency_type == other.currency_type and self.payment_method == other.payment_method and \
               self.transfers == other.transfers and self.attributes == other.attributes

    def __ne__(self, other):
        return not (self == other)


class FareAttributeCollection(BaseGtfsObjectCollection):
    def __init__(self, transit_data, csv_file=None):
        BaseGtfsObjectCollection.__init__(self, transit_data, FareAttribute)

        if csv_file is not None:
            self._load_file(csv_file)

    def add(self, ignore_errors=False, condition=None, **kwargs):
        try:
            fare_attribute = FareAttribute(transit_data=self._transit_data, **kwargs)

            if condition is not None and not condition(fare_attribute):
                return None

            self._transit_data._changed()

            assert fare_attribute.id not in self._objects
            self._objects[fare_attribute.id] = fare_attribute
            return fare_attribute
        except:
            if not ignore_errors:
                raise

    def add_object(self, fare_attribute, recursive=False):
        assert isinstance(fare_attribute, FareAttribute)

        if fare_attribute.id not in self:
            return self.add(**fare_attribute.to_csv_line())
        else:
            old_fare_attribute = self[fare_attribute.id]
            assert fare_attribute == old_fare_attribute
            return old_fare_attribute

    def remove(self, fare_attribute, recursive=False, clean_after=True):
        if not isinstance(fare_attribute, FareAttribute):
            fare_attribute = self[fare_attribute]
        else:
            assert self[fare_attribute.id] is fare_attribute

        if recursive:
            fare_rules_to_clean = [fare_rule for fare_rule in self._transit_data.fare_rules
                                   if fare_rule.fare is fare_attribute]
            for fare_rule in fare_rules_to_clean:
                self._transit_data.fare_rules.remove(fare_rule, recursive=True, clean_after=False)
        else:
            assert next((fare_rule for fare_rule in self._transit_data.fare_rules if fare_rule.fare is fare_attribute),
                        None) is None

        del self._objects[fare_attribute.id]

        if clean_after:
            self._transit_data.clean()

    def clean(self):
        fares_with_rules = {fare_rule.fare.id for fare_rule in self._transit_data.fare_rules}
        to_clean = [fare_attribute for fare_attribute in self if fare_attribute.id not in fares_with_rules]

        for fare_attribute in to_clean:
            del self._objects[fare_attribute.id]

    def has_data(self):
        return len(self._objects) > 0
