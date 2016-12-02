'''
Birthday reminder.
Usage:
    reminder.py gmail <username> <password> --birthdays <json_file>
'''

from dateutil import parser
import datetime as dt
import json
import yagmail
from docopt import docopt
from retrying import retry


SERVER = None
SUBJECT = '''Birthday Reminder: {name_of_birthday_person}'s birthday on {date}'''
BODY = '''
Hi {name},

This is a reminder that {name_of_birthday_person}s will be celebrating their
birthday on {date}.

There are {amount_of_days} days left to get a present!'''

@retry(stop_max_attempt_number=3)
def send_mail(to, subject, body):
    SERVER.send(str(to), subject, body)

def send_mails(birthdays, username, password):
    global SERVER
    SERVER = yagmail.SMTP(username, password)
    enumerated = list(enumerate(check_file(birthdays)))
    for j, i in enumerated:
        difference = i['birthdate'] - dt.datetime.now()
        if  dt.timedelta(days=0) < difference < dt.timedelta(days=7):
            for k, l in enumerated:
                subject = SUBJECT.format(name_of_birthday_person=i['name'],
                                         date=dt.datetime.strftime(i['birthdate'], '%Y-%m-%d'))
                body = BODY.format(name=l['name'], name_of_birthday_person=i['name'],
                                   date=i['birthdate'].strftime('%Y-%m-%d'),
                                   amount_of_days=str(difference.days))
                if j != k:
                    print l['email']
                    send_mail(l['email'], subject, body)

def check_file(input):
    '''returns only valid records from json file, with birthday date this year'''
    f = open(input).read()
    js= json.loads(f)
    valid = []
    for i in js:
        try:
            birthdate = parser.parse(i['birthdate'], yearfirst=True)\
                .replace( year=dt.datetime.now().year)
            valid.append({'name':i['name'], 'email': i['email'], 'birthdate': birthdate})
        except Exception, ex:
            print 'failed to parse ', js[i]['birthdate']
    return valid

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Birthday reminder 1.0')
    if arguments['gmail']:
        send_mails(arguments['<json_file>'], arguments['<username>'], arguments['<password>'])