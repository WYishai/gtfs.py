import csv

import gtfspy
from gtfspy.data_objects.base_object import BaseGtfsObjectCollection
from gtfspy.data_objects.line import LineCollection
from gtfspy.utils.validating import not_none_or_empty


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

        self.attributes = {k: v for k, v in kwargs.iteritems() if not_none_or_empty(v)}
        if not_none_or_empty(agency_lang):
            self.attributes["agency_lang"] = str(agency_lang)
        if not_none_or_empty(agency_phone):
            self.attributes["agency_phone"] = str(agency_phone)
        if not_none_or_empty(agency_email):
            self.attributes["agency_email"] = str(agency_email)
        if not_none_or_empty(agency_fare_url):
            self.attributes["agency_fare_url"] = str(agency_fare_url)

        self.lines = LineCollection(transit_data, self)

    @property
    def agency_lang(self):
        """
        :rtype: str | None
        """

        return self.attributes.get("agency_lang", None)

    @agency_lang.setter
    def agency_lang(self, value):
        """
        :type value: str | None
        """

        self.attributes["agency_lang"] = value

    @property
    def agency_phone(self):
        """
        :rtype: str | None
        """

        return self.attributes.get("agency_phone", None)

    @agency_phone.setter
    def agency_phone(self, value):
        """
        :type value: str | None
        """

        self.attributes["agency_phone"] = value

    @property
    def agency_email(self):
        """
        :rtype: str | None
        """

        return self.attributes.get("agency_email", None)

    @agency_email.setter
    def agency_email(self, value):
        """
        :type value: str | None
        """

        self.attributes["agency_email"] = value

    @property
    def agency_fare_url(self):
        """
        :rtype: str | None
        """

        return self.attributes.get("agency_fare_url", None)

    @agency_fare_url.setter
    def agency_fare_url(self, value):
        """
        :type value: str | None
        """

        self.attributes["agency_fare_url"] = value

    def get_line(self, route):
        return self.lines.get_line(route)

    def get_csv_fields(self):
        return ["agency_id", "agency_name", "agency_url", "agency_timezone"] + self.attributes.keys()

    def to_csv_line(self):
        result = dict(agency_id=self.agency_id,
                      agency_name=self.agency_name,
                      agency_url=self.agency_url,
                      agency_timezone=self.agency_timezone,
                      **self.attributes)
        return result

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
               self.attributes == other.attributes

    def __ne__(self, other):
        return not (self == other)


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
