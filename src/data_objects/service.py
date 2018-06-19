from datetime import datetime

from utils.parsing import parse_or_default, str_to_bool


class Service:
    def __init__(self, service_id, start_date, end_date, sunday=None, monday=None, tuesday=None, wednesday=None,
                 thursday=None, friday=None, saturday=None, **kwargs):
        """
        :type service_id: str | int
        :type start_date: datetime | str
        :type end_date: datetime | str
        :type sunday: str | bool | None
        :type monday: str | bool | None
        :type tuesday: str | bool | None
        :type wednesday: str | bool | None
        :type thursday: str | bool | None
        :type friday: str | bool | None
        :type saturday: str | bool | None
        """

        self.service_id = int(service_id)
        self.start_date = start_date if isinstance(start_date, datetime) else datetime.strptime(start_date, "%Y%m%d").date()
        self.end_date = end_date if isinstance(end_date, datetime) else datetime.strptime(end_date, "%Y%m%d").date()
        self.sunday = parse_or_default(sunday, False, str_to_bool)
        self.monday = parse_or_default(monday, False, str_to_bool)
        self.tuesday = parse_or_default(tuesday, False, str_to_bool)
        self.wednesday = parse_or_default(wednesday, False, str_to_bool)
        self.thursday = parse_or_default(thursday, False, str_to_bool)
        self.friday = parse_or_default(friday, False, str_to_bool)
        self.saturday = parse_or_default(saturday, False, str_to_bool)

        assert len(kwargs) == 0
