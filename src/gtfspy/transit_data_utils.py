from gtfspy.transit_data_object import TransitData


def clone_transit_data(transit_data):
    """
    :rtype: TransitData
    :type transit_data: TransitData
    """

    new_transit_data = TransitData()
    for service in transit_data.calendar:
        new_transit_data.add_service_object(service, recursive=False)
    for shape in transit_data.shapes:
        new_transit_data.add_shape_object(shape)
    for stop in transit_data.stops:
        new_transit_data.add_stop_object(stop, recursive=False)
    for agency in transit_data.agencies:
        new_transit_data.add_agency_object(agency, recursive=False)
    for route in transit_data.routes:
        new_transit_data.add_route_object(route, recursive=False)
    for trip in transit_data.trips:
        new_transit_data.add_trip_object(trip, recursive=False)
        for stop_time in trip.stop_times:
            new_transit_data.add_stop_time_object(stop_time, recursive=False)

    return new_transit_data


def create_partial_transit_data(transit_data, lines):
    """
    :rtype: TransitData
    :type transit_data: TransitData
    :type lines: dict[int, list[str]]
    """

    new_transit_data = TransitData()

    for agency_id, line_numbers in lines.iteritems():
        for line in transit_data.agencies[agency_id].lines:
            if line.line_number in line_numbers:
                for route in line.routes.itervalues():
                    for trip in route.trips:
                        for stop_time in trip.stop_times:
                            new_transit_data.add_stop_time_object(stop_time, recursive=True)

    return new_transit_data
