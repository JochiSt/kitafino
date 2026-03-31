import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import parse_qs

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

    url = None
    soup = BeautifulSoup(r_login.text, "lxml")
    links = soup.find_all('a')

    urls = []

    # get ACI from links in website
    for link in links:
        link_text = link.get('href')
        if not link_text:
            continue
        elif "javascript" in link_text:
            continue
        elif "index.php" in link_text:
            if "aci" in link_text:
                if not url:
                    url = link_text

            if "kw_ts" in link_text and "bestellen" in link_text:
                urls.append(link_text)
                #print(link_text)

    parsed_url = urlparse(urls[1])
    aci = parse_qs(parsed_url.query)['aci'][0]

    #calculate epoch of monday this week 11:00
    now = datetime.now()
    monday = now - timedelta(days = now.weekday())
    monday = monday.replace(hour=11,minute=0,second=0);
    monday = int((monday - datetime(1970, 1, 1)).total_seconds())
    if next_week:
        monday += 7*24*60*60 # for next week

    params = {
        'kw_ts': monday,
        'aci': aci
        }
    #kitafino_raw = s.get('https://app.kitafino.de/sys_k2/index.php?action=bestellen', params=params)
    kitafino_raw = s.get('https://user.kitafino.de/sys_k2/'+urls[1])
    kitafino_close = s.get('https://app.kitafino.de/sys_k2/index.php?action=log_out')
    #kitafino_close = s.get('https://user.kitafino.de/sys_k2/index.php?action=log_out')
    s.close()

    return kitafino_raw.text

if __name__ == "__main__":
    html_content = get_kitafino_response()
    with open('kitafino_raw.txt', 'w') as file:
        file.write(html_content)
