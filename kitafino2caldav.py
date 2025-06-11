

import kitafino
import parse_kitafino
import caldav_calendar

if __name__ == "__main__":
    calendar = caldav_calendar.calDAVconnect()
    kitafino_raw = kitafino.get_kitafino_response()
    kitafino_parsed = parse_kitafino.extract_meal_data(kitafino_raw)

    for (date, meal) in kitafino_parsed:
        if meal:
            caldav_calendar.createWholeDayEvent(calendar, date, meal)