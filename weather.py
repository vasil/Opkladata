from datetime import datetime

from google.appengine.api import urlfetch 
from xml.dom import minidom

WEATHER_URL = 'http://www.google.com/ig/api?weather=%s' 
CITY = 'Skopje'
 
data = lambda tag: tag.getAttribute('data') 


class Weather(object):
    @classmethod
    def get_temp(cls, city=CITY):
        url = WEATHER_URL % city
        result = urlfetch.fetch(url)
        
        if result.status_code == 200:
            dom = minidom.parseString(result.content)
            temp_c = dom.getElementsByTagName('temp_c')[0]
            current_datetime = dom.getElementsByTagName('current_date_time')[0]
            
            curent_datetime = (datetime.strptime(data(current_datetime)[0:18], 
                                                 '%Y-%m-%d %H:%M:%S'))
            temperature = int(data(temp_c)) 
            return (curent_datetime, temperature)
