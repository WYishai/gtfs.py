import transit_data
from utils.time import parse_timedelta


class StopTime:
    def __init__(self, transit_data, trip_id, arrival_time, departure_time, stop_id, stop_sequence, pickup_type,
                 drop_off_type, shape_dist_traveled, stop_headsign=None, timepoint=None, **kwargs):
        """
        :type transit_data: transit_data.TransitData
        """

        self.trip = transit_data.trips[trip_id]
        self.arrival_time = parse_timedelta(arrival_time)
        self.departure_time = parse_timedelta(departure_time)
        self.stop = transit_data.stops[int(stop_id)]
        self.stop_sequence = int(stop_sequence)
        self.pickup_type = True if pickup_type == '' else not bool(int(pickup_type))
        self.drop_off_type = True if drop_off_type == '' else not bool(int(drop_off_type))
        self.shape_dist_traveled = 0 if shape_dist_traveled == '' else float(shape_dist_traveled)
        self.stop_headsign = stop_headsign
        self.timepoint = timepoint

        assert len(kwargs) == 0
