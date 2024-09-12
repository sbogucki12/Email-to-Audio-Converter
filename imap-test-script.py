import imaplib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

# Attempt to connect to Gmail's IMAP server
try:
    # Create an IMAP4 client connected to Gmail's SSL server
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    
    # Attempt to login
    imap.login(EMAIL, PASSWORD)
    
    # If login is successful, list available mailboxes
    print("Successfully connected to Gmail IMAP server.")
    print("Available mailboxes:")
    status, mailboxes = imap.list()
    for mailbox in mailboxes:
        print(mailbox.decode().split()[-1])
    
    # Logout
    imap.logout()
except imaplib.IMAP4.error as e:
    print(f"An error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
