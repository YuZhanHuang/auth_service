import calendar
import time
from datetime import timedelta, datetime
from typing import Union

from delorean import Delorean, parse

from project.constants import LOCAL_TZ
from project.validators import validate_datetime_str


def to_utc_with_start_time(date_str: str) -> datetime:
    return parse(f'{date_str} 00:00:00', timezone=LOCAL_TZ).naive


def to_utc_with_end_time(date_str: str) -> datetime:
    return parse(f'{date_str} 23:59:59.999999', timezone=LOCAL_TZ).naive


def to_local_with_specific_format(dt: datetime, format_: str = '%Y-%m-%d'):
    """
    from UTC to Local
    """
    local_datetime = Delorean(dt, 'UTC').shift(LOCAL_TZ).datetime.replace(tzinfo=None)

    return local_datetime.strftime(format_)


def first_day_of_year_utc():
    local_now = Delorean(datetime.utcnow(), 'UTC').shift(LOCAL_TZ).datetime
    first_day_of_year_local = datetime(local_now.year, 1, 1, 0, 0, 0)

    return Delorean(first_day_of_year_local, LOCAL_TZ).naive


def last_day_of_year_utc():
    local_now = Delorean(datetime.utcnow(), 'UTC').shift(LOCAL_TZ).datetime
    last_day_of_year_local = datetime(local_now.year, 12, 31, 23, 59, 59, 999999)

    return Delorean(last_day_of_year_local, LOCAL_TZ).naive


def get_milliseconds():
    return int(round(time.time() * 1000))


def working_days_period(current: Delorean = None, days: int = 0, naive: bool = False):
    today_start, today_end = working_today(current, naive)

    return today_start - timedelta(days=days), today_end - timedelta(days=days)


def parse_time(s: str, tz=LOCAL_TZ) -> Delorean:
    """
    處理時間字串，轉為 Delorean 時間物件
    :param s: 時間字串
    :param tz: 時區
    :return: Delorean
    """
    if validate_datetime_str(s):
        return parse(s, dayfirst=False, yearfirst=True, timezone=tz)


def working_today(current: Delorean = None, naive=False):
    """
    current: Delorean，請使用當地時間
    naive: boolean，是否有時區
    每天的收單時間為
    @台灣時間            @台灣時間
    昨日15:00:00    ~   今日14:59:59.999999
          |                  |
    ---------------------------------------->
    naive is True
    without timezone     without timezone
    昨天7:00:00     ~    今日6:59:59.999999

    naive is False
    @UTC                 @UTC
    昨天7:00:00     ~    今日6:59:59.999999
    """
    today = Delorean(timezone='Asia/Taipei') if current is None else current
    today_end = today.replace(hour=14, minute=59, second=59, microsecond=999999)
    today_start = (today - timedelta(days=1)).replace(hour=15, minute=0, second=0, microsecond=0)

    if naive:
        return today_start.naive, today_end.naive

    return today_start.shift('UTC').datetime, today_end.shift('UTC').datetime


def working_current_month(naive=False):
    now = Delorean(timezone='Asia/Taipei')
    _, last_day = calendar.monthrange(now.datetime.year, now.datetime.month)
    first_day = (now.replace(day=1) - timedelta(days=1)).replace(
        hour=15, minute=0, second=0, microsecond=0)
    end_day = now.replace(day=last_day,
                          hour=14, minute=59, second=59, microsecond=999999)

    if naive:
        return first_day.naive, end_day.naive

    return first_day.shift('UTC').datetime, end_day.shift('UTC').datetime


def working_specific_month(year=None, month=None, naive=False):
    if year is None or month is None:
        return working_current_month(naive=naive)

    first, last = calendar.monthrange(year, month)
    first_day_info = {'year': year, 'month': month, 'day': first,
                      'hour': 15, 'minute': 0, 'second': 0,
                      'microsecond': 0}
    last_day_info = {'year': year, 'month': month, 'day': last,
                     'hour': 14, 'minute': 59, 'second': 59,
                     'microsecond': 999999}

    first_day = Delorean(datetime=datetime(**first_day_info), timezone='Asia/Taipei')
    last_day = Delorean(datetime=datetime(**last_day_info), timezone='Asia/Taipei')

    if naive:
        return first_day.naive, last_day.naive

    return first_day.shift('UTC').datetime, last_day.shift('UTC').datetime


def days360(start_date: Union[str, datetime], end_date: Union[str, datetime]) -> Union[int, None]:
    """
    date string format 2021-11-28 or datetime object
    https://www.iotafinance.com/en/Date-Calculator.html
    可以到這裡進行驗算
    """
    if isinstance(start_date, str):
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
    elif isinstance(start_date, datetime):
        start = start_date
    else:
        return None

    if isinstance(end_date, str):
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    elif isinstance(end_date, datetime):
        end = end_date
    else:
        return None

    start_day, start_month, start_year = start.day, start.month, start.year
    end_day, end_month, end_year = end.day, end.month, end.year

    if (start_day == 31) or (start_month == 2
                             and (start_day == 29 or start_day == 28 and
                                  calendar.isleap(start.year))):
        start_day = 30

    if end_day == 31:
        if start_day != 30:
            end_day = 1

            if end_month == 12:
                end_year += 1
                end_month = 1
            else:
                end_month += 1
        else:
            end_day = 30

    return (end_day + end_month * 30 + end_year * 360) - (
            start_day + start_month * 30 + start_year * 360)


def get_current_day_naive(d: datetime = None):
    """
    取得今日時間
    LOCAL_TZ一日開始與結束時間 -> utc時區(naive)
    2023-01-08 12:30:30+08:00

    -> 2023-01-07 16:00:00 ~ 2023-01-07 15:59:59
    """
    utc_now = datetime.utcnow()
    local_start_of_day = Delorean(utc_now, 'UTC').shift(LOCAL_TZ).start_of_day
    local_end_of_day = Delorean(utc_now, 'UTC').shift(LOCAL_TZ).end_of_day
    utc_start_of_day = Delorean(local_start_of_day, LOCAL_TZ).shift('UTC').naive
    utc_end_of_day = Delorean(local_end_of_day, LOCAL_TZ).shift('UTC').naive

    return utc_start_of_day, utc_end_of_day
