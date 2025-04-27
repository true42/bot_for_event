from datetime import datetime, timedelta


def last_day_of_month(any_day):
    # The day 28 exists in every month. 4 days later, it's always next month
    next_month = any_day.replace(day=28) + timedelta(days=4)
    # subtracting the number of the current day brings us back one month
    return_date = next_month - timedelta(days=next_month.day)
    return return_date.day


if __name__ == '__main__':
    now = datetime.now()
    print(last_day_of_month(now))
