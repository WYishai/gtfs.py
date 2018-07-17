import csv

import gtfspy
from gtfspy.data_objects.base_object import BaseGtfsObjectCollection
from gtfspy.utils.parsing import parse_yes_no_unknown, yes_no_unknown_to_int
from gtfspy.utils.validating import not_none_or_empty, validate_true_false, validate_yes_no_unknown


class Stop:
    def __init__(self, transit_data, stop_id, stop_name, stop_lat, stop_lon, stop_code=None, stop_desc=None,
                 zone_id=None, stop_url=None, location_type=None, parent_station=None, stop_timezone=None,
                 wheelchair_boarding=None, **kwargs):
        """
        :type transit_data: gtfspy.transit_data_object.TransitData
        :type stop_id: str | int
        :type stop_name: str
        :type stop_lat: str | float
        :type stop_lon: str | float
        :type stop_code: str | None
        :type stop_desc: str | None
        :type zone_id: str | int | None
        :type stop_url: str | None
        :type location_type: str | bool | None
        :type parent_station: str | int | None
        :type stop_timezone: str | None
        :type wheelchair_boarding: str | int | None
        """

        self.id = int(stop_id)
        self.stop_name = stop_name
        self.stop_lat = float(stop_lat)
        self.stop_lon = float(stop_lon)

        self.attributes = {k: v for k, v in kwargs.iteritems() if not_none_or_empty(v)}
        if not_none_or_empty(stop_code):
            self.attributes["stop_code"] = str(stop_code)
        if not_none_or_empty(stop_desc):
            self.attributes["stop_desc"] = str(stop_desc)
        if not_none_or_empty(zone_id):
            self.attributes["zone_id"] = int(zone_id)
        if not_none_or_empty(stop_url):
            self.attributes["stop_url"] = str(stop_url)
        if not_none_or_empty(location_type):
            self.attributes["location_type"] = int(location_type)
        if not_none_or_empty(parent_station):
            # TODO: save the station object instead of the id
            self.attributes["parent_station"] = int(parent_station)
        if not_none_or_empty(stop_timezone):
            self.attributes["stop_timezone"] = str(stop_timezone)
        if not_none_or_empty(wheelchair_boarding):
            if isinstance(wheelchair_boarding, bool):
                self.attributes["wheelchair_boarding"] = yes_no_unknown_to_int(wheelchair_boarding)
            else:
                self.attributes["wheelchair_boarding"] = int(wheelchair_boarding)

        self.stop_times = []

    @property
    def stop_code(self):
        """
        :rtype: str | None
        """

        return self.attributes.get("stop_code", None)

    @stop_code.setter
    def stop_code(self, value):
        """
        :type value: str | None
        """

        self.attributes["stop_code"] = value

    @property
    def stop_desc(self):
        """
        :rtype: str | None
        """

        return self.attributes.get("stop_desc", None)

    @stop_desc.setter
    def stop_desc(self, value):
        """
        :type value: str | None
        """

        self.attributes["stop_desc"] = value

    @property
    def zone_id(self):
        """
        :rtype: int | None
        """

        return self.attributes.get("zone_id", None)

    @zone_id.setter
    def zone_id(self, value):
        """
        :type value: int | None
        """

        self.attributes["zone_id"] = value

    @property
    def stop_url(self):
        """
        :rtype: str | None
        """

        return self.attributes.get("stop_url", None)

    @stop_url.setter
    def stop_url(self, value):
        """
        :type value: str | None
        """

        self.attributes["stop_url"] = value

    @property
    def is_central_station(self):
        """
        :rtype: bool
        """

        return bool(self.attributes.get("location_type", False))

    @is_central_station.setter
    def is_central_station(self, value):
        """
        :type value: bool
        """

        self.attributes["location_type"] = int(value)

    @property
    def parent_station(self):
        """
        :rtype: int | None
        """

        return self.attributes.get("parent_station", None)

    @parent_station.setter
    def parent_station(self, value):
        """
        :type value: int | None
        """

        self.attributes["parent_station"] = value

    @property
    def stop_timezone(self):
        """
        :rtype: str | None
        """

        return self.attributes.get("stop_timezone", None)

    @stop_timezone.setter
    def stop_timezone(self, value):
        """
        :type value: str | None
        """

        self.attributes["stop_timezone"] = value

    @property
    def wheelchair_boarding(self):
        """
        :rtype: bool | None
        """

        return parse_yes_no_unknown(self.attributes.get("wheelchair_boarding", None))

    @wheelchair_boarding.setter
    def wheelchair_boarding(self, value):
        """
        :type value: bool | None
        """

        self.attributes["wheelchair_boarding"] = yes_no_unknown_to_int(value)

    def get_csv_fields(self):
        return ["stop_id", "stop_name", "stop_lat", "stop_lon"] + self.attributes.keys()

    def to_csv_line(self):
        result = dict(stop_id=self.id,
                      stop_name=self.stop_name,
                      stop_lat=self.stop_lat,
                      stop_lon=self.stop_lon,
                      **self.attributes)
        return result

    def validate(self, transit_data):
        """
        :type transit_data: gtfspy.transit_data_object.TransitData
        """

        assert validate_true_false(self.attributes.get("location_type", 0))
        assert self.parent_station is None or self.parent_station in transit_data.stops
        assert validate_yes_no_unknown(self.attributes.get("wheelchair_boarding", None))

    def __eq__(self, other):
        if not isinstance(other, Stop):
            return False

        return self.id == other.id and self.stop_name == other.stop_name and \
               self.stop_lat == other.stop_lat and self.stop_lon == other.stop_lon and \
               self.attributes == other.attributes

    def __ne__(self, other):
        return not (self == other)


