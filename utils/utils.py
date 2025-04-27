from datetime import datetime, timedelta
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def last_day_of_month(any_day):
    # The day 28 exists in every month. 4 days later, it's always next month
    next_month = any_day.replace(day=28) + timedelta(days=4)
    # subtracting the number of the current day brings us back one month
    return_date = next_month - timedelta(days=next_month.day)
    return return_date.day


def generate_button(type_button, list_hour=None):
    if list_hour is None:
        list_hour = []
    if type_button == 'text':
        return generate_button_date()
    elif type_button == 'date':
        return generate_button_time(list_hour)
    else:
        return generate_button_time()


def generate_button_time(list_hour=None):
    hour_list = [[], [], [], [], [], []]
    max_len_row = 5
    index_hour = 0
    for hour in range(9, 33):
        try:
            if hour in list_hour:
                continue
        except TypeError:
            pass

        if len(hour_list[index_hour]) == max_len_row:
            index_hour += 1

        if hour > 23:
            hour = hour - 24

        hour_list[index_hour].append(
            KeyboardButton(
                text=f'{hour:02}:00'
            )
        )
    else:
        hour_list[index_hour+1].append(
            KeyboardButton(
                text=f'Назад'
            )
        )

    keyboard = ReplyKeyboardMarkup(
        keyboard=hour_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard


def generate_button_date():
    list_date =[[], []]
    now = datetime.now()

    plus_date = timedelta(days=7-now.weekday())
    date_begin_next_week = now + plus_date
    for i in range(7):
        day = date_begin_next_week + timedelta(days=i)
        list_date[0].append(
            KeyboardButton(
                text=f'{day.day}.{day.month}'
            )
        )
    else:
        list_date[1].append(KeyboardButton(
                text='Готово'
            ))

    keyboard = ReplyKeyboardMarkup(
        keyboard=list_date,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard


if __name__ == '__main__':
    now = datetime.now()
    print(last_day_of_month(now))
