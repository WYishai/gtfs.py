from utils.parsing import parse_or_default


class Shape:
    def __init__(self, shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence, shape_dist_traveled=None, **kwargs):
        """
        :type shape_id: str | int
        :type shape_pt_lat: str | float
        :type shape_pt_lon: str | float
        :type shape_pt_sequence: str | int
        :type shape_dist_traveled: str | float | None
        """

        # TODO: split the shape to separated shape points

        self.shape_id = int(shape_id)
        self.shape_pt_lat = float(shape_pt_lat)
        self.shape_pt_lon = float(shape_pt_lon)
        self.shape_pt_sequence = int(shape_pt_sequence)
        self.shape_dist_traveled = parse_or_default(shape_dist_traveled, None, float)

        assert len(kwargs) == 0
