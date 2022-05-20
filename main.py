from random import randint
import datetime as dt
import smtplib
import pandas

MY_EMAIL = #your e-mail goes here as string ie. 'email@email.com'
MY_PASSWORD = #your password goes here as string ie. 'easypassword123'
SMTP_ADRESS = #SMTP adress of your e-mail service provider ie. "smtp.gmail.com"

# ----------- CSV HANDLING ---------- #
data = pandas.read_csv('birthdays.csv')

# ---------- CHECKING FOR BIRTHDAYS ----------- #
today = dt.datetime.now()
emails = None
try:
    emails = data.loc[(data['month'] == today.month) & (data['day'] == today.day), ['name', 'email']]
except KeyError:
    pass

list_to_send = []
if len(emails.index) > 0:
    for i, person in emails.iterrows():
        email = emails.email.loc[i]
        name = emails.name.loc[i]
        email_model = randint(1, 3)
        list_to_send.append((name, email, email_model))
else:
    print('no birthdays today')

with smtplib.SMTP(SMTP_ADRESS) as connection:
    connection.starttls()
    connection.login(user=MY_EMAIL, password=MY_PASSWORD)
    for n in list_to_send:
        with open(f"letter_templates/letter_{n[2]}.txt") as file:
            text = file.read()
            msg = text.replace('[NAME]', n[1])
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=n[1],
                                msg=f"To: {n[1]}\nSubject: Happy Birthday!!! \n\n{msg}")