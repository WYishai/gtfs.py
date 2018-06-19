import csv

from data_objects.base_object import BaseGtfsObjectCollection
from data_objects.line import LineCollection
from utils.parsing import parse_or_default


class Agency:
    def __init__(self, transit_data, agency_id, agency_name, agency_url, agency_timezone, agency_lang=None,
                 agency_phone=None, agency_email=None, agency_fare_url=None, **kwargs):
        """
        :type agency_id: str | int
        :type agency_name: str
        :type agency_url: str
        :type agency_timezone: str
        :type agency_lang: str | None
        :type agency_phone: str | None
        :type agency_email: str | None
        :type agency_fare_url: str | None
        """

        self.agency_id = int(agency_id)
        self.agency_name = agency_name
        self.agency_url = agency_url
        self.agency_timezone = agency_timezone
        self.agency_lang = parse_or_default(agency_lang, None, str)
        self.agency_phone = parse_or_default(agency_phone, None, str)
        self.agency_email = parse_or_default(agency_email, None, str)
        self.agency_fare_url = parse_or_default(agency_fare_url, None, str)

        self.lines = LineCollection(transit_data, self)

        assert len(kwargs) == 0

    def get_line(self, route):
        return self.lines.get_line(route)


class AgencyCollection(BaseGtfsObjectCollection):
    def __init__(self, transit_data, csv_file=None):
        BaseGtfsObjectCollection.__init__(self, transit_data)

        if csv_file is not None:
            self._load_file(csv_file)

    def add_agency(self, **kwargs):
        agency = Agency(transit_data=self._transit_data, **kwargs)

        self._transit_data._changed()

        assert agency.agency_id not in self._objects
        self._objects[agency.agency_id] = agency
        return agency

    def _load_file(self, csv_file):
        if isinstance(csv_file, str):
            with open(csv_file, "rb") as f:
                self._load_file(f)
        else:
            reader = csv.DictReader(csv_file)
            self._objects = {agency.agency_id: agency for agency in
                             (Agency(transit_data=self._transit_data, **row) for row in reader)}
