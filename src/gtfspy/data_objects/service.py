from datetime import datetime, date

from gtfspy.data_objects.base_object import BaseGtfsObjectCollection
from gtfspy.utils.parsing import parse_or_default, str_to_bool
from gtfspy.utils.validating import not_none_or_empty


class Service(object):
    def __init__(self, service_id, start_date, end_date, sunday=None, monday=None, tuesday=None, wednesday=None,
                 thursday=None, friday=None, saturday=None, **kwargs):
        """
        :type service_id: str | int
        :type start_date: date | str
        :type end_date: date | str
        :type sunday: str | bool | None
        :type monday: str | bool | None
        :type tuesday: str | bool | None
        :type wednesday: str | bool | None
        :type thursday: str | bool | None
        :type friday: str | bool | None
        :type saturday: str | bool | None
        """

        self._id = int(service_id)
        self.start_date = start_date if isinstance(start_date, date) else datetime.strptime(start_date, "%Y%m%d").date()
        self.end_date = end_date if isinstance(end_date, date) else datetime.strptime(end_date, "%Y%m%d").date()
        sunday = parse_or_default(sunday, False, str_to_bool)
        monday = parse_or_default(monday, False, str_to_bool)
        tuesday = parse_or_default(tuesday, False, str_to_bool)
        wednesday = parse_or_default(wednesday, False, str_to_bool)
        thursday = parse_or_default(thursday, False, str_to_bool)
        friday = parse_or_default(friday, False, str_to_bool)
        saturday = parse_or_default(saturday, False, str_to_bool)
        self.days_relevance = [sunday, monday, tuesday, wednesday, thursday, friday, saturday]

        self.attributes = {k: v for k, v in kwargs.iteritems() if not_none_or_empty(v)}

    @property
    def id(self):
        return self._id

    @property
    def sunday(self):
        """
        :rtype: bool
        """

        return self.days_relevance[0]

    @sunday.setter
    def sunday(self, value):
        """
        :type value: bool | int
        """

        self.days_relevance[0] = bool(value)

    @property
    def monday(self):
        """
        :rtype: bool
        """

        return self.days_relevance[1]

    @monday.setter
    def monday(self, value):
        """
        :type value: bool | int
        """

        self.days_relevance[1] = bool(value)

    @property
    def tuesday(self):
        """
        :rtype: bool
        """

        return self.days_relevance[2]

    @tuesday.setter
    def tuesday(self, value):
        """
        :type value: bool | int
        """

        self.days_relevance[2] = bool(value)

    @property
    def wednesday(self):
        """
        :rtype: bool
        """

        return self.days_relevance[3]

    @wednesday.setter
    def wednesday(self, value):
        """
        :type value: bool | int
        """

        self.days_relevance[3] = bool(value)

    @property
    def thursday(self):
        """
        :rtype: bool
        """

        return self.days_relevance[4]

    @thursday.setter
    def thursday(self, value):
        """
        :type value: bool | int
        """

        self.days_relevance[4] = bool(value)

    @property
    def friday(self):
        """
        :rtype: bool
        """

        return self.days_relevance[5]

    @friday.setter
    def friday(self, value):
        """
        :type value: bool | int
        """

        self.days_relevance[5] = bool(value)

    @property
    def saturday(self):
        """
        :rtype: bool
        """

        return self.days_relevance[6]

    @saturday.setter
    def saturday(self, value):
        """
        :type value: bool | int
        """

        self.days_relevance[6] = bool(value)

    def is_active_on(self, date):
        """
        :rtype: bool
        """

        return self.days_relevance[date.isoweekday() % 7]

    def get_csv_fields(self):
        return ["service_id", "start_date", "end_date", "sunday", "monday", "tuesday", "wednesday", "thursday",
                "friday", "saturday"] + self.attributes.keys()

    def to_csv_line(self):
        return dict(service_id=self.id,
                    start_date=self.start_date.strftime("%Y%m%d"),
                    end_date=self.end_date.strftime("%Y%m%d"),
                    sunday=int(self.sunday),
                    monday=int(self.monday),
                    tuesday=int(self.tuesday),
                    wednesday=int(self.wednesday),
                    thursday=int(self.thursday),
                    friday=int(self.friday),
                    saturday=int(self.saturday),
                    **self.attributes)

    def validate(self, transit_data):
        """
        :type transit_data: transit_data_object.TransitData
        """

        assert self.start_date <= self.end_date
        assert True in self.days_relevance

    def __eq__(self, other):
        if not isinstance(other, Service):
            return False

        return self.id == other.id and self.start_date == other.start_date and \
               self.end_date == other.end_date and self.days_relevance == other.days_relevance and \
               self.attributes == other.attributes

    def __ne__(self, other):
        return not (self == other)


class ServiceCollection(BaseGtfsObjectCollection):
    def __init__(self, transit_data, csv_file=None):
        BaseGtfsObjectCollection.__init__(self, transit_data, Service)

        if csv_file is not None:
            self._load_file(csv_file)

    def add(self, ignore_errors=False, condition=None, **kwargs):
        try:
            service = Service(**kwargs)

            if condition is not None and not condition(service):
                return None

            self._transit_data._changed()

            assert service.id not in self._objects
            self._objects[service.id] = service
            return service
        except:
            if not ignore_errors:
                raise

    def add_object(self, service, recursive=False):
        assert isinstance(service, Service)

        if service.id not in self:
            return self.add(**service.to_csv_line())
        else:
            old_service = self[service.id]
            assert service == old_service
            return old_service

    def remove(self, service, recursive=False, clean_after=True):
        if not isinstance(service, Service):
            service = self[service]
        else:
            assert self[service.id] is service

        if recursive:
            for trip in self._transit_data.trips:
                if trip.service is service:
                    self._transit_data.trips.remove(trip, recursive=True, clean_after=False)
        else:
            assert next((trip for trip in self._transit_data.trips if trip.service is service), None) is None

        del self._objects[service.id]

        if clean_after:
            self._transit_data.clean()

    def clean(self):
        to_clean = []
        for service in self:
            if next((trip for trip in self._transit_data.trips if trip.service is service), None) is None:
                to_clean.append(service)

        for service in to_clean:
            del self._objects[service.id]
