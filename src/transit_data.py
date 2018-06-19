from zipfile import ZipFile

from data_objects import *


class TransitData:
    def __init__(self, gtfs_file=None):
        self.agencies = AgencyCollection(self)
        self.routes = RouteCollection(self)
        self.shapes = ShapeCollection(self)
        self.calendar = ServiceCollection(self)
        self.trips = TripCollection(self)
        self.stops = StopCollection(self)

        self.has_changed = False
        self.is_verified = False

        if gtfs_file is not None:
            self.load_gtfs_file(gtfs_file)

    def _changed(self):
        self.has_changed = True
        self.is_verified = False

    def load_gtfs_file(self, gtfs_file):
        assert not self.has_changed

        # TODO: replace this check with check if this object is file-like
        if not isinstance(gtfs_file, file):
            with open(gtfs_file, "rb") as gtfs_real_file:
                self.load_gtfs_file(gtfs_real_file)

        self._changed()

        zip_file = ZipFile(gtfs_file)

        with zip_file.open("agency.txt", "r") as agency_file:
            self.agencies._load_file(agency_file)

        with zip_file.open("routes.txt", "r") as routes_file:
            self.routes._load_file(routes_file)

        with zip_file.open("shapes.txt", "r") as shapes_file:
            self.shapes._load_file(shapes_file)

        with zip_file.open("calendar.txt", "r") as calendar_file:
            self.calendar._load_file(calendar_file)

        with zip_file.open("trips.txt", "r") as trips_file:
            self.trips._load_file(trips_file)

        with zip_file.open("stops.txt", "r") as stops_file:
            self.stops._load_file(stops_file)

        with zip_file.open("stop_times.txt", "r") as stop_times_file:
            reader = csv.DictReader(stop_times_file)
            for row in reader:
                stop_time = StopTime(transit_data=self, **row)
                stop_time.trip.stop_times.append(stop_time)
                stop_time.stop.stop_times.append(stop_time)

    def add_agency(self, **kwargs):
        self.agencies.add_agency(**kwargs)

    def add_route(self, **kwargs):
        self.routes.add_route(**kwargs)

    def add_shape(self, **kwargs):
        self.shapes.add_shape(**kwargs)

    def add_service(self, **kwargs):
        self.calendar.add_service(**kwargs)

    def add_trip(self, **kwargs):
        self.trips.add_trip(**kwargs)

    def add_stop(self, **kwargs):
        self.stops.add_stop(**kwargs)

    def add_stop_time(self, **kwargs):
        stop_time = StopTime(transit_data=self, **kwargs)

        assert stop_time.stop_sequence not in (st.stop_sequence for st in stop_time.trip.stop_times)
        self._changed()
        stop_time.trip.stop_times.append(stop_time)
        stop_time.stop.stop_times.append(stop_time)
        return stop_time

    def verify(self):
        pass

        self.is_verified = True
