from operator import indexOf
import os
import pandas as pd
import re
import subprocess
import smtplib
read_file = pd.read_excel("~/Downloads/mail-check-jacksonville.xlsx")
read_file_charlotte = pd.read_excel("~/Downloads/mail-check-charlotte.xlsx")
df = pd.DataFrame(read_file)
for x in df["Email"][:1]:
    output = subprocess.run(["nslookup", "-type=mx", re.search(r"[a-z]+[.][a-z]+", x).group()], capture_output=True).stdout
    email = output.decode('utf-8')
    email_list = list(filter(bool, email.splitlines()))
    smtps = []
    for y in email_list:
        email_and_number = re.search(r"[0-9][0-9]?\s(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)", y)
        if email_and_number is not None:
            smtps.append(email_and_number.group())
    smtp_to_check = ''
    list_ints = []
    list_emails = []
    for z in smtps:
        z_list = z.split()
        list_ints.append(int(z_list[0]))
        list_emails.append(z_list[1])
    preferred_smtp = list_emails[list_ints.index(min(list_ints))][:-1]
    output = subprocess.run(["nc", "-v", "google.com", "80",])
    if output.returncode == 1:
        print("Process timed out")
        exit
    output = subprocess.run(['HELO', 'google.com'])
server = smtplib.SMTP()
server.connect('smtp.gmail.com', '587')
server.set_debuglevel(1)
server.verify('rphatak@berkeley.edu')
server.quit()

    