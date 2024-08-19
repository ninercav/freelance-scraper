import json
import os
from dotenv import load_dotenv
import time
from scraper_freelancermap import scrape_freelancermap
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from scraper_gulp import scrape_gulp


def send_mail(results):
    freelancermap_results, gulp_results = results['freelancermap'], results['gulp']

    msg = MIMEMultipart()
    msg['From'] = 'lifelongmemer@gmail.com'
    msg['To'] = 'leah.iliyav@gmail.com'
    msg['Subject'] = f'New reports from freelancermap and gulp ({freelancermap_results.__len__() + gulp_results.__len__()} projects found)'

    freelancermap_html_projects = ""
    gulp_html_projects = ""

    for project in freelancermap_results:
        freelancermap_html_projects += f"""
        <div>
            <h2>{project}</h2>
            <p><strong>Company:</strong> {freelancermap_results[project]['company']}</p>
            <p><strong>Location:</strong> {freelancermap_results[project]['location']}</p>
            <p><strong>Keywords:</strong> {', '.join(freelancermap_results[project]['keywords'])}</p>
            <p><strong>URL:</strong> <a href={freelancermap_results[project]['url']}>{freelancermap_results[project]['url']}</a></p>
        </div>
        """

    for project in gulp_results:
        gulp_html_projects += f"""
        <div>
            <h2>{project}</h2>
            <p><strong>Company:</strong> {gulp_results[project]['company'] if 'company' in gulp_results[project] else 'Not provided'}</p>
            <p><strong>Location:</strong> {gulp_results[project]['location']}</p>
            <p><strong>Start Date:</strong> {gulp_results[project]['start_date']}</p>
            <p><strong>URL:</strong> <a href={gulp_results[project]['url']}>{gulp_results[project]['url']}</a></p>
        </div>
        """

    html_content = f"""
    <html>
    <body>
        <h1>Freelancermap results</h1>
        <p><strong>Number of projects found:</strong> {freelancermap_results.__len__()}</p>
        {freelancermap_html_projects}
        
        <h1>Gulp results</h1>
        <p><strong>Number of projects found:</strong> {gulp_results.__len__()}</p>
        {gulp_html_projects}
    </body>
    </html>
    """

    msg.attach(MIMEText(html_content, 'html'))

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    smtp_user = os.getenv('GMAIL_ADDRESS')
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
        gulp_results = scrape_gulp()
        print("Freelancermap results:\n", freelancermap_results)
        print("Gulp results:\n", gulp_results)
        print(f"{freelancermap_results.__len__() + gulp_results.__len__()} new projects found!")
        send_mail({
            'freelancermap': freelancermap_results,
            'gulp': gulp_results
        })

        time.sleep(interval)


if __name__ == '__main__':
    load_dotenv()
    interval = os.getenv('POLL_INTERVAL')
    if not os.getenv('GMAIL_ADDRESS') or not os.getenv('GMAIL_PASSWORD'):
        raise Exception("Please set GMAIL_ADDRESS and GMAIL_PASSWORD as environment variables")
    poll_website(int(interval) if interval else None)