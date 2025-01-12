import time
import urllib.request 
from discord_webhook import DiscordWebhook, DiscordEmbed
from bs4 import BeautifulSoup
import re
import os
from datetime import date
import datetime
import calendar
from config import DISCORD_WEBHOOK_URL, SITE_URL, DATA

# def jobs() :

response = urllib.request.urlopen(SITE_URL)
update_time = response.headers['last-modified']
urllib.request.urlretrieve(SITE_URL, DATA+"jobs.html")
time.sleep(1)

html_page = open(DATA+"jobs.html", mode="r", encoding="utf8")

soup = BeautifulSoup(html_page, 'lxml')

jobs = []
CDDI = soup.find_all("tbody")[0]
tr = CDDI.find_all("tr")
count = 0
for x in tr :
    count += 1
    if count > 1 :
        job = []
        for y in x : 
            if y.text != "" :
                job.append(y.text)
                if re.search(r'a href', str(y)):
                    z = re.match(r'<td><a href="(offres/CD\d+.txt)">', str(y)).group(1)
                    z = SITE_URL.replace("offres.html", z)
                    job.append(z)
        jobs.append(job)

timestamp_maison = open(DATA+"last_job_was_on.txt", "r", encoding="utf8")
old = list(timestamp_maison)[0]
format_old = time.strptime(old, "%d/%m/%Y")
timestamp_maison.close()

new = jobs[0][0]
format_new = time.strptime(new, "%d/%m/%Y")

update = []
if format_new > format_old : 
    for x in jobs :
        format_test = time.strptime(x[0], "%d/%m/%Y")
        if format_test > format_old :
            update.append(x)
    timestamp_maison = open(DATA+"last_job_was_on.txt", "w", encoding="utf8")
    timestamp_maison.write(str(new))

#traitement des dates
today = datetime.date.today()
new_1 = new.split("/")
new_date = date(int(new_1[2]), int(new_1[1]), int(new_1[0]))
delta = today - new_date

month_to_num = {month: index for index, month in enumerate(calendar.month_abbr) if month}
test = re.match(r"\w+, (\d+\s\w+\s\d+)", update_time).group(1)
test = test.split()
update_date = date(int(test[2]), int(month_to_num[test[1]]), int(test[0]))
delta_2 = today - update_date

if delta_2.days == 0 :
    print(f"Last page update was today!")
else :
    print(f"Last page update was {delta_2.days} days ago ({update_time})")

if delta.days == 0 :
    print(f"\nLast job update was today!")
else :
    print(f"\nIl n'y a pas eu de nouvel emploi depuis {delta.days} jours.")
time.sleep(3)

# Post Results to Discord Channel
if update != []:
    for x in update :
        webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)
        with open(DATA+"alert.gif", "rb") as f:
            webhook.add_file(file=f.read(), filename='alert.gif')
        embed = DiscordEmbed(title='Nouvelle offre d\'emploi ! ', url=x[-1])
        embed.set_author(name='Le bot du travail', url=SITE_URL, icon_url='attachment://alert.gif')
        embed.set_timestamp()
        embed.add_embed_field(name='Date de publication', value=x[0])
        embed.add_embed_field(name='Entreprise', value=x[1])
        embed.add_embed_field(name='Lieu de travail', value=x[2])
        embed.add_embed_field(name='Type de poste', value=x[3])
        webhook.add_embed(embed)
        response = webhook.execute()

html_page.close()
if os.DATA.exists(DATA+"jobs.html"):
    os.remove(DATA+"jobs.html")

# schedule.every().day.at("09:00").do(jobs)
# schedule.every().day.at("14:00").do(jobs)
# schedule.every().day.at("19:30").do(jobs)

# while True :
#     schedule.run_pending()
#     time.sleep(1)