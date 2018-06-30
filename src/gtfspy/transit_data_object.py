import os
import zipfile
from cStringIO import StringIO
from zipfile import ZipFile

from gtfspy.data_objects import *


class TransitData:
    def __init__(self, gtfs_file=None, validate=True):
        self.agencies = AgencyCollection(self)
        self.routes = RouteCollection(self)
        self.shapes = ShapeCollection(self)
        self.calendar = ServiceCollection(self)
        self.trips = TripCollection(self)
        self.stops = StopCollection(self)

        # TODO: create dedicated object for unknown files collection
        # TODO: save the headers order in the unknown files
        self.unknown_files = {}

        self.has_changed = False
        self.is_validated = True

        if gtfs_file is not None:
            self.load_gtfs_file(gtfs_file, validate=validate)

    def _changed(self):
        self.has_changed = True
        self.is_validated = False

    def load_gtfs_file(self, gtfs_file, validate=True):
        assert not self.has_changed

        with ZipFile(gtfs_file) as zip_file:
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
                    stop_time.trip.stop_times.add(stop_time)
                    stop_time.stop.stop_times.append(stop_time)

            for inner_file in zip_file.filelist:
                if inner_file.filename not in ["agency.txt", "routes.txt", "shapes.txt", "calendar.txt", "trips.txt",
                                               "stops.txt", "stop_times.txt"]:
                    with zip_file.open(inner_file, "r") as f:
                        self.unknown_files[inner_file.filename] = UnknownFile(f)

        if validate:
            self.validate()

    def save(self, file_path, compression=zipfile.ZIP_DEFLATED, validate=True):
        assert not os.path.exists(file_path)

        if validate:
            self.validate()

        with ZipFile(file_path, mode="w", compression=compression) as zip_file:
            dome_file = StringIO()
            self.agencies.save(dome_file)
            zip_file.writestr("agency.txt", dome_file.getvalue())
            dome_file.close()

            dome_file = StringIO()
            self.routes.save(dome_file)
            zip_file.writestr("routes.txt", dome_file.getvalue())
            dome_file.close()

            dome_file = StringIO()
            self.shapes.save(dome_file)
            zip_file.writestr("shapes.txt", dome_file.getvalue())
            dome_file.close()

            dome_file = StringIO()
            self.calendar.save(dome_file)
            zip_file.writestr("calendar.txt", dome_file.getvalue())
            dome_file.close()

            dome_file = StringIO()
            self.trips.save(dome_file)
            zip_file.writestr("trips.txt", dome_file.getvalue())
            dome_file.close()

            dome_file = StringIO()
            self.stops.save(dome_file)
            zip_file.writestr("stops.txt", dome_file.getvalue())
            dome_file.close()

            fields = []
            for trip in self.trips:
                for stop_time in trip.stop_times:
                    fields += (field for field in stop_time.get_csv_fields() if field not in fields)
            dome_file = StringIO()
            writer = csv.DictWriter(dome_file, fieldnames=fields, restval=None)
            writer.writeheader()
            for trip in self.trips:
                for stop_time in trip.stop_times:
                    writer.writerow(stop_time.to_csv_line())
            zip_file.writestr("stop_times.txt", dome_file.getvalue())
            dome_file.close()

            for file_name, file_data in self.unknown_files.iteritems():
                zip_file.writestr(file_name, file_data.data)

    def add_agency(self, **kwargs):
        self.agencies.add_agency(**kwargs)

    def add_agency_object(self, agency, recursive=False):
        assert isinstance(agency, Agency)

        if agency.agency_id not in self.agencies:
            self.agencies.add_agency(**agency.to_csv_line())
        else:
            assert agency == self.agencies[agency.agency_id]

    def add_route(self, **kwargs):
        self.routes.add_route(**kwargs)

    def add_route_object(self, route, recursive=False):
        assert isinstance(route, Route)

        if route.route_id not in self.routes:
            if recursive:
                self.add_agency_object(route.agency, recursive=True)
            else:
                assert route.agency.agency_id in self.agencies and route.agency == self.agencies[route.agency.agency_id]
            self.routes.add_route(**route.to_csv_line())
        else:
            assert route == self.routes[route.route_id]

    def add_shape_point(self, **kwargs):
        self.shapes.add_shape_point(**kwargs)

    def add_shape_object(self, shape, recursive=False):
        assert isinstance(shape, Shape)

        if shape.shape_id not in self.shapes:
            for row in shape.to_csv_line():
                self.shapes.add_shape_point(**row)
        else:
            assert shape == self.shapes[shape.shape_id]

    def add_service(self, **kwargs):
        self.calendar.add_service(**kwargs)

    def add_service_object(self, service, recursive=False):
        assert isinstance(service, Service)

        if service.service_id not in self.calendar:
            self.calendar.add_service(**service.to_csv_line())
        else:
            assert service == self.calendar[service.service_id]

    def add_trip(self, **kwargs):
        self.trips.add_trip(**kwargs)

    def add_trip_object(self, trip, recursive=False):
        assert isinstance(trip, Trip)

        if trip.trip_id not in self.trips:
            if recursive:
                self.add_route_object(trip.route, recursive=True)
                self.add_service_object(trip.service, recursive=True)
                self.add_shape_object(trip.shape, recursive=True)
            else:
                assert trip.route.route_id in self.routes and trip.route == self.routes[trip.route.route_id]
                assert trip.service.service_id in self.calendar and trip.service == self.calendar[trip.service.service_id]
                assert trip.shape.shape_id in self.shapes and trip.shape == self.shapes[trip.shape.shape_id]
            self.trips.add_trip(**trip.to_csv_line())
        else:
            assert trip == self.trips[trip.trip_id]

    def add_stop(self, **kwargs):
        self.stops.add_stop(**kwargs)

    def add_stop_object(self, stop, recursive=False):
        assert isinstance(stop, Stop)

        if stop.stop_id not in self.stops:
            if stop.parent_station is not None:
                if recursive:
                    # TODO: add when we are changing stop.parent_station to be a Stop object
                    # self.add_stop_object(stop.parent_station, recursive=True)
                    pass
                else:
                    assert stop.parent_station in self.stops
                    # TODO: change to this condition when we are changing stop.parent_station to be a Stop object
                    # assert stop.parent_station.stop_id in self.stops and stop.parent_station == self.stops[stop.parent_station.stop_id]
            self.stops.add_stop(**stop.to_csv_line())
        else:
            assert stop == self.stops[stop.stop_id]

    def add_stop_time(self, **kwargs):
        stop_time = StopTime(transit_data=self, **kwargs)

        assert stop_time.stop_sequence not in (st.stop_sequence for st in stop_time.trip.stop_times)
        self._changed()
        stop_time.trip.stop_times.add(stop_time)
        stop_time.stop.stop_times.append(stop_time)
        return stop_time

    def add_stop_time_object(self, stop_time, recursive=False):
        assert isinstance(stop_time, StopTime)

        if recursive:
            self.add_trip_object(stop_time.trip, recursive=True)
            self.add_stop_object(stop_time.stop, recursive=True)
        else:
            assert stop_time.trip.trip_id in self.trips and stop_time.trip == self.trips[stop_time.trip.trip_id]
            assert stop_time.stop.stop_id in self.stops and stop_time.stop == self.stops[stop_time.stop.stop_id]
        self.add_stop_time(**stop_time.to_csv_line())

    def clean(self):
        self.trips.clean()
        self.stops.clean()
        self.shapes.clean()
        self.calendar.clean()
        self.routes.clean()
        self.agencies.clean()

    def validate(self, force=False):
        if self.is_validated and not force:
            return

        self.agencies.validate()
        self.routes.validate()
        self.shapes.validate()
        self.calendar.validate()
        self.trips.validate()
        self.stops.validate()

        self.is_validated = True

    def __eq__(self, other):
        if not isinstance(other, TransitData):
            return False

        return self.agencies == other.agencies and self.routes == other.routes and self.trips == other.trips and \
               self.calendar == other.calendar and self.shapes == other.shapes and self.stops == other.stops
