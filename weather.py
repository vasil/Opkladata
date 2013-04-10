from datetime import datetime
from google.appengine.api import urlfetch 
from django.utils import simplejson as json

WEATHER_URL = 'http://api.openweathermap.org/data/2.1/find/name?q=%s' 
CITY = 'Skopje'

class Weather(object):
    @classmethod
    def get_temp(cls, city=CITY):
        url = WEATHER_URL % city
        result = urlfetch.fetch(url)
        
        if result.status_code == 200:
            json_data = json.loads(result.content.decode('utf-8'))
            temp_k = json_data['list'][0]['main']['temp']
            temp_url = json_data['list'][0]['url']
            current_datetime = json_data['list'][0]['date']
            current_datetime = (datetime.strptime(current_datetime, 
                                                 '%Y-%m-%d %H:%M:%S'))
            temperature = int(temp_k - 272.15);
            return (current_datetime, temperature, temp_url)
