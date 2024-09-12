import imaplib
import email
from email.header import decode_header
import os
import time
from gtts import gTTS
from datetime import date
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gmail account credentials
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

def connect_to_gmail():
    print("Attempting to connect to Gmail...")
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, PASSWORD)
        print("Successfully connected to Gmail.")
        return mail
    except Exception as e:
        print(f"Failed to connect to Gmail. Error: {str(e)}")
        raise

def get_emails(mail, sender_email, sender_name):
    print(f"Searching for emails from {sender_email} ({sender_name})...")
    mail.select("inbox")
    today = date.today().strftime("%d-%b-%Y")
    search_criteria = f'(FROM "{sender_email}" SENTON {today})'
    print(f"Search criteria: {search_criteria}")
    _, search_data = mail.search(None, search_criteria)
    email_ids = search_data[0].split()
    print(f"Found {len(email_ids)} matching email(s).")
    return email_ids

def process_email(mail, email_id):
    print(f"Processing email ID: {email_id}")
    try:
        _, msg_data = mail.fetch(email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        email_message = email.message_from_bytes(raw_email)

        subject = decode_header(email_message["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()

        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_message.get_payload(decode=True).decode()

        print(f"Successfully processed email. Subject: {subject}")
        return subject, body
    except Exception as e:
        print(f"Error processing email {email_id}. Error: {str(e)}")
        return None, None

def text_to_speech(text, filename):
    max_retries = 3
    delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            tts = gTTS(text)
            tts.save(filename)
            print(f"Successfully saved audio to {filename}")
            return
        except Exception as e:
            print(f"Attempt {attempt + 1} failed. Error: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print("Max retries reached. Could not create audio file.")
                raise

def main():
    mail = None
    try:
        mail = connect_to_gmail()
        
        sources = [
            ("dan@tldrnewsletter.com", "TLDR"),
            ("dan@tldrnewsletter.com", "TLDR AI"),
            ("dan@tldrnewsletter.com", "TLDR InfoSec"),
            ("dan@tldrnewsletter.com", "TLDR Founders"),
            ("dan@tldrnewsletter.com", "TLDR Crypto"),
            ("dan@tldrnewsletter.com", "TLDR Design"),
            ("dan@tldrnewsletter.com", "TLDR Web Dev"),
            ("dan@tldrnewsletter.com", "TLDR Marketing"),
            ("dan@tldrnewsletter.com", "TLDR DevOps"),
            ("noreply@news.bloomberg.com", "Bloomberg Technology"),
            ("robotic@substack.com", "Interconnects by Nathan Lambert")
        ]

        all_content = ""

        for sender_email, sender_name in sources:
            email_ids = get_emails(mail, sender_email, sender_name)
            if email_ids:
                latest_email_id = email_ids[-1]
                email_subject, email_body = process_email(mail, latest_email_id)
                if email_subject and email_body:
                    all_content += f"From: {sender_name}\nSubject: {email_subject}\n\n{email_body}\n\n"
            else:
                print(f"No emails found for {sender_name} ({sender_email})")

        print(f"Total content length: {len(all_content)} characters")

        if not all_content:
            print("No content was retrieved. Cannot create audio file.")
            return

        today = date.today().strftime("%Y-%m-%d")
        text_filename = f"consolidated_emails_{today}.txt"
        with open(text_filename, "w", encoding="utf-8") as f:
            f.write(all_content)

        audio_filename = f"consolidated_emails_{today}.mp3"
        text_to_speech(all_content, audio_filename)

        print(f"Process completed. Text saved to {text_filename} and audio saved to {audio_filename}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if mail:
            mail.logout()
            print("Logged out of Gmail.")

if __name__ == "__main__":
    main()
