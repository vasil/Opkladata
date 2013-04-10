import json
from datetime import datetime
from google.appengine.api import urlfetch 

WEATHER_URL = 'http://api.openweathermap.org/data/2.1/find/name?q=%s' 
CITY = 'Skopje'

class Weather(object):
    @classmethod
    def get_temp(cls, city=CITY):
        url = WEATHER_URL % city
        result = urlfetch.fetch(url)
        
        if result.status_code == 200:
            json_data = json.loads(result.content)
            
            temp_k = json.loads(json_data)['list']['main']['temp']
            temp_url = json.loads(json_data)['list'][0]['url']
            current_datetime = dom.getElementsByTagName('current_date_time')[0]
            curent_datetime = (datetime.strptime(data(current_datetime)[0:18], 
                                                 '%Y-%m-%d %H:%M:%S'))
            temperature = int(temp_k) - 272.15;
            return (curent_datetime, temperature, temp_url)
