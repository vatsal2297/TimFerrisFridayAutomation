from authentication import gmail_authenticate
from dbconnection import *
import os
import re
import base64
from bs4 import BeautifulSoup, NavigableString
from datetime import datetime
import time
import pytz

# Get the message
def get_email(service, user_id, msg_id, log_file):    
    try:
        message = service.users().messages().get(userId = user_id, id = msg_id).execute()
        return message
    except Exception as error:
        log_file.write(f'Error: Fetching Message: {error} \n')
        return None
            
# Process and filter the emails
def process_email(connection, msg, counter, skip_threshold, log_file, local_timezone):                  
    old_version_email_detector = 0

    headers = msg['payload']['headers']
    subject = ''
    sender = '' 

    for header in headers:
        if header['name'] == 'Subject':
            subject = header['value']
        if header['name'] == 'From':
            sender = header['value']
   
    #re.search(r'^\d+-Bullet Friday.*', subject) or re.search(r'^\d+-BF.*', subject)
    if (re.search(r'^(Mega )?\d+-(BF|Bullet Friday|Bullet Saturday|Bullet Sunday).*', subject)): 
        log_file.write(f"{'=' * 60}\n")
        log_file.write(f"Processing Message... {msg['id']}\n")
        log_file.write(f"{'=' * 60}\n")
        
        counter += 1
        email_date = ""

        if counter <= skip_threshold:
            log_file.write(f"Skipping email: {subject}, from: {sender} \n")
            return counter, old_version_email_detector
        else:
            log_file.write(f"Processing email: {subject}, from: {sender} \n")
            
            # Convert Email Internal date from epoch (ms) to datetime format
            email_date = datetime.fromtimestamp(int(msg['internalDate']) / 1000, pytz.utc).astimezone(local_timezone).strftime('%Y-%m-%d %H:%M:%S')

            for part in msg['payload']['parts']:
                if part['mimeType'] == "text/html":
                    data = part['body']['data']
                    data = str(data).replace("-","+").replace("_","/")
                    html_content = base64.b64decode(data).decode("utf-8")
                    old_version_email_detector = parse_bullet_points(msg['id'], email_date, subject, html_content, log_file, connection)
            
            return counter, old_version_email_detector
    else:
        return counter, old_version_email_detector

# Parse bullets for each email
def parse_bullet_points(msg_id, email_date, subject, html_content, log_file, connection):
    log_file.write(f"{'=' * 60}\n")
    log_file.write(f"{msg_id} | {email_date} \n")
    log_file.write(f"{'=' * 60}\n")
    log_file.write(f"Parsing Bullets... \n")
    log_file.write(f"{'=' * 60}\n")

    span_tag = None
    strong_bullet_tags = []
    heading_text = ""
    bullet_content = []
    last_row_id = 0

    soup = BeautifulSoup(html_content, "html.parser")

    # if soup.find('hr'):
    #     log_file.write("This is a newer version of 5-Bullet Friday \n")
    #     return -1
    # elif soup.find_all('div', role="separator"):
    #     separate_divs = soup.find_all('div', role="separator")
    #     if len(separate_divs) > 2:
    #         log_file.write("This is a newer version of 5-Bullet Friday \n")
    #         return -1
    if soup.find_all('span'):
        span_tags = soup.find_all('span')
        for tag in span_tags:
            if (re.search(r'^And, as always, please give me feedback on Twitter.*', tag.text) or
                re.search(r'^And there you have it.', tag.text)
                ):
                span_tag = tag
                break
    else:
        log_file.write("This is a different version of 5-Bullet Friday \n")
        return -1

    log_file.write(f"Span Tag Detected: {span_tag}\n")   

    try:
        last_row_id = insert_friday_email(connection, msg_id, email_date, subject, log_file)
        log_file.write(f"tff_5bullet_email record inserted with ID: {last_row_id} \n")
    except Exception as error:
        log_file.write("Insertion Failed for tff_5bullet_email !!!")
        log_file.write(f"{subject} | Error: {error}")
    
    log_file.write(f"{'-' * 60}\n")

    for strong_tag in soup.find_all('strong'):
        if re.search(r'^.* — ?$', strong_tag.text) and span_tag not in strong_tag.find_all_previous():
            heading_text = strong_tag.text.replace("\u200b", "").replace("—", "").strip()
            
            paragraph_text = ""
            paragraph_content = []
            
            for sibling in strong_tag.find_next_siblings():
                if sibling == span_tag or (sibling.name == 'strong' and re.search(r'^.* — ?$', sibling.text)):
                    break
                else:
                    paragraph_content.append(str(sibling).replace("\u200b",""))
                    if sibling.next_sibling == "\u200b" or sibling.next_sibling == " ":
                        paragraph_content.append(" ")
        
            paragraph_text = ''.join(paragraph_content)

            # Identify and remove style attributes from each paragraph tags to keep the styling neutral (after combining all paras)
            # Identify and remove tags from each paragraph to get the searchable text
            paragraph_text_stripped, paragraph_text_searchable = re.sub(r'style="[^"]*"', "", paragraph_text), re.sub(r'<[^>]*>', "", paragraph_text)
            log_file.write(f"{heading_text}: {len(paragraph_text)} | {len(paragraph_text_stripped)} | {len(paragraph_text_searchable)}\n")
            bullet_content.append((int(last_row_id), heading_text, paragraph_text_stripped, paragraph_text_searchable))
            log_file.write(f"{'-' * 60}\n")

    log_file.write(f"Number of Bullets: {len(bullet_content)} \n")

    rows_affected = 0
    try:
        rows_affected = insert_email_bullets(connection, bullet_content, log_file)
        log_file.write(f"tff_bullets records inserted: {rows_affected} rows affected \n")
    except Exception as error:
        log_file.write("Insertion Failed for tff_bullets !!! \n")
        log_file.write(f"{rows_affected} | Error: {error} \n")

    log_file.write(f"{'=' * 100}\n\n\n")
    return 0

