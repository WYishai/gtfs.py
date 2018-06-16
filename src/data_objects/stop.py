import transit_data


class Stop:
    def __init__(self, transit_data, stop_id, stop_code, stop_name, stop_desc, stop_lat, stop_lon, location_type,
                 parent_station, zone_id, **kwargs):
        """
        :type transit_data: transit_data.TransitData
        """

        self.stop_id = int(stop_id)
        self.stop_code = stop_code
        self.stop_name = stop_name
        self.stop_desc = stop_desc
        self.stop_lat = float(stop_lat)
        self.stop_lon = float(stop_lon)
        self.is_central_station = bool(int(location_type))
        self.parent_station = parent_station
        # self.parent_station = None if parent_station == '' else transit_data.stops[parent_station]
        self.zone_id = None if zone_id == '' else int(zone_id)

        self.stop_times = []

        assert len(kwargs) == 0
