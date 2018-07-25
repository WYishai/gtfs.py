import os
import shutil
import tempfile
import zipfile
from zipfile import ZipFile

from gtfspy.data_objects import *


class TransitData(object):
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
                    self.agencies._load_file(agency_file, filter=lambda agency: agency.id in partial)

            with zip_file.open("routes.txt", "r") as routes_file:
                if partial is None:
                    self.routes._load_file(routes_file)
                else:
                    self.routes._load_file(routes_file,
                                           ignore_errors=True,
                                           filter=lambda route: partial[route.agency.id] is None or
                                                                route.line.line_number in partial[route.agency.id])
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
                                                   (fare_rule.origin_id is None or fare_rule.origin_id in zone_ids) and
                                                   (fare_rule.destination_id is None or fare_rule.destination_id in zone_ids) and
                                                   (fare_rule.contains_id is None or fare_rule.contains_id in zone_ids))

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
                with open(os.path.join(tempdir, file_name), "wb") as f:
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
        return self.agencies.add(**kwargs)

    def add_agency_object(self, agency, recursive=False):
        return self.agencies.add_object(agency, recursive=recursive)

    def add_route(self, **kwargs):
        return self.routes.add(**kwargs)

    def add_route_object(self, route, recursive=False):
        return self.routes.add_object(route, recursive=recursive)

    def add_shape_point(self, **kwargs):
        return self.shapes.add(**kwargs)

    def add_shape_object(self, shape, recursive=False):
        return self.shapes.add_object(shape, recursive=recursive)

    def add_service(self, **kwargs):
        return self.calendar.add(**kwargs)

    def add_service_object(self, service, recursive=False):
        return self.calendar.add_object(service, recursive=recursive)

    def add_trip(self, **kwargs):
        return self.trips.add(**kwargs)

    def add_trip_object(self, trip, recursive=False):
        return self.trips.add_object(trip, recursive=recursive)

    def add_stop(self, **kwargs):
        return self.stops.add(**kwargs)

    def add_stop_object(self, stop, recursive=False):
        return self.stops.add_object(stop, recursive=recursive)

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
            assert stop_time.trip in self.trips
            assert stop_time.stop in self.stops
        return self.add_stop_time(**stop_time.to_csv_line())

    def add_fare_attribute(self, **kwargs):
        return self.fare_attributes.add(**kwargs)

    def add_fare_attribute_object(self, fare_attribute, recursive=False):
        return self.fare_attributes.add_object(fare_attribute, recursive=recursive)

    def add_fare_rule(self, **kwargs):
        return self.fare_rules.add(**kwargs)

    def add_fare_rule_object(self, fare_rule, recursive=False):
        return self.fare_rules.add_object(fare_rule, recursive=recursive)

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
                if len(trip.stop_times) != len(other.trips[trip.id].stop_times):
                    return False
                for self_stop_time, other_stop_time in zip(trip.stop_times, other.trips[trip.id].stop_times):
                    if self_stop_time != other_stop_time:
                        return False

            return True

        return False

    def __ne__(self, other):
        return not (self == other)
