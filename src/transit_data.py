from zipfile import ZipFile

from data_objects import *


class TransitData:
    def __init__(self, gtfs_file=None):
        self.agencies = {}
        self.routes = {}
        self.shapes = {}
        self.calendar = {}
        self.trips = {}
        self.stops = {}

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
            reader = csv.DictReader(agency_file)
            self.agencies = AgencyCollection(self, agency_file)

        with zip_file.open("routes.txt", "r") as routes_file:
            self.routes = RouteCollection(self, routes_file)

        with zip_file.open("shapes.txt", "r") as shapes_file:
            self.shapes = ShapeCollection(self, shapes_file)

        with zip_file.open("calendar.txt", "r") as calendar_file:
            self.calendar = ServiceCollection(self, calendar_file)

        with zip_file.open("trips.txt", "r") as trips_file:
            self.trips = TripCollection(self, trips_file)

        with zip_file.open("stops.txt", "r") as stops_file:
            self.stops = StopCollection(self, stops_file)

        with zip_file.open("stop_times.txt", "r") as stop_times_file:
            reader = csv.DictReader(stop_times_file)
            for row in reader:
                stop_time = StopTime(transit_data=self, **row)
                stop_time.trip.stop_times.append(stop_time)
                stop_time.stop.stop_times.append(stop_time)

    def add_agency(self, **kwargs):
        agency = Agency(**kwargs)

        # TODO: merge this to code line to one function
        assert agency.agency_id not in self.agencies
        self._changed()
        self.agencies[agency.agency_id] = agency
        return agency

    def add_route(self, **kwargs):
        route = Route(transit_data=self, **kwargs)

        assert route.route_id not in self.routes
        self._changed()
        self.routes[route.route_id] = route
        return route

    def add_shape(self, **kwargs):
        shape = Shape(**kwargs)

        assert shape.shape_id not in self.shapes
        self._changed()
        self.shapes[shape.shape_id] = shape
        return shape

    def add_service(self, **kwargs):
        service = Service(**kwargs)

        assert service.service_id not in self.calendar
        self._changed()
        self.calendar[service.service_id] = service
        return service

    def add_trip(self, **kwargs):
        trip = Trip(transit_data=self, **kwargs)

        assert trip.trip_id not in self.trips
        self._changed()
        self.trips[trip.trip_id] = trip
        trip.route.trips.append(trip)
        return trip

    def add_stop(self, **kwargs):
        stop = Stop(transit_data=self, **kwargs)

        assert stop.stop_id not in self.stops
        self._changed()
        self.stops[stop.stop_id] = stop
        return stop

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