if __name__ == "__main__":
    # Opens the file object for logging purpose
    CURR_DIR = os.path.dirname(os.path.realpath(__file__))
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    
    tff_5bullet_log_file = None
    log_file = f"{str(CURR_DIR)}/5BulletDBOldLog_{current_datetime}.txt"
    if not os.path.exists(log_file):
        tff_5bullet_log_file = open(log_file, "w", encoding="utf-8")
    else:
        tff_5bullet_log_file = open(log_file, "w", encoding="utf-8")

    # Calculate execution time - START
    start = time.time()

    skip_threshold = 0
    counter = 0
    limit_emails = 500 #200
    old_version_email_detector = 0
    LOCAL_TIMEZONE = pytz.timezone("America/New_York")
    internal_date_start = int(LOCAL_TIMEZONE.localize(datetime(2022, 3, 18, 0, 0, 0)).astimezone(pytz.utc).timestamp() * 1000)

    # Access Gmail API Service and authenticate the user
    service = gmail_authenticate(tff_5bullet_log_file)
    if not service:
        tff_5bullet_log_file.write("Something wrong with Gmail Authentication !!!")
        tff_5bullet_log_file.write("Exiting Program...\n")
        exit()

    # Initializing attributes for Gmail API
    USER_ID = "me"
    LABEL_IDS = ['CATEGORY_UPDATES', 'INBOX']
    QUERY = 'from: Tim Ferriss <tim@fourhourbody.com>'
    MAX_RESULTS = 50 #15
    next_page_token = None
    
    # Check if db is available to connect and exit in case of failure
    tff_5bullet_log_file.write(f"{'=' * 60}\n")
    tff_5bullet_log_file.write("Connecting to Database...\n")
    tff_5bullet_log_file.write(f"{'=' * 60}\n")
    if not db_connect(tff_5bullet_log_file):
        tff_5bullet_log_file.write("Db Connection Failed !!!\n")
        tff_5bullet_log_file.close()
        exit()
    else:
        connection = db_connect(tff_5bullet_log_file)

    # The Email fetching process starts here
    tff_5bullet_log_file.write(f"{'=' * 60}\n")
    tff_5bullet_log_file.write("Starting to Get Emails...\n")
    tff_5bullet_log_file.write(f"{'=' * 60}\n")
    while True:
        # Fetch emails and use next page token if available
        results = service.users().messages().list(
            userId = USER_ID, 
            labelIds = LABEL_IDS,
            q = QUERY, 
            maxResults = MAX_RESULTS, 
            pageToken = next_page_token
        ).execute()

        # Fetch the list of messages based on above parameters
        messages = results.get("messages", [])

        # if there are no emails, then break
        if not messages:
            tff_5bullet_log_file.write("No emails found !!! \n")
            break
        
        # Process each email
        for msg in messages:
            message = get_email(service, USER_ID, msg['id'], tff_5bullet_log_file)
            if message and int(message['internalDate']) < internal_date_start:
                counter, old_version_email_detector = process_email(connection, message, counter, skip_threshold, tff_5bullet_log_file, LOCAL_TIMEZONE)
                if counter >= skip_threshold + limit_emails or old_version_email_detector < 0: #5
                    break

        # Check if there is next page token for next batch of emails and 
        # the number of emails required to be fetched are still remaining
        if old_version_email_detector == 0 and counter <= limit_emails: #and counter <= skip_threshold
            next_page_token = results.get("nextPageToken")
        else:
            next_page_token = None

        # If no next page token found, then all emails are fetched and task is completed
        if not next_page_token:
            tff_5bullet_log_file.write(f"\n\n\n{'=' * 100}\n")
            tff_5bullet_log_file.write("End: All emails have been fetched \n")
            break
        else:
            # Wait for 1 second after each API batch call
            time.sleep(1)
    
    # Calculate execution time - STOP
    end = time.time()
    
    tff_5bullet_log_file.write(f"{'=' * 100}\n")
    tff_5bullet_log_file.write(f"\n\nTotal emails found: {counter} \n")
    tff_5bullet_log_file.write(f"Total execution time: {end - start} \n")
    
    # Close the file if open
    if not tff_5bullet_log_file.closed:
        tff_5bullet_log_file.close()
    
    # Close the db connection if open
    if connection and connection.is_connected():
        connection.close()


