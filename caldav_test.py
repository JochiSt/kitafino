
### Imports
import sys
from datetime import datetime, timedelta, time
import caldav
import credentials

### Variables
NEXTCLOUD_HOSTNAME = credentials.caldav_hostname
CALDAV_CALENDAR_NAME = credentials.caldav_calendar_name
CALDAV_USER_NAME = credentials.caldav_user_name

# build url for connecting to nextcloud
url  = "https://"+ NEXTCLOUD_HOSTNAME +"/remote.php/dav/calendars/"
url += CALDAV_USER_NAME + "/"
url += CALDAV_CALENDAR_NAME + "/"

today  = datetime.combine(datetime.today(), time(0,0))

# connect to nextcloud
client = caldav.DAVClient(url,
                          username=credentials.caldav_login["username"],
                          password=credentials.caldav_login["password"],
                          ssl_verify_cert=False)
principal = client.principal()
calendars = principal.calendars()

# search for the matching calendar
calendar = None
for cal in calendars:
    if CALDAV_CALENDAR_NAME.upper() == str(cal).upper():
        print("Calendar "+ CALDAV_CALENDAR_NAME +" found")
        calendar = cal

if calendar:
    may_event = calendar.save_event(
        dtstart=datetime(2025, 6, 17, 6),
        dtend=datetime(2025, 6, 18, 1),
        summary="Do the needful",
    )