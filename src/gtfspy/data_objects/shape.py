import csv
from operator import attrgetter

from gtfspy.data_objects.base_object import BaseGtfsObjectCollection
from gtfspy.utils.validating import not_none_or_empty
from sortedcontainers import SortedList


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

        self.attributes = {k: v for k, v in kwargs.iteritems() if not_none_or_empty(v)}
        if not_none_or_empty(shape_dist_traveled):
            self.attributes["shape_dist_traveled"] = float(shape_dist_traveled)

    @property
    def shape_dist_traveled(self):
        """
        :rtype: float | None
        """

        return self.attributes.get("shape_dist_traveled", None)

    @shape_dist_traveled.setter
    def shape_dist_traveled(self, value):
        """
        :type value: float | None
        """

        self.attributes["shape_dist_traveled"] = value

    def validate(self, transit_data):
        # TODO: validate ShapePoint values
        pass

    def __eq__(self, other):
        if not isinstance(other, ShapePoint):
            return False

        return self.shape_pt_lat == other.shape_pt_lat and self.shape_pt_lon == other.shape_pt_lon and \
               self.shape_pt_sequence == other.shape_pt_sequence and \
               (self.shape_dist_traveled is None or other.shape_dist_traveled is None or
                self.shape_dist_traveled == other.shape_dist_traveled) and \
               self.attributes == other.attributes

    def __ne__(self, other):
        return not (self == other)


class Shape:
    def __init__(self, shape_id):
        """
        :type shape_id: str | int
        """

        self.shape_id = int(shape_id)

        self.shape_points = SortedList(key=attrgetter("shape_pt_sequence"))

    def get_csv_fields(self):
        return ["shape_id", "shape_pt_lat", "shape_pt_lon", "shape_pt_sequence"] + \
               list({key for shape_point in self.shape_points for key in shape_point.attributes.iterkeys()})

    def to_csv_line(self):
        for shape_point in self.shape_points:
            result = dict(shape_id=self.shape_id,
                          shape_pt_lat=shape_point.shape_pt_lat,
                          shape_pt_lon=shape_point.shape_pt_lon,
                          shape_pt_sequence=shape_point.shape_pt_sequence,
                          **shape_point.attributes)
            yield result

    def validate(self, transit_data):
        """
        :type transit_data: transit_data_object.TransitData
        """

        assert len(self.shape_points) != 0
        for shape_point in self.shape_points:
            shape_point.validate(transit_data)

    def __eq__(self, other):
        if not isinstance(other, Shape):
            return False

        return self.shape_id == other.shape_id and self.shape_points == other.shape_points

    def __ne__(self, other):
        return not (self == other)


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
