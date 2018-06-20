import csv

from data_objects.base_object import BaseGtfsObjectCollection
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

    def get_csv_fields(self):
        return ["shape_id", "shape_pt_lat", "shape_pt_lon", "shape_pt_sequence", "shape_dist_traveled"]

    def to_csv_line(self):
        return {"shape_id": self.shape_id,
                "shape_pt_lat": self.shape_pt_lat,
                "shape_pt_lon": self.shape_pt_lon,
                "shape_pt_sequence": self.shape_pt_sequence,
                "shape_dist_traveled": self.shape_dist_traveled}


class ShapeCollection(BaseGtfsObjectCollection):
    def __init__(self, transit_data, csv_file=None):
        BaseGtfsObjectCollection.__init__(self, transit_data)

        if csv_file is not None:
            self._load_file(csv_file)

    def add_shape(self, **kwargs):
        shape = Shape(**kwargs)

        self._transit_data._changed()

        assert shape.shape_id not in self._objects
        self._objects[shape.shape_id] = shape
        return shape

    def _load_file(self, csv_file):
        if isinstance(csv_file, str):
            with open(csv_file, "rb") as f:
                self._load_file(f)
        else:
            reader = csv.DictReader(csv_file)
            self._objects = {shape.shape_id: shape for shape in
                             (Shape(**row) for row in reader)}
