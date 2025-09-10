import argparse

import kitafino
import parse_kitafino
import caldav_calendar

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="kitafino 2 caldav")
    parser.add_argument('--current_week', action='store_true', help='get meals for current week')
    args = parser.parse_args()

    calendar = caldav_calendar.calDAVconnect()

    if args.current_week:
        kitafino_raw = kitafino.get_kitafino_response(next_week=False)
    else:
        kitafino_raw = kitafino.get_kitafino_response()

    kitafino_parsed = parse_kitafino.extract_meal_data(kitafino_raw)

    for (date, meal) in kitafino_parsed:
        if meal:
            caldav_calendar.createWholeDayEvent(calendar, date, meal)