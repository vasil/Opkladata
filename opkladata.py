import os
import logging
import datetime
from weather import Weather

from google.appengine.api import mail
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 

ORDER = [_, '1st', '2nd', '3rd']
TIME = [_, '08:00', '13:00', '17:00']
MEASURE_EMAIL_TEMPLATE = 'measure_email.txt'

class Record(db.Model):
    temperature = db.IntegerProperty()
    date = db.DateProperty(auto_now_add=True)
    datetime = db.DateTimeProperty(auto_now_add=True)

class BaseHandler(webapp.RequestHandler):
    def render_mail(self, mail_template, template_values):
        message = mail.EmailMessage()
        message.sender = "Measured Temperature <vasil@noobiru.com>"
        message.subject = "The %s measured temperature today." % \
                          template_values['order']
        message.to = "SUDIJA"
        message.cc = """NATPREVARUVACH1,
                        NTPREVARUVACH2,
                        DELEGAT1"""
        path = os.path.join(os.path.dirname(__file__), 'templates', 
                            mail_template)
        message.body = template.render(path, template_values)
        message.send()

    def render_html(self, data):
        pass

class MeasureHandler(BaseHandler):
    def get(self, time):
        (_, measured_temp) = Weather.get_temp('Skopje')
        record = Record()
        record.temperature = measured_temp
        record.put()
        today = datetime.date.today()
        todays_records = Record.all().filter('date', today).fetch(3)
        template_values = {'temperature': measured_temp,
                           'order': ORDER[int(time)],
                           'time': TIME[int(time)]}
        if len(todays_records) >= 3:
            sum = reduce(lambda a, b: a+b.temperature, todays_records, 0)
            template_values['mean'] = round(float(sum) / len(todays_records))
            template_values['day'] = today.strftime('%B %d')
        self.render_mail(MEASURE_EMAIL_TEMPLATE, template_values)


class InsightsHandler(BaseHandler):
    pass #Sorry. Not this time.

class LogMailHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Mail from: %s: %s" % (mail_message.sender, 
                                            mail_message.subject))

application = webapp.WSGIApplication([
    ('/measure/(.*)', MeasureHandler),
    ('/insights', InsightsHandler),
    LogMailHandler.mapping()
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
