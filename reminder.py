from dateutil import parser
import datetime as dt
import json
import yagmail
import click
from retrying import retry


SERVER = None
SUBJECT = '''Birthday Reminder: {name_of_birthday_person}'s birthday on {date}'''
BODY = '''
Hi {name},

This is a reminder that {name_of_birthday_person}s will be celebrating their
birthday on {date}.

There are {amount_of_days} left to get a present!'''

@retry(stop_max_attempt_number=3)
def send_mail(server, to, subject, body):
    SERVER.send(to, subject, body)

@click.command()
@click.option('--gmail_username', help='Your gmail username')
@click.option('--gmail_password', help='Your gmail password')
@click.option('--birthdays', help='json file  of names, emails, and birthdates',
type = click.File('r', encoding='utf8'))
def send_mails(birthdays, gmail_username, gmail_password):
    SERVER = yagmail.SMTP(gmail_username, gmail_password)
    enumerated = enumerate(check_file(birthdays))
    for j, i in enumerated:
        difference = i['birthdate'] - dt.datetime.now()
        if  dt.timedelta(days=0) < difference < dt.timedelta(days=7):
            subject = SUBJECT.format(name_of_birthday_person=i['name'], date=dt.strftime(i['birthdate'], '%Y-%m-%d'))
            body = BODY.format(name=l['name'], name_of_birthday_person=i['name'], amount_of_days=str(difference.days))
            for k, l in enumerated:
                if j != k:
                    send_mail(l['email'], subject, body)

def check_file(input):
    '''returns only valid records from json file, with birthday date this year'''
    f = input.read()
    js= json.loads(f)
    valid = []
    for i in js:
        try:
            birthdate = parser.parse(i['birthdate'], yearfirst=True)\
                .replace( year=dt.datetime.now().year)
            valid.append({'name':js[i]['name'], 'email': js[i]['email'], 'birthdate': birthdate})
        except Exception, ex:
            print 'failed to parse ', js[i]['birthdate']
    return valid

if __name__ == '__main__':
    send_mails()