class StopCollection(BaseGtfsObjectCollection):
    def __init__(self, transit_data, csv_file=None):
        BaseGtfsObjectCollection.__init__(self, transit_data, Stop)

        if csv_file is not None:
            self._load_file(csv_file)

    def add_stop(self, ignore_errors=False, condition=None, **kwargs):
        try:
            stop = Stop(transit_data=self._transit_data, **kwargs)

            if condition is not None and not condition(stop):
                return None

            self._transit_data._changed()

            assert stop.id not in self._objects
            self._objects[stop.id] = stop
            return stop
        except:
            if not ignore_errors:
                raise

    def add_stop_object(self, stop, recursive=False):
        assert isinstance(stop, Stop)

        if stop.id not in self:
            if stop.parent_station is not None:
                if recursive:
                    # TODO: add when we are changing stop.parent_station to be a Stop object
                    # self.add_stop_object(stop.parent_station, recursive=True)
                    pass
                else:
                    assert stop.parent_station in self
                    # TODO: change to this condition when we are changing stop.parent_station to be a Stop object
                    # assert stop.parent_station in self.stops
            self.add_stop(**stop.to_csv_line())
        else:
            assert stop == self[stop.id]

    def remove(self, stop, recursive=False, clean_after=True):
        if not isinstance(stop, Stop):
            stop = self[stop]
        else:
            assert self[stop.id] is stop

        if recursive:
            for stop_time in stop.stop_times:
                stop_time.trip.stop_times.remove(stop_time)
        else:
            assert len(stop.stop_times) == 0

        del self._objects[stop.id]

        if clean_after:
            self._transit_data.clean()

    def clean(self):
        to_clean = set()
        for stop in self:
            if len(stop.stop_times) == 0:
                to_clean.add(stop.id)

        for stop in self:
            while stop.parent_station is not None and stop.id not in to_clean and stop.parent_station in to_clean:
                to_clean.remove(stop.parent_station)
                stop = self[stop.parent_station]

        for stop_id in to_clean:
            del self._objects[stop_id]

    def _load_file(self, csv_file, ignore_errors=False, filter=None):
        if isinstance(csv_file, str):
            with open(csv_file, "rb") as f:
                self._load_file(f, ignore_errors=ignore_errors, filter=filter)
        else:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.add_stop(ignore_errors=ignore_errors, condition=filter, **row)
