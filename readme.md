# Email to Audio Converter

## Project Overview

This project is an semi-automated system that fetches specific emails from a Gmail account, consolidates their content, and converts it into an audio file. The primary goal is to allow me to listen to my daily newsletter emails, mostly from [TLDR](https://tldr.tech/), creating a personalized audio digest.

Every morning, I open infinity tabs and then never get around to reading their contents.  This aims to resolve that.  It will be fully automated when I upload it to the cloud and have it run on a schedule.  

## Initial Requirements

The initial use-case was to create an automation project with the following specifications:

1. Connect to a Gmail account and retrieve emails from specific senders.
2. The emails to be processed are various newsletters including "TLDR", "Bloomberg Technology", and "Interconnects by Nathan Lambert".
3. Extract the subject line and body content of each email.
4. Consolidate the extracted content into a single text file.
5. Convert the consolidated text into an audio file.

## Development Process

The development of this project was an iterative process and by "iterative", I mean a back-and-forth chat with Claude.ai:

1. **Initial Script Development**: We started by creating a Python script that could connect to Gmail using IMAP, search for specific emails, and extract their content. Actually, we started by configuring the Gmail account to allow IMAP connections and we generated a google app password.  And you'll need to do that as well if you're trying this at home. 

2. **Environment Variable Implementation**: Implemented the use of environment variables to store email credentials.

3. **Debugging and Error Handling**: We added basic error handling and debugging print statements to help identify and resolve issues during development. We left them in the code to proside some UX.  

4. **Refinement of Email Search**:  We were initially filtering emails by the sender's email address and the email's subject, but I had hard-coded values for the sender's email and the sender's name. Not the email's subject.  Fixed that, and it worked.  

5. **Text-to-Speech Integration**: We integrated the gTTS (Google Text-to-Speech) library to convert the consolidated text into an audio file.

## Technologies Used

- **Python**: The core programming language used for the project.
- **imaplib**: Python's built-in library for IMAP protocol operations.
- **email**: Python's built-in library for parsing email messages.
- **os**: Used for interacting with the operating system, particularly for environment variables.
- **dotenv**: Used to load environment variables from a .env file.
- **gTTS (Google Text-to-Speech)**: Used to convert text to speech.
- **datetime**: Used for date operations.

## How to Use

1. Clone the repository to your local machine.
2. Create a `.env` file in the project root with your Gmail credentials:
   ```
   EMAIL=your.email@gmail.com
   PASSWORD=your-app-password
   ```
3. Install the required Python packages:
   ```
   pip install python-dotenv gtts
   ```
4. Run the script:
   ```
   python email_to_audio.py
   ```
## Customization

To customize the emails that the script searches for, you need to modify the `sources` list in the `main()` function of the `email_to_audio.py` file. Each item in this list is a tuple containing two elements: the sender's email address and the sender's name.

Here's how the `sources` list looks in the script:

```python
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
```

To change the emails the script searches for:

1. Open `email_to_audio.py` in a text editor.
2. Locate the `sources` list in the `main()` function.
3. Modify, add, or remove entries from this list.
4. Each entry should be in the format: `("sender_email@example.com", "Sender Name")`

For example, if you want to add a new newsletter and remove one you don't read, you might change it to:

```python
sources = [
    ("dan@tldrnewsletter.com", "TLDR"),
    ("dan@tldrnewsletter.com", "TLDR AI"),
    ("newsletter@example.com", "My New Newsletter"),  # Added new newsletter
    ("dan@tldrnewsletter.com", "TLDR InfoSec"),
    ("dan@tldrnewsletter.com", "TLDR Founders"),
    ("dan@tldrnewsletter.com", "TLDR Crypto"),
    ("dan@tldrnewsletter.com", "TLDR Design"),
    ("dan@tldrnewsletter.com", "TLDR Web Dev"),
    ("dan@tldrnewsletter.com", "TLDR Marketing"),
    # Removed "TLDR DevOps"
    ("noreply@news.bloomberg.com", "Bloomberg Technology"),
    ("robotic@substack.com", "Interconnects by Nathan Lambert")
]
```

Remember to save the file after making your changes.

Note: The script searches for emails received on the current date from each sender in this list. Make sure the email addresses and names are correct, as any typos will result in those emails not being found.

## Output

### Successful Run

If the script runs successfully, you will see console output similar to this:

```
Attempting to connect to Gmail...
Successfully connected to Gmail.
Searching for emails from dan@tldrnewsletter.com (TLDR)...
Search criteria: (FROM "dan@tldrnewsletter.com" SENTON 11-Sep-2023)
Found 1 matching email(s).
Processing email ID: b'1'
Successfully processed email. Subject: TLDR Newsletter
...
[Similar output for other email sources]
...
Total content length: 15000 characters
Process completed. Text saved to consolidated_emails_2023-09-11.txt and audio saved to consolidated_emails_2023-09-11.mp3
```

The script will create two files:
1. A text file (`consolidated_emails_YYYY-MM-DD.txt`) containing the content of today's emails.
2. An MP3 file (`consolidated_emails_YYYY-MM-DD.mp3`) with the audio version of the content.

### Failed Run

If the script encounters issues, you might see error messages such as:

```
Failed to connect to Gmail. Error: [AUTHENTICATIONFAILED] Invalid credentials (Failure)
```
or
```
No emails found for TLDR (dan@tldrnewsletter.com)
...
No content was retrieved. Cannot create audio file.
```

These messages will help in diagnosing what went wrong, whether it's an authentication issue, no matching emails found, or other potential problems.

## Troubleshooting

If you encounter issues:

1. Ensure your Gmail account has IMAP enabled.
2. If you're using 2-Factor Authentication, make sure you're using an App Password.
3. Check that the email senders in the script match exactly with the senders in your inbox.
4. Verify that you have received emails from the specified senders on the current date.

## Future Enhancements

Well, first, I should probably improve it so that it removes URLs from being read verbally in the audio file. That's next. It'll be pretty annoying until I do that. 

Potential areas for future development include:
- Deployment to the cloud to run on a schedule
- Convert this into a cmd line app so that I can search emails and convert to audio on demand


