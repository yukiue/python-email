#!/usr/bin/env python3

import re

date = '開催通知 1/11 (火) 1:32〜12:10'

regex = re.compile(r'(\w+)\s(\d{1,2})/(\d{1,2})\s\((\w)\)\s(\d{1,2}):(\d{1,2})〜(\d{1,2}):(\d{1,2})')

mo = regex.search(date)

print(mo)
print(mo.group())
print(mo.groups())
