#!/usr/bin/env python3

import re

date = '(開催通知) 研究ミーティング 2020-03-16 (月) 13:30/15:00'

regex = re.compile(
    r'(.+)\s(\d{4})-(\d{2})-(\d{2})\s\((\w)\)\s(\d{2}):(\d{2})/(\d{2}):(\d{2})'
)

mo = regex.search(date)

print(mo)
print(mo.group())
print(mo.groups())
