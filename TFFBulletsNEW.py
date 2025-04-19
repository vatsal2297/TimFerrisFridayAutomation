from authentication import gmail_authenticate
from dbconnection import *
import os
import re
import base64
from bs4 import BeautifulSoup
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
        log_file.write("==========================================================\n")
        log_file.write(f"Processing Message... {msg['id']}\n")
        log_file.write("==========================================================\n")
        
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
    log_file.write("==========================================================\n")
    log_file.write(f"{msg_id} | {email_date} \n")
    log_file.write("==========================================================\n")
    log_file.write(f"Parsing Bullets... \n")
    log_file.write("==========================================================\n")

    hr_tag = None
    last_row_id = 0
    rows_affected = 0
    bullet_content = []

    soup = BeautifulSoup(html_content, "html.parser")

    if soup.find('hr'):
        hr_tag = soup.find('hr')
    elif soup.find_all('div', role="separator"):
        separate_divs = soup.find_all('div', role="separator")
        for div in separate_divs:
            style = div.get("style", "")
            if "width:100%" in style and "font-size:1px" in style and "height:1px" in style:
                hr_tag = div
                break
    else:
        #parse_older_bullet_points(soup)
        log_file.write("This is an older version of 5-Bullet Friday \n")
        return -1

    try:
        last_row_id = insert_friday_email(connection, msg_id, email_date, subject, log_file)
        log_file.write(f"tff_5bullet_email record inserted with ID: {last_row_id} \n")
    except Exception as error:
        log_file.write("Insertion Failed for tff_5bullet_email !!!")
        log_file.write(f"{subject} | Error: {error}")

    log_file.write("----------------------------------------------------------------\n")

    # Finding and Traversing through all 'h2' tags (bullets) and getting it's content
    for element in soup.find_all('h2'):
        # Stopping at HR_TAG
        if hr_tag and hr_tag in element.find_all_previous():
            break

        heading_text = element.text.strip().replace("\u200b","")  #element.get_text(strip = True)

        paragraph_text = ""
        paragraph_content = []

        # Finding and Traversing through all the siblings of 'h2' tag and getting it's content
        for sibling in element.find_next_siblings():
            if sibling == hr_tag or sibling.name == 'h2':
                break
            if sibling.name == 'p':
                paragraph_content.append(str(sibling).replace("\u200b",""))
        
        paragraph_text = ''.join(paragraph_content)

        # Identify and remove style attributes from each paragraph tags to keep the styling neutral (after combining all paras)
        # Identify and remove tags from each paragraph to get the searchable text
        paragraph_text_stripped, paragraph_text_searchable= re.sub(r'style="[^"]*"', "", paragraph_text), re.sub(r'<[^>]*>', "", paragraph_text)
        log_file.write(f"{heading_text}: {len(paragraph_text)} | {len(paragraph_text_stripped)} | {len(paragraph_text_searchable)} \n")
        bullet_content.append((int(last_row_id), heading_text, paragraph_text_stripped, paragraph_text_searchable))
        log_file.write("----------------------------------------------------------------\n")
        
    log_file.write(f"Number of Bullets: {len(bullet_content)} \n")

    rows_affected = 0
    try:
        rows_affected = insert_email_bullets(connection, bullet_content, log_file)
        log_file.write(f"tff_bullets records inserted: {rows_affected} rows affected \n")
    except Exception as error:
        log_file.write("Insertion Failed for tff_bullets !!! \n")
        log_file.write(f"{rows_affected} | Error: {error} \n")
   
    log_file.write("=============================================================================================\n\n\n")
    return 0

if __name__ == "__main__":
    # Opens the file object for logging purpose
    CURR_DIR = os.path.dirname(os.path.realpath(__file__))
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")

    tff_5bullet_log_file = None
    log_file = f"{str(CURR_DIR)}/5BulletDBLog_{current_datetime}.txt"
    if not os.path.exists(log_file):
        tff_5bullet_log_file = open(log_file, "w", encoding="utf-8")
    else:
        tff_5bullet_log_file = open(log_file, "w", encoding="utf-8")

    # Calculate execution time - START
    start = time.time()

    SKIP_THRESHOLD = 0
    counter = 0
    LIMIT_EMAILS = 250 #200
    old_version_email_detector = 0
    LOCAL_TIMEZONE = pytz.timezone("America/New_York")

    # Access Gmail API Service and authenticate the user
    service = gmail_authenticate(tff_5bullet_log_file)

    # Initializing parameters for Gmail API
    USER_ID = "me"
    LABEL_IDS = ['CATEGORY_UPDATES', 'INBOX']
    QUERY = 'from: Tim Ferriss <tim@fourhourbody.com>'
    MAX_RESULTS = 50 #15
    next_page_token = None
    
    # Check if db is available to connect and exit in case of failure
    tff_5bullet_log_file.write("==========================================================\n")
    tff_5bullet_log_file.write("Connecting to Database...\n")
    tff_5bullet_log_file.write("==========================================================\n")
    if not db_connect(tff_5bullet_log_file):
        tff_5bullet_log_file.write("Db Connection Failed !!!\n")
        tff_5bullet_log_file.close()
        exit()
    else:
        connection = db_connect(tff_5bullet_log_file)
        tff_5bullet_log_file.write("DB Connection Successful !!!\n")

    # The Email fetching process starts here
    tff_5bullet_log_file.write("==========================================================\n")
    tff_5bullet_log_file.write("Starting to Get Emails...\n")
    tff_5bullet_log_file.write("==========================================================\n")
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
            if message:
                counter, old_version_email_detector = process_email(connection, message, counter, SKIP_THRESHOLD, tff_5bullet_log_file, LOCAL_TIMEZONE)
                if counter >= SKIP_THRESHOLD + LIMIT_EMAILS or old_version_email_detector < 0: #5
                    break

        # Check if there is next page token for next batch of emails and 
        # the number of emails required to be fetched are still remaining
        if old_version_email_detector == 0 and counter <= LIMIT_EMAILS: #and counter <= skip_threshold
            next_page_token = results.get("nextPageToken")
        else:
            next_page_token = None

        # If no next page token found, then all emails are fetched and task is completed
        if not next_page_token:
            tff_5bullet_log_file.write("\n\n\n==========================================================\n")
            tff_5bullet_log_file.write("End: All emails have been fetched \n")
            break
        else:
            # Wait for 1 second after each API batch call
            time.sleep(1)
    
    # Calculate execution time - STOP
    end = time.time()
    
    tff_5bullet_log_file.write("==========================================================\n")
    tff_5bullet_log_file.write(f"\n\nTotal emails found: {counter} \n")
    tff_5bullet_log_file.write(f"Total execution time: {end - start} \n")
    
    # Close the file if open
    if not tff_5bullet_log_file.closed:
        tff_5bullet_log_file.close()
    
    # Close the db connection if open
    if connection and connection.is_connected():
        connection.close()