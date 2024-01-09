import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta



s = requests.Session()

#login to kitafino
s.get('https://www.kitafino.de')
r_login  =s.post('https://www.kitafino.de/sys_k2/index.php?action=do_login', data={'passwort': 'YOUR_PASSWORD', 'benutzername': 'YOUR_USERNAME' })


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
foo = soup.body.findAll('a',  {"name" : re.compile('menu*')})
returnvalue="udef"
#loop all items
for bar in foo:
    #extract date of current entry
    date_=bar['name'].replace('menu', '')
    item_date=datetime.utcfromtimestamp(int(date_))
    #print(item_date.strftime('%Y-%m-%d %H:%M:%S'))


    
    #go to next sibling of class "order_table"
    sibling=bar.find_next_sibling("div",{'class','order_table'})
    #find next tag of class "order_button_bestellt"
    order_sibling=sibling.find_next("a",{"class" : re.compile('order_button_bestellt')})
    #extract meal string and clean whitespaces
    mystring=order_sibling.text.strip().replace("\n", "").replace("\t", "")
    while '  ' in mystring:
        mystring = mystring.replace('  ', ' ')

    sep = '€'
    mystring = mystring.split(sep, 1)[0]
    listOfWords = mystring.split(" ", 1)
    if len(listOfWords) > 0: 
        mystring = listOfWords[1]
    #print clean meal
    #print(mystring)


    #print only todays meal
    today=datetime.now()
    if item_date.year==today.year:
       if item_date.month==today.month:
           if item_date.day==today.day:
                mystring = mystring.replace('(', ' (')
                returnvalue=mystring
                #print(mystring)
    
    
print(returnvalue)

