import transit_data
from utils.parsing import parse_or_default, str_to_bool


class Stop:
    def __init__(self, transit_data, stop_id, stop_name, stop_lat, stop_lon, stop_code=None, stop_desc=None,
                 zone_id=None, stop_url=None, location_type=None, parent_station=None, stop_timezone=None,
                 wheelchair_boarding=None, **kwargs):
        """
        :type transit_data: transit_data.TransitData
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

        self.stop_id = int(stop_id)
        self.stop_name = stop_name
        self.stop_lat = float(stop_lat)
        self.stop_lon = float(stop_lon)
        self.stop_code = parse_or_default(stop_code, None, str)
        self.stop_desc = parse_or_default(stop_desc, None, str)
        self.zone_id = parse_or_default(zone_id, None, int)
        self.stop_url = parse_or_default(stop_url, None, str)
        self.is_central_station = parse_or_default(location_type, False, str_to_bool)
        self.parent_station = parse_or_default(parent_station, None, int)
        # self.parent_station = None if parent_station == '' else transit_data.stops[parent_station]
        self.stop_timezone = parse_or_default(stop_timezone, None, str)
        self.wheelchair_boarding = parse_or_default(wheelchair_boarding, None, int)

        self.stop_times = []

        assert len(kwargs) == 0
