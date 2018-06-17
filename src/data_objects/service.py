from datetime import datetime


class Service:
    def __init__(self, service_id, sunday, monday, tuesday, wednesday, thursday, friday, saturday, start_date, end_date,
                 **kwargs):
        self.service_id = service_id
        self.sunday = bool(int(sunday))
        self.monday = bool(int(monday))
        self.tuesday = bool(int(tuesday))
        self.wednesday = bool(int(wednesday))
        self.thursday = bool(int(thursday))
        self.friday = bool(int(friday))
        self.saturday = bool(int(saturday))
        self.start_date = start_date if isinstance(start_date, datetime) else datetime.strptime(start_date, "%Y%m%d").date()
        self.end_date = end_date if isinstance(end_date, datetime) else datetime.strptime(end_date, "%Y%m%d").date()

        assert len(kwargs) == 0
