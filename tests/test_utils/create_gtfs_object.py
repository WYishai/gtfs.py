import csv
from cStringIO import StringIO
from datetime import date, timedelta

from gtfspy import TransitData
from gtfspy.data_objects import UnknownFile


def create_full_transit_data():
    td = TransitData()

    td.add_stop(stop_id=10000, stop_name="Jerusalem Central Station", stop_lat=31.789467, stop_lon=35.203715,
                stop_code="10000", stop_desc="Jerusalem Central Station", zone_id=1, location_type=1,
                stop_timezone="Asia/Jerusalem", test_attribute="stop test data")
    td.add_stop(stop_id=10001, stop_name="Platform 1", stop_lat=31.789467, stop_lon=35.203715,
                stop_code="10001", stop_desc="Jerusalem Central Station, Platform 1", zone_id=1, location_type=0,
                parent_station=10000, wheelchair_boarding=True, stop_url="http://stop.com/")
    td.add_stop(stop_id=20000, stop_name="Tel Aviv Central Station", stop_lat=32.055818, stop_lon=34.779427,
                stop_code="20000", stop_desc="Tel Aviv Central Station", zone_id=2, wheelchair_boarding=1)
    td.add_stop(stop_id=30000, stop_name="Netania Central Station", stop_lat=32.326889, stop_lon=34.858740,
                stop_code="30000", stop_desc="Netania Central Station", zone_id=3, wheelchair_boarding=False)

    td.add_shape_point(shape_id=1, shape_pt_lat=td.stops[10001].stop_lat, shape_pt_lon=td.stops[10001].stop_lon,
                       shape_pt_sequence=0, shape_dist_traveled=0)
    td.add_shape_point(shape_id=1, shape_pt_lat=td.stops[20000].stop_lat, shape_pt_lon=td.stops[20000].stop_lon,
                       shape_pt_sequence=1, shape_dist_traveled=None, test_attribute="shape test data")
    td.add_shape_point(shape_id=2, shape_pt_lat=td.stops[20000].stop_lat, shape_pt_lon=td.stops[20000].stop_lon,
                       shape_pt_sequence=0)
    td.add_shape_point(shape_id=2, shape_pt_lat=td.stops[10001].stop_lat, shape_pt_lon=td.stops[10001].stop_lon,
                       shape_pt_sequence=1)

    td.add_service(service_id=1, start_date=date.today(), end_date=date.today() + timedelta(weeks=8), sunday=True,
                   monday=True, tuesday=True, wednesday=True, thursday=True)
    td.add_service(service_id=2, start_date=date.today(), end_date=date.today() + timedelta(weeks=8), sunday=True,
                   monday=True, tuesday=True, wednesday=True, thursday=True, friday=True)
    td.add_service(service_id=3, start_date=date.today(), end_date=date.today() + timedelta(weeks=8), friday=True)
    td.add_service(service_id=4, start_date=date.today(), end_date=date.today() + timedelta(weeks=8), saturday=True)
    td.add_service(service_id=5, start_date=date.today(), end_date=date.today() + timedelta(weeks=8), sunday=True,
                   monday=False, tuesday=False, wednesday=False, thursday=False, friday=False, saturday=False,
                   test_attribute="service test data")

    td.add_agency(agency_id=1, agency_name="agency name 1", agency_url="http://www.agencyname1.com/",
                  agency_timezone="Asia/Jerusalem", agency_lang="HE", agency_phone="+972-2-1234567",
                  agency_email="agencyname1@host.com", agency_fare_url="http://www.agencyname1.com/fare",
                  test_attribute="test data 1")
    td.add_agency(agency_id=30, agency_name="agency name 30", agency_url="https://www.agencyname30.com/",
                  agency_timezone="Asia/Jerusalem", agency_phone="*1234", agency_email="mail@agencyname30.com",
                  agency_fare_url="https://www.agencyname30.com/fare")

    td.add_route(route_id="1001", route_short_name="1", route_long_name="route 1001 long name", route_type=3,
                 agency_id=1, route_desc=None, route_color=None, route_text_color=None, bikes_allowed=True)
    td.add_route(route_id="1002", route_short_name="2", route_long_name="route 1002 long name", route_type=3,
                 agency_id=1, route_desc=None, route_color=None, route_text_color=None, bikes_allowed=True)
    td.add_route(route_id="1003", route_short_name="3", route_long_name="route 1003 long name", route_type=3,
                 agency_id=1, route_desc=None, route_color=None, route_text_color=None, bikes_allowed=False)
    td.add_route(route_id="30001", route_short_name="301", route_long_name="route 30001 long name", route_type=2,
                 agency_id=30, route_desc="Rail!", route_color=None, route_text_color=None, bikes_allowed=None,
                 test_attribute="test data 30001")

    td.add_trip(trip_id="1001_1", route_id="1001", service_id=2, shape_id=1, bikes_allowed=False)
    td.add_trip(trip_id="1001_2", route_id="1001", service_id=1, shape_id=2, bikes_allowed=None)
    td.add_trip(trip_id="1002_1", route_id="1002", service_id=1)
    td.add_trip(trip_id="1002_2", route_id="1002", service_id=3)
    td.add_trip(trip_id="1002_3", route_id="1002", service_id=4)
    td.add_trip(trip_id="1002_4", route_id="1002", service_id=5)
    td.add_trip(trip_id="1003_1", route_id="1003", service_id=1, wheelchair_accessible=False)
    td.add_trip(trip_id="30001_1", route_id="30001", service_id=2, trip_headsign="trip headsign",
                trip_short_name="trip 30001_1 short name", direction_id=1, block_id=1, bikes_allowed=True,
                wheelchair_accessible=True, original_trip_id="30001_1 origin", test_attribute="trip test data")

    td.add_stop_time(trip_id="1001_1", arrival_time=timedelta(hours=6), departure_time=timedelta(hours=6, minutes=5),
                     stop_id=10001, stop_sequence=0, drop_off_type=1, shape_dist_traveled=0)
    td.add_stop_time(trip_id="1001_1", arrival_time=timedelta(hours=7), departure_time=timedelta(hours=7),
                     stop_id=20000, stop_sequence=1, pickup_type=1, shape_dist_traveled=65.0)
    td.add_stop_time(trip_id="1001_2", arrival_time=timedelta(hours=12), departure_time=timedelta(hours=12),
                     stop_id=10001, stop_sequence=0, drop_off_type=1, shape_dist_traveled=0)
    td.add_stop_time(trip_id="1001_2", arrival_time=timedelta(hours=13), departure_time=timedelta(hours=13),
                     stop_id=20000, stop_sequence=1, pickup_type=1, shape_dist_traveled=65.0)
    td.add_stop_time(trip_id="1002_1", arrival_time=timedelta(hours=6), departure_time=timedelta(hours=6, minutes=5),
                     stop_id=20000, stop_sequence=0, drop_off_type=1)
    td.add_stop_time(trip_id="1002_1", arrival_time=timedelta(hours=7), departure_time=timedelta(hours=7),
                     stop_id=10001, stop_sequence=1, pickup_type=1)
    td.add_stop_time(trip_id="1002_2", arrival_time=timedelta(hours=12), departure_time=timedelta(hours=12, minutes=5),
                     stop_id=20000, stop_sequence=0, drop_off_type=1)
    td.add_stop_time(trip_id="1002_2", arrival_time=timedelta(hours=13), departure_time=timedelta(hours=13),
                     stop_id=10001, stop_sequence=1, pickup_type=1)
    td.add_stop_time(trip_id="1002_3", arrival_time=timedelta(hours=23, minutes=30),
                     departure_time=timedelta(hours=23, minutes=35), stop_id=20000, stop_sequence=0, drop_off_type=1)
    td.add_stop_time(trip_id="1002_3", arrival_time=timedelta(hours=25, minutes=1),
                     departure_time=timedelta(hours=25, minutes=1), stop_id=10001, stop_sequence=1, pickup_type=1)
    td.add_stop_time(trip_id="1002_4", arrival_time=timedelta(hours=8), departure_time=timedelta(hours=8, minutes=5),
                     stop_id=20000, stop_sequence=0, drop_off_type=1)
    td.add_stop_time(trip_id="1002_4", arrival_time=timedelta(hours=9), departure_time=timedelta(hours=9),
                     stop_id=10001, stop_sequence=1, pickup_type=1)
    td.add_stop_time(trip_id="1003_1", arrival_time=timedelta(hours=23), departure_time=timedelta(hours=23, minutes=5),
                     stop_id=10001, stop_sequence=0, drop_off_type=1)
    td.add_stop_time(trip_id="1003_1", arrival_time=timedelta(hours=24), departure_time=timedelta(hours=24),
                     stop_id=20000, stop_sequence=1)
    td.add_stop_time(trip_id="1003_1", arrival_time=timedelta(hours=25, minutes=13),
                     departure_time=timedelta(hours=25, minutes=13), stop_id=30000, stop_sequence=2, pickup_type=1)
    td.add_stop_time(trip_id="30001_1", arrival_time=timedelta(hours=11, minutes=30),
                     departure_time=timedelta(hours=11, minutes=30), stop_id=20000, stop_sequence=0, drop_off_type=1,
                     stop_headsign="Tel Aviv Central Station headsign", timepoint=1,
                     test_attribute="stop time test data 1")
    td.add_stop_time(trip_id="30001_1", arrival_time=timedelta(hours=12, minutes=20),
                     departure_time=timedelta(hours=12, minutes=20), stop_id=30000, stop_sequence=1, pickup_type=1,
                     stop_headsign="Netania Central Station headsign", timepoint=0,
                     test_attribute="stop time test data 2")

    td.add_fare_attribute(fare_id="1", price=10, currency_type="ILS", payment_method=0, transfers=0)
    td.add_fare_attribute(fare_id="2", price=12.2, currency_type="ILS", payment_method=0, transfers=0)
    td.add_fare_attribute(fare_id="3", price=16.85, currency_type="ILS", payment_method=1, transfers=0, agency_id=30,
                          transfer_duration=1, test_attribute="fare attribute test data")

    td.add_fare_rule(fare_id="3", route_id="30001")
    td.add_fare_rule(fare_id="1", origin_id=1, destination_id=2)
    td.add_fare_rule(fare_id="1", origin_id=2, destination_id=1)
    td.add_fare_rule(fare_id="1", route_id="1003", contains_id=3)
    td.add_fare_rule(fare_id="2", route_id="1003", test_attribute="fare rule test data")

    td.translator.add_translate("EN", "hello", "hello")
    td.translator.add_translate("IT", "hello", "ciao")
    td.translator.add_translate("GR", "hello", "hallo")
    td.translator.add_translate("NE", "hello", "hallo")
    td.translator.add_translate("FR", "hello", "bonjour")
    td.translator.add_translate("EN", "bye", "bye")
    td.translator.add_translate("IT", "bye", "addio")
    td.translator.add_translate("NE", "bye", "doei")
    td.translator.add_translate("FR", "bye", "au revoir")
    td.translator.add_translate("EN", "test", "test")

    dome_file = StringIO()
    writer = csv.DictWriter(dome_file, ["key1", "key2"])
    writer.writeheader()
    writer.writerow({"key1": "value1_1", "key2": "value2_1"})
    writer.writerow({"key1": "value1_2", "key2": "value2_2"})
    dome_file.seek(0)
    td.unknown_files["unknown.txt"] = UnknownFile(dome_file)
    dome_file.close()

    return td
