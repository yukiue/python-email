# python-email
extract events from emails

## Features
- Search emails using IMAP(Internet Message Access Protocol).
- Select whether to input from your terminal or load config file when importing your login information.
- Note that the subject must be in the following format:
```
(開催通知) NAME DATE START_TIME〜END_TIME
```

## Examples
### Input your login information from your terminal:
```shell
$ python client.py
Input your IMAP hostname, username and password
hostname: imap.gmail.com
username: abc@gmail.com
password:
abc@gmail.com authenticated (Success)
```
### Read your login information from config file:
edit .client.ini as follows
```
[info]
hostname = YOUR_HOSTNAME
username = YOUR_USERNAME
password = YOUR_PASSWORD
```
```shell
$ python client.py -f
abc@gmail.com authenticated (Success)
```

