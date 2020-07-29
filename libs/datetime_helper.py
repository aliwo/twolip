from datetime import datetime, timedelta


class DateTimeHelper:

    @classmethod
    def date_korean(cls, date):
        return date.strftime("%Y{} %m{} %d{}").format('년', '월', '일')

    @classmethod
    def time_korean(cls, time):
        hour, minute, sec = str(time).split(':')
        ampm = "오전"
        if int(hour) > 12:
            hour = int(hour) - 12
            ampm = "오후"
        return "%s %s:%s" % (ampm, hour, minute)

    @classmethod
    def full_datetime(cls, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def now_strf(cls):
        datetime.now().strftime("%Y%m%d_%H%M%S")

    @classmethod
    def last_day_of_month(cls, date):
        '''
        특정 date 가 주어지면, date.month 의 말일을 구해줍니다.
        :param date:
        :return:
        '''
        next_month = date.replace(day=28) + timedelta(days=4)
        return next_month - timedelta(days=next_month.day)