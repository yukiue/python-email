#!/usr/bin/env python3

import argparse
import calendar
import configparser
import datetime
import email
import re
from email.header import decode_header, make_header
from getpass import getpass

from imapclient import IMAPClient


def input_info():
    print('Input your IMAP hostname, username and password')
    hostname = input('hostname: ')
    username = input('username: ')
    password = getpass('password: ')

    return hostname, username, password


def read_info():
    config = configparser.ConfigParser()
    config.read('.client.ini')
    hostname = config['info']['hostname']
    username = config['info']['username']
    password = config['info']['password']

    return hostname, username, password


def get_subjects(hostname, username, password):
    with IMAPClient(host=hostname) as client:
        login = client.login(username, password)
        print(login.decode())
        client.select_folder('INBOX')

        msg = client.search(['SUBJECT', u'開催通知'], charset='utf-8')

        resp = client.fetch(msg, 'RFC822')

        subj_list = []
        for uid, data in resp.items():
            email_msg = email.message_from_bytes(data[b'RFC822'])
            # subj = str(make_header(decode_header(email_msg["Subject"])))

            subj = str(make_header(decode_header(email_msg.get("Subject"))))
            if subj.startswith("(開催通知)"):
                subj_list.append(subj)

        return subj_list


def get_events(subj_list):
    all_event_list = []
    for subj in subj_list:
        event = subj.split(maxsplit=1)[1]
        all_event_list.append(event)

    return all_event_list


def ext_day_events(all_event_list, date):
    event_dict = {}
    for event in all_event_list:
        regex = re.compile(
            r'(.+)\s(\d{4})-(\d{2})-(\d{2})\s\((\w)\)\s(\d{2}):(\d{2})/(\d{2}):(\d{2})'
        )
        mo = regex.search(event)

        if mo is not None:
            if str(int(mo.group(3))) == str(date.month) and str(
                    int(mo.group(4))) == str(date.day):
                event_dict[event] = datetime.time(int(mo.group(6)),
                                                  int(mo.group(7)))

    return sorted(event_dict.keys(), key=lambda e: event_dict[e])


def ext_week_events(all_event_list, date):
    def beginning_week(date):
        weekday = date.weekday()
        return date - datetime.timedelta(days=weekday)

    beginning_week = beginning_week(date)

    event_list = []
    for i in range(7):
        d = beginning_week + datetime.timedelta(days=i)
        event_list += ext_day_events(all_event_list, d)

    return event_list


def ext_month_events(all_event_list, date):
    def beginning_month(date):
        day = date.day
        return date - datetime.timedelta(days=day - 1)

    beginning_month = beginning_month(date)
    month_range = calendar.monthrange(date.year, date.month)

    event_list = []
    for i in range(month_range[1]):
        d = beginning_month + datetime.timedelta(days=i)
        event_list += ext_day_events(all_event_list, d)

    return event_list


def parse_args():
    parser = argparse.ArgumentParser(description='extract events from emails')

    parser.add_argument('-t',
                        '--type',
                        help='specify display type',
                        type=str,
                        choices=[
                            'today', 'tomorrow', 'this_week', 'next_week',
                            'this_month', 'all'
                        ],
                        default='today')
    parser.add_argument(
        '-f',
        '--file',
        help='read your login information from config file',
        action='store_true',
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if args.file:
        hostname, username, password = read_info()
    else:
        hostname, username, password = input_info()

    subj_list = get_subjects(hostname, username, password)
    all_event_list = get_events(subj_list)
    today = datetime.date.today()

    _type = args.type
    if _type == 'today':
        event_list = ext_day_events(all_event_list, today)
    elif _type == 'tomorrow':
        event_list = ext_day_events(all_event_list,
                                    today + datetime.timedelta(days=1))
    elif _type == 'this_week':
        event_list = ext_week_events(all_event_list, today)
    elif _type == 'next_week':
        event_list = ext_week_events(all_event_list,
                                     today + datetime.timedelta(weeks=1))
    elif _type == 'this_month':
        event_list = ext_month_events(all_event_list, today)
    elif _type == 'all':
        event_list = all_event_list

    for event in event_list:
        print(event)


if __name__ == "__main__":
    main()
