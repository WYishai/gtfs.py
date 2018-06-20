import csv
from datetime import datetime

from data_objects.base_object import BaseGtfsObjectCollection
from utils.parsing import parse_or_default, str_to_bool


class Service:
    def __init__(self, service_id, start_date, end_date, sunday=None, monday=None, tuesday=None, wednesday=None,
                 thursday=None, friday=None, saturday=None, **kwargs):
        """
        :type service_id: str | int
        :type start_date: datetime | str
        :type end_date: datetime | str
        :type sunday: str | bool | None
        :type monday: str | bool | None
        :type tuesday: str | bool | None
        :type wednesday: str | bool | None
        :type thursday: str | bool | None
        :type friday: str | bool | None
        :type saturday: str | bool | None
        """

        self.service_id = int(service_id)
        self.start_date = start_date if isinstance(start_date, datetime) else datetime.strptime(start_date, "%Y%m%d").date()
        self.end_date = end_date if isinstance(end_date, datetime) else datetime.strptime(end_date, "%Y%m%d").date()
        self.sunday = parse_or_default(sunday, False, str_to_bool)
        self.monday = parse_or_default(monday, False, str_to_bool)
        self.tuesday = parse_or_default(tuesday, False, str_to_bool)
        self.wednesday = parse_or_default(wednesday, False, str_to_bool)
        self.thursday = parse_or_default(thursday, False, str_to_bool)
        self.friday = parse_or_default(friday, False, str_to_bool)
        self.saturday = parse_or_default(saturday, False, str_to_bool)
        self.days_relevance = [self.sunday, self.monday, self.tuesday, self.wednesday, self.thursday, self.friday,
                               self.saturday]

        assert len(kwargs) == 0

    def is_active_on(self, date):
        return self.days_relevance[date.isoweekday() % 7]

    def get_csv_fields(self):
        return ["service_id", "start_date", "end_date", "sunday", "monday", "tuesday", "wednesday", "thursday",
                "friday", "saturday"]

    def to_csv_line(self):
        return {"service_id": self.service_id,
                "start_date": self.start_date.strftime("%Y%m%d"),
                "end_date": self.end_date.strftime("%Y%m%d"),
                "sunday": 1 if self.sunday else 0,
                "monday": 1 if self.monday else 0,
                "tuesday": 1 if self.tuesday else 0,
                "wednesday": 1 if self.wednesday else 0,
                "thursday": 1 if self.thursday else 0,
                "friday": 1 if self.friday else 0,
                "saturday": 1 if self.saturday else 0}


class ServiceCollection(BaseGtfsObjectCollection):
    def __init__(self, transit_data, csv_file=None):
        BaseGtfsObjectCollection.__init__(self, transit_data)

        if csv_file is not None:
            self._load_file(csv_file)

    def add_service(self, **kwargs):
        service = Service(**kwargs)

        self._transit_data._changed()

        assert service.service_id not in self._objects
        self._objects[service.service_id] = service
        return service

    def _load_file(self, csv_file):
        if isinstance(csv_file, str):
            with open(csv_file, "rb") as f:
                self._load_file(f)
        else:
            reader = csv.DictReader(csv_file)
            self._objects = {service.service_id: service for service in
                             (Service(**row) for row in reader)}
