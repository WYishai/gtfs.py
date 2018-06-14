class Service:
    def __init__(self, service_id, sunday, monday, tuesday, wednesday, thursday, friday, saturday, start_date, end_date,
                 **kwargs):
        self.service_id = service_id
        self.sunday = sunday
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.start_date = start_date
        self.end_date = end_date

        assert len(kwargs) == 0
