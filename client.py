#!/usr/bin/env python3

import email
from imapclient import IMAPClient
from email.header import decode_header, make_header
from getpass import getpass
import datetime
import argparse


def input_info():
    print('Input your IMAP hostname, username and password')
    hostname = input('hostname: ')
    username = input('username: ')
    password = getpass('password: ')

    return hostname, username, password


def get_subject(hostname, username, password):
    with IMAPClient(host=hostname) as client:
        client.login(username, password)
        client.select_folder('INBOX')

        msg = client.search(['SUBJECT', u'開催通知'], charset='utf-8')

        resp = client.fetch(msg, 'RFC822')

        subj_list = []
        for uid, data in resp.items():
            email_msg = email.message_from_bytes(data[b'RFC822'])
            # subj = str(make_header(decode_header(email_msg["Subject"])))

            subj = str(make_header(decode_header(email_msg.get("Subject"))))
            subj_list.append(subj)

        return subj_list


def ext_day_events(subj_list, date):
    for subj in subj_list:
        if 'Re:' not in subj and len(subj.split()) == 5:
            subj_sep = subj.split()
            if str(date.month) + '/' + str(date.day) == subj_sep[2]:
                print(subj_sep[1], subj_sep[2], subj_sep[3], subj_sep[4])


def ext_week_events(subj_list, date):
    def beginning_week(date):
        weekday = date.weekday()
        return date - datetime.timedelta(days=weekday)

    beginning_week = beginning_week(date)

    for i in range(7):
        d = beginning_week + datetime.timedelta(days=i)
        ext_day_events(subj_list, d)


def parse_args():
    parser = argparse.ArgumentParser(description='extract events from e-mail')

    parser.add_argument('-t', '--type',
                        help='specify display type', type=str,
                        choices=['today', 'tomorrow', 'this_week', 'next_week'],
                        default='day')

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    _type = args.type
    hostname, username, password = input_info()
    subj_list = get_subject(hostname, username, password)
    today = datetime.date.today()
    if _type == 'today':
        ext_day_events(subj_list, today)
    elif _type == 'tomorrow':
        ext_day_events(subj_list, today + datetime.timedelta(days=1))
    elif _type == 'this_week':
        ext_week_events(subj_list, today)
    elif _type == 'next_week':
        ext_week_events(subj_list, today + datetime.timedelta(weeks=1))


if __name__ == "__main__":
    main()
