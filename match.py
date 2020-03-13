#!/usr/bin/env python3

import re

date = '1/11 (火) 11:1〜12:10'

regex = re.compile(r'(\d{1,2})/(\d{1,2})\s\((\w)\)\s(\d{1,2}):(\d{1,2})〜(\d{1,2}):(\d{1,2})')

mo = regex.search(date)

print(mo)
print(mo.group())
print(mo.groups())
