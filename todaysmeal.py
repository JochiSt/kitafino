import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

import credentials

#login to kitafino
s = requests.Session()
s.get('https://www.kitafino.de')
r_login  =s.post('https://www.kitafino.de/sys_k2/index.php?action=do_login',
                    data={
                        'passwort': credentials.kitafino_login['password'],
                        'benutzername': credentials.kitafino_login['username'],
                        }
                )

#calculate epoch of monday this week 11:00
now = datetime.now()
monday = now - timedelta(days = now.weekday())
monday=monday.replace(hour=11,minute=0,second=0);
monday= int((monday - datetime(1970, 1, 1)).total_seconds())

params = {'kw_ts': monday}
kitafino_raw = s.get('https://www.kitafino.de/sys_k2/index.php?action=bestellen', params=params)
kitafino_close = s.get('https://www.kitafino.de/sys_k2/index.php?action=log_out')
s.close()

#use BeautifulSoup to extract needed Parts
soup = BeautifulSoup(kitafino_raw.text, "html.parser")

#search all <a name=menuexxxxxxxx> -> each on is start of one entry
foo = soup.body.findAll('div',  {"class" : re.compile('order_table*')})
returnvalue="udef"
#loop all items
for bar in foo:

    #find next tag of class "order_button_bestellt"
    order_sibling=bar.find_next("a",{"class" : re.compile('order_button_bestellt*')})
    #extract meal string and clean whitespaces
    dateSibling=bar.find_next("strong",{"class" : re.compile('left*')})
    mystring=dateSibling.text.strip().replace("\n", "").replace("\t", "")
    while '  ' in mystring:
        mystring = mystring.replace('  ', ' ')

    sep = ' '
    mystring = mystring.split(sep, 1)[1]
    item_date = datetime.strptime(mystring, "%d.%m.%Y")
    #print(item_date.strftime('%Y-%m-%d %H:%M:%S'))

    order=order_sibling.text.strip().replace("\n", "").replace("\t", "")
    while '  ' in order:
        order = order.replace('  ', ' ')
    sep = ' '
    sep = '€'
    order = order.split(sep, 1)[0]

    listOfWords = order.split(" ", 1)
    if len(listOfWords) > 0:
        order = listOfWords[1]
    print(item_date, order)

    today=datetime.now()
    if item_date.year==today.year:
       if item_date.month==today.month:
           if item_date.day==today.day:
                order = order.replace('(', ' (')
                returnvalue=order
                #print(mystring)

