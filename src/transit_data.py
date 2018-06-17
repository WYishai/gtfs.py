import csv
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
            self.agencies = {agency.agency_id: agency for agency in (Agency(**row) for row in reader)}

        with zip_file.open("routes.txt", "r") as routes_file:
            reader = csv.DictReader(routes_file)
            self.routes = {route.route_id: route for route in
                           (Route(transit_data=self, **row) for row in reader)}

        with zip_file.open("shapes.txt", "r") as shapes_file:
            reader = csv.DictReader(shapes_file)
            self.shapes = {shape.shape_id: shape for shape in
                           (Shape(**row) for row in reader)}

        with zip_file.open("calendar.txt", "r") as calendar_file:
            reader = csv.DictReader(calendar_file)
            self.calendar = {service.service_id: service for service in
                             (Service(**row) for row in reader)}

        with zip_file.open("trips.txt", "r") as trips_file:
            reader = csv.DictReader(trips_file)
            self.trips = {trip.trip_id: trip for trip in
                          (Trip(transit_data=self, **row) for row in reader)}
        for trip in self.trips.itervalues():
            trip.route.trips.append(trip)

        with zip_file.open("stops.txt", "r") as stops_file:
            reader = csv.DictReader(stops_file)
            self.stops = {stop.stop_id: stop for stop in
                          (Stop(transit_data=self, **row) for row in reader)}

        with zip_file.open("stop_times.txt", "r") as stop_times_file:
            reader = csv.DictReader(stop_times_file)
            for row in reader:
                stop_time = StopTime(transit_data=self, **row)
                stop_time.trip.stop_times.append(stop_time)
                stop_time.stop.stop_times.append(stop_time)

    def add_agency(self, agency_id, agency_name, agency_url, agency_timezone, agency_lang, agency_phone,
                   agency_fare_url, **kwargs):
        agency = Agency(agency_id=agency_id, agency_name=agency_name, agency_url=agency_url,
                        agency_timezone=agency_timezone, agency_lang=agency_lang, agency_phone=agency_phone,
                        agency_fare_url=agency_fare_url, **kwargs)

        # TODO: merge this to code line to one function
        assert agency.agency_id not in self.agencies
        self._changed()
        self.agencies[agency.agency_id] = agency
        return agency

    def add_route(self, route_id, route_long_name, route_type, agency_id, route_color, route_desc, route_short_name,
                  **kwargs):
        route = Route(transit_data=self, route_id=route_id, route_long_name=route_long_name, route_type=route_type,
                      agency_id=agency_id, route_color=route_color, route_desc=route_desc,
                      route_short_name=route_short_name, **kwargs)

        assert route.route_id not in self.routes
        self._changed()
        self.routes[route.route_id] = route
        return route

    def add_shape(self, shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence, shape_dist_traveled=None, **kwargs):
        shape = Shape(shape_id=shape_id, shape_pt_lat=shape_pt_lat, shape_pt_lon=shape_pt_lon,
                      shape_pt_sequence=shape_pt_sequence, shape_dist_traveled=shape_dist_traveled, **kwargs)

        assert shape.shape_id not in self.shapes
        self._changed()
        self.shapes[shape.shape_id] = shape
        return shape

    def add_service(self, service_id, sunday, monday, tuesday, wednesday, thursday, friday, saturday, start_date,
                    end_date, **kwargs):
        service = Service(service_id=service_id, sunday=sunday, monday=monday, tuesday=tuesday, wednesday=wednesday,
                          thursday=thursday, friday=friday, saturday=saturday, start_date=start_date, end_date=end_date,
                          **kwargs)

        assert service.service_id not in self.calendar
        self._changed()
        self.calendar[service.service_id] = service
        return service

    def add_trip(self, trip_id, route_id, service_id, trip_headsign, direction_id, shape_id, **kwargs):
        trip = Trip(trip_id=trip_id, route_id=route_id, service_id=service_id, trip_headsign=trip_headsign,
                    direction_id=direction_id, shape_id=shape_id, **kwargs)

        assert trip.trip_id not in self.trips
        self._changed()
        self.trips[trip.trip_id] = trip
        trip.route.trips.append(trip)
        return trip

    def add_stop(self, stop_id, stop_code, stop_name, stop_desc, stop_lat, stop_lon, location_type, parent_station,
                 zone_id, **kwargs):
        stop = Stop(transit_data=self, stop_id=stop_id, stop_code=stop_code, stop_name=stop_name, stop_desc=stop_desc,
                    stop_lat=stop_lat, stop_lon=stop_lon, location_type=location_type, parent_station=parent_station,
                    zone_id=zone_id, **kwargs)

        assert stop.stop_id not in self.stops
        self._changed()
        self.stops[stop.stop_id] = stop
        return stop

    def add_stop_time(self, trip_id, arrival_time, departure_time, stop_id, stop_sequence, pickup_type, drop_off_type,
                      shape_dist_traveled, stop_headsign=None, timepoint=None, **kwargs):
        stop_time = StopTime(transit_data=self, trip_id=trip_id, arrival_time=arrival_time,
                             departure_time=departure_time, stop_id=stop_id, stop_sequence=stop_sequence,
                             pickup_type=pickup_type, drop_off_type=drop_off_type,
                             shape_dist_traveled=shape_dist_traveled, stop_headsign=stop_headsign, timepoint=timepoint,
                             **kwargs)

        assert stop_time.stop_sequence not in (st.stop_sequence for st in stop_time.trip.stop_times)
        self._changed()
        stop_time.trip.stop_times.append(stop_time)
        stop_time.stop.stop_times.append(stop_time)
        return stop_time

    def verify(self):
        pass

        self.is_verified = True
