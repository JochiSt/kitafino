import requests
from datetime import datetime, timedelta

import credentials

def get_kitafino_response(next_week = True):
    #login to kitafino
    s = requests.Session()
    s.get('https://www.kitafino.de')
    r_login  =s.post('https://auth.kitafino.de/sys_k2/index.php?action=do_login',
                        data={
                            'passwort': credentials.kitafino_login['password'],
                            'benutzername': credentials.kitafino_login['username'],
                            }
                    )

    #calculate epoch of monday this week 11:00
    now = datetime.now()
    monday = now - timedelta(days = now.weekday())
    monday = monday.replace(hour=10,minute=0,second=0);
    monday = int((monday - datetime(1970, 1, 1)).total_seconds())
    if next_week:
        monday += 7*24*60*60 # for next week

    params = {'kw_ts': monday}
    kitafino_raw = s.get('https://app.kitafino.de/sys_k2/index.php?action=bestellen', params=params)
    kitafino_close = s.get('https://app.kitafino.de/sys_k2/index.php?action=log_out')
    s.close()

    return kitafino_raw.text

if __name__ == "__main__":
    html_content = get_kitafino_response()
    with open('kitafino_raw.txt', 'w') as file:
        file.write(html_content)