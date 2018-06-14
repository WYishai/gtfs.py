import transit_data


class StopTime:
    def __init__(self, transit_data, trip_id, arrival_time, departure_time, stop_id, stop_sequence, pickup_type,
                 drop_off_type, shape_dist_traveled, stop_headsign=None, timepoint=None, **kwargs):
        """
        :type transit_data: transit_data.TransitData
        """

        self.trip = transit_data.trips[trip_id]
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.stop = transit_data.stops[stop_id]
        self.stop_sequence = stop_sequence
        self.stop_headsign = stop_headsign
        self.pickup_type = pickup_type
        self.drop_off_type = drop_off_type
        self.shape_dist_traveled = shape_dist_traveled
        self.timepoint = timepoint

        assert len(kwargs) == 0
