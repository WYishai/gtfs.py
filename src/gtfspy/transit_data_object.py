import os
import shutil
import tempfile
import zipfile
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
        self.translator = Translator()
        self.fare_attributes = FareAttributeCollection(self)
        self.fare_rules = FareRuleCollection(self)

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

    def load_gtfs_file(self, gtfs_file, validate=True, partial=None):
        assert not self.has_changed

        with ZipFile(gtfs_file) as zip_file:
            zip_files_list = zip_file.namelist()

            with zip_file.open("agency.txt", "r") as agency_file:
                if partial is None:
                    self.agencies._load_file(agency_file)
                else:
                    self.agencies._load_file(agency_file, filter=lambda agency: agency.agency_id in partial)

            with zip_file.open("routes.txt", "r") as routes_file:
                if partial is None:
                    self.routes._load_file(routes_file)
                else:
                    self.routes._load_file(routes_file,
                                           ignore_errors=True,
                                           filter=lambda route: route.line.line_number in partial[route.agency.agency_id])
                    for agency in self.agencies:
                        agency.lines.clean()

            with zip_file.open("shapes.txt", "r") as shapes_file:
                self.shapes._load_file(shapes_file, ignore_errors=partial is not None)

            with zip_file.open("calendar.txt", "r") as calendar_file:
                self.calendar._load_file(calendar_file, ignore_errors=partial is not None)

            with zip_file.open("trips.txt", "r") as trips_file:
                self.trips._load_file(trips_file, ignore_errors=partial is not None)
                if partial is not None:
                    self.shapes.clean()
                    self.calendar.clean()

            with zip_file.open("stops.txt", "r") as stops_file:
                self.stops._load_file(stops_file, ignore_errors=partial is not None)

            with zip_file.open("stop_times.txt", "r") as stop_times_file:
                reader = csv.DictReader(stop_times_file)
                for row in reader:
                    try:
                        stop_time = StopTime(transit_data=self, **row)
                        stop_time.trip.stop_times.add(stop_time)
                        stop_time.stop.stop_times.append(stop_time)
                    except:
                        if partial is None:
                            raise

                if partial is not None:
                    self.stops.clean()

            if "translations.txt" in zip_files_list:
                with zip_file.open("translations.txt", "r") as translation_file:
                    self.translator._load_file(translation_file)

            if "fare_attributes.txt" in zip_files_list and "fare_rules.txt" in zip_files_list:
                with zip_file.open("fare_attributes.txt", "r") as fare_attributes_file:
                    self.fare_attributes._load_file(fare_attributes_file, ignore_errors=partial is not None)
                with zip_file.open("fare_rules.txt", "r") as fare_rules_file:
                    if partial is None:
                        self.fare_rules._load_file(fare_rules_file)
                    else:
                        zone_ids = {stop.zone_id for stop in self.stops}
                        self.fare_rules._load_file(fare_rules_file,
                                                   ignore_errors=True,
                                                   filter=lambda fare_rule:
                                                   fare_rule.origin_id is None or fare_rule.origin_id in zone_ids or
                                                   fare_rule.destination_id is None or fare_rule.destination_id in zone_ids or
                                                   fare_rule.contains_id is None or fare_rule.contains_id in zone_ids)

                if partial is not None:
                    self.fare_attributes.clean()
            else:
                assert "fare_attributes.txt" in zip_files_list
                assert "fare_rules.txt" in zip_files_list

            for inner_file in zip_file.filelist:
                # TODO: collect this known files list on reading
                if inner_file.filename not in ["agency.txt", "routes.txt", "shapes.txt", "calendar.txt", "trips.txt",
                                               "stops.txt", "stop_times.txt", "translations.txt", "fare_attributes.txt",
                                               "fare_rules.txt"]:
                    with zip_file.open(inner_file, "r") as f:
                        self.unknown_files[inner_file.filename] = UnknownFile(f)

        if validate:
            self.validate()

    def save(self, file_path, compression=zipfile.ZIP_DEFLATED, validate=True):
        if validate:
            self.validate()

        tempdir = tempfile.mkdtemp()
        temp_gtfs_file_path = tempfile.mktemp(suffix=".zip")

        try:
            with open(os.path.join(tempdir, "agency.txt"), "wb") as f:
                self.agencies.save(f)

            with open(os.path.join(tempdir, "routes.txt"), "wb") as f:
                self.routes.save(f)

            with open(os.path.join(tempdir, "shapes.txt"), "wb") as f:
                self.shapes.save(f)

            with open(os.path.join(tempdir, "calendar.txt"), "wb") as f:
                self.calendar.save(f)

            with open(os.path.join(tempdir, "trips.txt"), "wb") as f:
                self.trips.save(f)

            with open(os.path.join(tempdir, "stops.txt"), "wb") as f:
                self.stops.save(f)

            fields = []
            for trip in self.trips:
                for stop_time in trip.stop_times:
                    fields += (field for field in stop_time.get_csv_fields() if field not in fields)
            with open(os.path.join(tempdir, "stop_times.txt"), "wb") as f:
                writer = csv.DictWriter(f, fieldnames=fields, restval=None)
                writer.writeheader()
                for trip in self.trips:
                    for stop_time in trip.stop_times:
                        writer.writerow(stop_time.to_csv_line())

            if self.translator.has_data():
                with open(os.path.join(tempdir, "translations.txt"), "wb") as f:
                    self.translator.save(f)

            if self.fare_rules.has_data():
                with open(os.path.join(tempdir, "fare_attributes.txt"), "wb") as f:
                    self.fare_attributes.save(f)

                with open(os.path.join(tempdir, "fare_rules.txt"), "wb") as f:
                    self.fare_rules.save(f)

            for file_name, file_data in self.unknown_files.iteritems():
                with open(os.path.join(tempdir, file_name)) as f:
                    f.write(file_data.data)

            with ZipFile(temp_gtfs_file_path, mode="w", compression=compression) as zip_file:
                for file_name in os.listdir(tempdir):
                    zip_file.write(os.path.join(tempdir, file_name), arcname=file_name)
            shutil.move(temp_gtfs_file_path, file_path)
        finally:
            if os.path.exists(tempdir) and os.path.isdir(tempdir):
                shutil.rmtree(tempdir)
            if os.path.exists(temp_gtfs_file_path) and not os.path.isdir(temp_gtfs_file_path):
                os.remove(temp_gtfs_file_path)

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

    def add_fare_attribute(self, **kwargs):
        self.fare_attributes.add_fare_attribute(**kwargs)

    def add_fare_attribute_object(self, fare_attribute, recursive=False):
        assert isinstance(fare_attribute, FareAttribute)

        if fare_attribute.fare_id not in self.fare_attributes:
            self.fare_attributes.add_fare_attribute(**fare_attribute.to_csv_line())
        else:
            assert fare_attribute == self.fare_attributes[fare_attribute.fare_id]

    def add_fare_rule(self, **kwargs):
        self.fare_rules.add_fare_rule(**kwargs)

    def add_fare_rule_object(self, fare_rule, recursive=False):
        assert isinstance(fare_rule, FareRule)

        if recursive:
            self.add_fare_attribute_object(fare_rule.fare, recursive=True)
        else:
            assert fare_rule.fare.fare_id in self.fare_attributes \
                   and fare_rule.fare == self.fare_attributes[fare_rule.fare.fare_id]
        self.fare_rules.add_fare_rule(**fare_rule.to_csv_line())

    def clean(self):
        self.trips.clean()
        self.stops.clean()
        self.shapes.clean()
        self.calendar.clean()
        self.routes.clean()
        self.agencies.clean()
        self.fare_rules.clean()
        self.fare_attributes.clean()

    def validate(self, force=False):
        if self.is_validated and not force:
            return

        self.agencies.validate()
        self.routes.validate()
        self.shapes.validate()
        self.calendar.validate()
        self.trips.validate()
        self.stops.validate()
        self.fare_attributes.validate()
        self.fare_rules.validate()

        self.is_validated = True

    def __eq__(self, other):
        if not isinstance(other, TransitData):
            return False

        if self.agencies == other.agencies and self.routes == other.routes and self.trips == other.trips and \
                self.calendar == other.calendar and self.shapes == other.shapes and self.stops == other.stops and \
                self.fare_attributes == other.fare_attributes and self.fare_rules == other.fare_rules:
            for trip in self.trips:
                if len(trip.stop_times) != len(other.trips[trip.trip_id].stop_times):
                    return False
                for self_stop_time, other_stop_time in zip(trip.stop_times, other.trips[trip.trip_id].stop_times):
                    if self_stop_time != other_stop_time:
                        return False

            return True

        return False

    def __ne__(self, other):
        return not (self == other)
