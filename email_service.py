
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_notification(review_data):
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_SENDER_PASSWORD")
    RESTAURANT_OWNER_EMAIL = os.getenv("RESTAURANT_OWNER_EMAIL")

    if not all([EMAIL_SENDER, EMAIL_PASSWORD, RESTAURANT_OWNER_EMAIL]):
        print("Email configuration is missing. Skipping email notification.")
        return

    subject = f"New Customer Review from {review_data['customer_name']}"
    body = f"""
    Hello,

    You've received a new review. Here are the details and a suggested reply:

    ------------------------------------
    Customer Name: {review_data['customer_name']}
    Rating: {review_data['rating']}
    Review: "{review_data['review_text']}"
    ------------------------------------

    Detected Sentiment: {review_data['sentiment']}

    Suggested Reply:
    "{review_data['suggested_reply']}"

    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = RESTAURANT_OWNER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_SENDER, RESTAURANT_OWNER_EMAIL, text)
        server.quit()
        print(f"Email notification sent to {RESTAURANT_OWNER_EMAIL}")
    except Exception as e:
        print(f"Failed to send email: {e}")
