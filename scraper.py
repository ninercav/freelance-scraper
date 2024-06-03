import json
import os
from dotenv import load_dotenv
import time
from scraper_freelancermap import scrape_freelancermap
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(results):
    msg = MIMEMultipart()
    msg['From'] = 'lifelongmemer@gmail.com'
    msg['To'] = 'leah.iliyav@gmail.com'
    msg['Subject'] = 'New reports from Freelancermap'
    text = json.dumps(results, indent=2)  # todo: add better formatting

    msg.attach(MIMEText(text, 'plain'))

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'lifelongmemer@gmail.com'

    load_dotenv()
    smtp_password = os.getenv('GMAIL_PASSWORD')

    # Send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def poll_website(interval=30):
    print("Polling websites...")
    while True:
        freelancermap_results = scrape_freelancermap()
        print(f"{freelancermap_results.__len__()} new projects found!")
        print("Freelancermap results:\n", freelancermap_results)
        send_mail(freelancermap_results)

        time.sleep(interval)


if __name__ == '__main__':
    poll_website()
