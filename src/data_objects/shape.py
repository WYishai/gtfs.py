import csv
from operator import attrgetter

from sortedcontainers import SortedList

from data_objects.base_object import BaseGtfsObjectCollection
from utils.parsing import parse_or_default


class ShapePoint:
    def __init__(self, shape_pt_lat, shape_pt_lon, shape_pt_sequence, shape_dist_traveled=None, **kwargs):
        """
        :type shape_pt_lat: str | float
        :type shape_pt_lon: str | float
        :type shape_pt_sequence: str | int
        :type shape_dist_traveled: str | float | None
        """

        self.shape_pt_lat = float(shape_pt_lat)
        self.shape_pt_lon = float(shape_pt_lon)
        self.shape_pt_sequence = int(shape_pt_sequence)
        self.shape_dist_traveled = parse_or_default(shape_dist_traveled, None, float)

        assert len(kwargs) == 0


class Shape:
    def __init__(self, shape_id):
        """
        :type shape_id: str | int
        """

        self.shape_id = int(shape_id)

        self.shape_points = SortedList(key=attrgetter("shape_pt_sequence"))

    def get_csv_fields(self):
        return ["shape_id", "shape_pt_lat", "shape_pt_lon", "shape_pt_sequence", "shape_dist_traveled"]

    def to_csv_line(self):
        for shape_point in self.shape_points:
            yield {"shape_id": self.shape_id,
                   "shape_pt_lat": shape_point.shape_pt_lat,
                   "shape_pt_lon": shape_point.shape_pt_lon,
                   "shape_pt_sequence": shape_point.shape_pt_sequence,
                   "shape_dist_traveled": shape_point.shape_dist_traveled}

    def validate(self, transit_data):
        """
        :type transit_data: transit_data.TransitData
        """

        assert len(self.shape_points) != 0


class ShapeCollection(BaseGtfsObjectCollection):
    def __init__(self, transit_data, csv_file=None):
        BaseGtfsObjectCollection.__init__(self, transit_data)

        if csv_file is not None:
            self._load_file(csv_file)

    def add_shape_point(self, **kwargs):
        shape_id = int(kwargs.pop("shape_id"))
        shape_point = ShapePoint(**kwargs)

        self._transit_data._changed()

        if shape_id not in self._objects:
            shape = Shape(shape_id)
            self._objects[shape_id] = shape
        else:
            shape = self[shape_id]
        shape.shape_points.add(shape_point)
        return shape_point

    def remove(self, shape, recursive=False, clean_after=True):
        if not isinstance(shape, Shape):
            shape = self[shape]
        else:
            assert self[shape.shape_id] is shape

        if recursive:
            for trip in self._transit_data.trips:
                if trip.shape is shape:
                    self._transit_data.trips.remove(trip, recursive=True, clean_after=False)
        else:
            assert next((trip for trip in self._transit_data.trips if trip.shape is shape), None) is None

        del self._objects[shape.shape_id]

        if clean_after:
            self._transit_data.clean()

    def clean(self):
        to_clean = []
        for shape in self:
            if next((trip for trip in self._transit_data.trips if trip.shape is shape), None) is None:
                to_clean.append(shape)

        for shape in to_clean:
            del self._objects[shape.shape_id]

    def _load_file(self, csv_file):
        if isinstance(csv_file, str):
            with open(csv_file, "rb") as f:
                self._load_file(f)
        else:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.add_shape_point(**row)

    def save(self, csv_file):
        if isinstance(csv_file, str):
            with open(csv_file, "wb") as f:
                self.save(f)
        else:
            fields = []
            for obj in self:
                fields += (field for field in obj.get_csv_fields() if field not in fields)

            writer = csv.DictWriter(csv_file, fieldnames=fields, restval=None)
            writer.writeheader()
            for obj in self:
                writer.writerows(obj.to_csv_line())

    def validate(self):
        for i, obj in self._objects.iteritems():
            assert i == obj.shape_id
            obj.validate(self._transit_data)
