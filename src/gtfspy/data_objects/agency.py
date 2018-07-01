import csv

import gtfspy
from gtfspy.data_objects.base_object import BaseGtfsObjectCollection
from gtfspy.data_objects.line import LineCollection
from gtfspy.utils.parsing import parse_or_default


class Agency:
    def __init__(self, transit_data, agency_id, agency_name, agency_url, agency_timezone, agency_lang=None,
                 agency_phone=None, agency_email=None, agency_fare_url=None, **kwargs):
        """
        :type transit_data: gtfspy.transit_data_object.TransitData
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

    def get_csv_fields(self):
        return ["agency_id", "agency_name", "agency_url", "agency_timezone", "agency_lang", "agency_phone",
                "agency_email", "agency_fare_url"]

    def to_csv_line(self):
        return {"agency_id": self.agency_id,
                "agency_name": self.agency_name,
                "agency_url": self.agency_url,
                "agency_timezone": self.agency_timezone,
                "agency_lang": self.agency_lang,
                "agency_phone": self.agency_phone,
                "agency_email": self.agency_email,
                "agency_fare_url": self.agency_fare_url}

    def validate(self, transit_data):
        """
        :type transit_data: gtfspy.transit_data_object.TransitData
        """

        self.lines.validate()

    def __eq__(self, other):
        if not isinstance(other, Agency):
            return False

        return self.agency_id == other.agency_id and self.agency_name == other.agency_name and \
               self.agency_url == other.agency_url and self.agency_timezone == other.agency_timezone and \
               self.agency_lang == other.agency_lang and self.agency_phone == other.agency_phone and \
               self.agency_email == other.agency_email and self.agency_fare_url == other.agency_fare_url


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

    def remove(self, agency, recursive=False, clean_after=True):
        if not isinstance(agency, Agency):
            agency = self[agency]
        else:
            assert self[agency.agency_id] is agency

        if recursive:
            for line in list(agency.lines):
                agency.lines.remove(line, recursive=True, clean_after=False)
        else:
            for line in agency.lines:
                assert len(line.routes) == 0

        del self._objects[agency.agency_id]

        if clean_after:
            self._transit_data.clean()

    def clean(self):
        to_clean = []
        for agency in self:
            if next((route for line in agency.lines for route in line.routes), None) is None:
                to_clean.append(agency)

        for agency in to_clean:
            del self._objects[agency.agency_id]

    def _load_file(self, csv_file):
        if isinstance(csv_file, str):
            with open(csv_file, "rb") as f:
                self._load_file(f)
        else:
            reader = csv.DictReader(csv_file)
            self._objects = {agency.agency_id: agency for agency in
                             (Agency(transit_data=self._transit_data, **row) for row in reader)}

    def validate(self):
        for i, obj in self._objects.iteritems():
            assert i == obj.agency_id
            obj.validate(self._transit_data)