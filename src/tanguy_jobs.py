import time
import urllib.request 
from discord_webhook import DiscordWebhook, DiscordEmbed
from bs4 import BeautifulSoup
import re
import os
from datetime import date, timedelta, datetime
import calendar
from config import DISCORD_WEBHOOK_URL, SITE_URL, DATA, MEDIA

def fetch_jobs() :
    response = urllib.request.urlopen(SITE_URL)
    update_time = response.headers['last-modified']
    urllib.request.urlretrieve(SITE_URL, DATA+"jobs.html")
    time.sleep(1)
    return update_time

def parse_jobs(update_time) :
    jobs = []
    with open(DATA+"jobs.html", mode="r", encoding="utf8") as html_page:
        soup = BeautifulSoup(html_page, 'lxml')
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
    return jobs

def no_datefile_found():
    two_days_ago = date.today() - timedelta(days=2)
    formatted_date = two_days_ago.strftime("%d/%m/%Y")
    with open(DATA+"last_job_was_on.txt", "w") as file:
        file.write(formatted_date)
    print("Writing starting date as", formatted_date)

def get_last_saved_job_date():
    with open(DATA+"last_job_was_on.txt", "r", encoding="utf8") as timestamp_maison :
        old = list(timestamp_maison)[0]
        return datetime.strptime(old, "%d/%m/%Y")
    
def update_last_job_date(new_date):
    with open(DATA + "last_job_was_on.txt", "w", encoding="utf8") as timestamp_maison:
        timestamp_maison.write(new_date.strftime("%d/%m/%Y"))

def process_dates(new_date_str, update_time):
    today = datetime.today()
    new_date = datetime.strptime(new_date_str, "%d/%m/%Y")
    delta = today - new_date

    month_to_num = {month: index for index, month in enumerate(calendar.month_abbr) if month}
    test = re.match(r"\w+, (\d+\s\w+\s\d+)", update_time).group(1)
    test = test.split()
    update_date = datetime(int(test[2]), int(month_to_num[test[1]]), int(test[0]))
    delta_2 = today - update_date

    if delta_2.days == 0:
        print(f"Last page update was today!")
    else:
        print(f"Last page update was {delta_2.days} days ago ({update_time})")

    if delta.days == 0:
        print(f"\nLast job update was today!")
    else:
        print(f"\nIl n'y a pas eu de nouvel emploi depuis {delta.days} jours.")

def post_to_discord(update):
    for x in update:
        webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)
        with open(MEDIA + "alert.gif", "rb") as f:
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

def main():
    if not os.path.exists(DATA+"last_job_was_on.txt"):
        no_datefile_found()
    update_time = fetch_jobs()
    if update_time:
        jobs = parse_jobs(update_time)
        if jobs:
            old_date = get_last_saved_job_date()
            if old_date:
                new_date = datetime.strptime(jobs[0][0], "%d/%m/%Y")
                update = [x for x in jobs if datetime.strptime(x[0], "%d/%m/%Y") > old_date]
                if update:
                    update_last_job_date(new_date)
                    process_dates(jobs[0][0], update_time)
                    post_to_discord(update)

    if os.path.exists(DATA + "jobs.html"):
        os.remove(DATA + "jobs.html")

if __name__ == "__main__":
    main()
# schedule.every().day.at("09:00").do(jobs)
# schedule.every().day.at("14:00").do(jobs)
# schedule.every().day.at("19:30").do(jobs)

# while True :
#     schedule.run_pending()
#     time.sleep(1)