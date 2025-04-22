# TFF Bullets Email Automation

This project automates the process of scraping and collecting TFF bullet emails from your inbox for archival purposes. It saves these emails in a database (MySQL in this case), which is then accessed by a [Web Application](https://github.com/vatsal2297/Tim-Ferriss-Bullet-Friday-Archive) to display them on the user interface. It streamlines the workflow by integrating data collection, formatting, and loading email data into the database as part of a single automated pipeline.

---

## Requirements

- Python 3.x
- Required libraries (see `requirements.txt`)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/tff_bullets_email_automation.git
    ```
2. Navigate to the project directory:
    ```bash
    cd tff_bullets_email_automation
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration (to create your own Archive)

1. [Enable Gmail API](https://thepythoncode.com/article/use-gmail-api-in-python) for your Gmail account.
2. Replace `credentials.json` file's content with your own `credentials.json` file which you download from Step-1.
3. When you run the program for the first time, the token.pickle file will be automatically generated using `authentication.py`.
4. Create DB and two tables required for TFF Emails data using schema mentioned in `BulletFriday.sql`.
5. Change the credentials for your Database in the `dbconnection.py` according to your Database configuration.

## About the Scripts

**`TFFBulletsAUTO.py`** - Script for setting up automation. By setting this up in Windows Task Scheduler (or any other automation software), the emails data will be scraped, formatted and loaded in the database as per schedule. An ideal setup will be weekly on Friday EOD or Saturday Morning (as the emails are received on each Friday).

**`TFFBulletsNEW.py`** - Script for dumping all the emails in the database with the new format of bullets (The Bullets and overall content format was modernized for 5-Bullet Friday recently).

**`TFFBulletsOLD.py`** - Script for dumping all the emails in the database with old format of bullets. (*In Progress*)

**NOTE:** *The scripts for Dumping New and Old format emails are different because there are different conditions based on which the emails are scraped for both formats. My plan is to combine both scripts into one after I am done with completing `TFFBulletsOLD.py`*

**NOTE:** *The script log will be generated for `TFFBulletsAUTO.py`, `TFFBulletsNEW.py` and `TFFBulletsOLD.py` in the files `5BulletDBAutoLog_*.txt`, `5BulletDBLog_*.txt` and `5BulletDBOldLog_*.txt` respectively*

## RESOURCES

**1) Gmail API with Python / Google API Client Library for Python docs**
- [Send mails with Gmail API - *MailTrap*](https://mailtrap.io/blog/send-emails-with-gmail-api/)
- [Gmail API QuickStart with Python - *Google Devs*](https://developers.google.com/gmail/api/quickstart/python)
- [Gmail API Python client - *GitHub*](https://github.com/googleapis/google-api-python-client)
- [Gmail API Python client docs - *GitHub*](https://github.com/googleapis/google-api-python-client/tree/main/docs)

**2) Gmail API Structure/Documentation**
- [Gmail API messages list structure - *Google Devs*](https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html#list)

**3) Gmail API Overview & Reference**
- [Gmail API Guide - *Google Devs*](https://developers.google.com/gmail/api/guides)
- [Gmail API Reference - *Google Devs*](https://developers.google.com/gmail/api/reference/rest)
- [Gmail API Reference | users.messages - *Google Devs*](https://developers.google.com/gmail/api/reference/rest/v1/users.messages)
- [Quotas for Google Services - *Google Devs*](https://developers.google.com/apps-script/guides/services/quotas#:~:text=Email%20recipients%20per,1%2C500*%20%2F%20day)
- [Gmail API Guide for handling errors - *Google Devs*](https://developers.google.com/gmail/api/guides/handle-errors)

**4) Gmail API in Python - Developer Guide**
- [How to use Gmail API with Python - *ThePythonCode*](https://thepythoncode.com/article/use-gmail-api-in-python)
- [How to read emails from gmail using Gmail API in python - *Medium*](https://medium.com/@preetipriyanka24/how-to-read-emails-from-gmail-using-gmail-api-in-python-20f7d9d09ae9)

**5) Google API dashboard**
- [Gmail API Dashboard](https://console.developers.google.com/apis/dashboard)

**6) Oauth2 Authorization doc**
- [Protocols of Google OAuth2 - *Google Identity*](https://developers.google.com/identity/protocols/oauth2/)

**7) Python**
- [Strings in Python - *Google For Education*](https://developers.google.com/edu/python/strings)
- [Virtual Environment for Python - *Python Land*](https://python.land/virtual-environments/virtualenv)

**8) BeautifulSoup**
- [find_all_previous() & find_previous() function in BeautifulSoup using python - *Crummy*](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all-previous-and-find-previous)
- [Extract all 'p' tags between and after 'h' tags - *Reddit*](https://www.reddit.com/r/webscraping/comments/xgrh2o/extract_all_p_tags_between_after_h_tags/)
- Search: filtering html elements based on contents inside it beautifulsoup python
    - [Extract InnerHTML with BeautifulSoup - *DNMTechs*](https://dnmtechs.com/extracting-innerhtml-with-beautifulsoup-in-python-3/)
    - [Beautifulsoup search by text inside a tag - *GeeksForGeeks*](https://www.geeksforgeeks.org/beautifulsoup-search-by-text-inside-a-tag/)

**9) MySQL**
- [Attempted to edit MySQL service config and getting Access Denied - *ServerFault*](https://serverfault.com/questions/240246/attempted-to-edit-mysql-service-config-and-getting-access-denied)
- [Connector Python example - *MySQL Dev*](https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html)
- [How do I determine RAM for my MySQL server - *Quora*](https://www.quora.com/How-do-I-determine-how-much-RAM-I-need-for-a-MySQL-server-Our-database-is-big-20-GB-dump-file-and-our-current-server-has-64-GB-of-memory-of-which-58-GB-is-allocated-to-InnoDB-buffer-pool-which-is-all-used-Should-I)
- [I have a MySQL db that is close to a GB - *Reddit*](https://www.reddit.com/r/Database/comments/15e1y2z/i_have_a_mysql_database_that_is_close_to_a/)
- [How Do I connect to a MySQL db in python - *StackOverflow*](https://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python)
- [peewee, A lightweight ORM for Python Devs - *Medium*](https://medium.com/@HeCanThink/peewee-a-lightweight-orm-for-python-developers-953e84c66cc4)
- [Python MySQL - *RealPython*](https://realpython.com/python-mysql/)
- [MySQL ALTER TABLE options - *MySQL Dev*](https://dev.mysql.com/doc/refman/8.0/en/alter-table.html)
- [Run Database Connections over multiple files - *StackOverflow*](https://stackoverflow.com/questions/65995708/run-database-connection-over-multiple-files)
- [Order results by time regardless of date - *Tejas Shah Blog*](https://tejasnshah.wordpress.com/2009/03/24/sql-server-select-result-order-by-time/)

**10) Postman Testing**
- [How to access Google APIs using oauth in Postman - *Postman Blog*](https://blog.postman.com/how-to-access-google-apis-using-oauth-in-postman/)
- [Gmail Users List Sample - *Postman*](https://www.postman.com/api-evangelist/google/request/esog3c2/gmail-users-messages-list?tab=headers)
- [How to OAuth 2.0 Authorization with Postman | Generate Google Access Token in Postman Step by Step - *YouTube*](https://www.youtube.com/watch?v=zHfR96IZECQ)
- [How to use variables in Postman - *YouTube*](https://www.youtube.com/watch?v=BKLC-_C9fxE)
- [Loop request based on data from response in Postman - *YouTube*](https://www.youtube.com/watch?v=4wuvgX-egdc)
- [Gmail List messages Sample - *Postman*](https://www.postman.com/postman/google-api-workspace/request/8zpb3is/list-messages?tab=params)

**11) Epoch time**
- [Convert epoch time with milliseconds into datetime - *StackOverflow*](https://stackoverflow.com/questions/21787496/converting-epoch-time-with-milliseconds-to-datetime)
- [Epoch Convertor](https://www.epochconverter.com/)

**12) RegEx**
- [Advanced text processing using RegEx - *Medium*](https://medium.com/@monicanogueras/15-examples-for-advanced-text-processing-using-regex-48223adc720d)
- [RegEx QuickStart - *RexEgg*](https://www.rexegg.com/regex-quickstart.php)
- [RegEx Testing - *RegEx 101*](https://regex101.com/)
- [How to exclude a character from a regex group - *StackOverFlow*](https://stackoverflow.com/questions/4108561/how-to-exclude-a-character-from-a-regex-group)
- Search: comparing string against multiple regular expression re.search python
    - [Match a line with multiple RegEx using Python - *StackOverFlow*](https://stackoverflow.com/questions/8888567/match-a-line-with-multiple-regex-using-python)

**13) Terminal Scrollback VSCode**
- [Increase the number of lines of terminal shown in VSCode - *BobbyHadz*](https://bobbyhadz.com/blog/vscode-increase-number-of-lines-shown-in-terminal)

**14) Correct way to fetch emails for a given query**
- Search: gmail api is fetching previous emails data and mixing and matching with previous email data while fetching emails using beautiful soup and python
    - [Correct way to fetch all emails for a given query - *StackOverflow*](https://stackoverflow.com/questions/38963771/gmail-api-correct-way-to-fetch-all-emails-for-a-given-query)

**15) MarkDown Guide**
- Search - mark down language cheatsheet
    - [MarkDown CheatSheet - *MarkDownGuide*](https://www.markdownguide.org/cheat-sheet/)

**16) VSCode** 
- [Change Encoding for files in VSCode - *Kinda Code*](https://www.kindacode.com/article/how-to-change-file-encoding-in-vs-code#change-encoding-for-a-single-file)

**17) Logging**
- Search: how to effectively make a log file what to log
    - [Logging Best Practices - *BetterStack*](https://betterstack.com/community/guides/logging/logging-best-practices/)
    - [Some Logging Framework Recommendations - *BetterStack*](https://betterstack.com/community/guides/logging/logging-framework/#some-logging-framework-recommendations)
    - [A Comprehensive guide to logging in Python - *BetterStack*](https://betterstack.com/community/guides/logging/how-to-start-logging-with-python/)

**18) Windows Task Scheduler**
- Search: how to specify venv for python executable for Windows Task Scheduler
    - [Run a Python script in Virtual Env from Windows Task Scheduler - *StackOverFlow*](https://stackoverflow.com/questions/34622514/run-a-python-script-in-virtual-environment-from-windows-task-scheduler)
- Search: how to run windows task scheduler python script silently
    - [pythonw.exe Tutorial - *Coders Legacy*](https://coderslegacy.com/pythonw-exe-tutorial/)
- Search: shutdown computer automatically after the windows task script is ran successfully
    - [How do I auto shutdown my PC after a Task completion - *Microsoft Forum*](https://answers.microsoft.com/en-us/windows/forum/all/how-do-i-auto-shutdown-my-pc-after-a-programtask/e0471b1b-e3c4-473b-a968-80e2964cda48)

**19) Gmail API Error**
- Search: gmail api error handling python
    - [How to manage Google API errors in Python - *StackOverFlow*](https://stackoverflow.com/questions/23945784/how-to-manage-google-api-errors-in-python)
    - [Troubleshooting - *Google*](https://cloud.google.com/apis/docs/troubleshooting)
    - [Google Errors - *Google AIP*](https://google.aip.dev/193)
    - [Google Standard methods > List - *Google AIP*](https://google.aip.dev/132)
    - [Status Codes and their use in gRPC - *GitHub*](https://github.com/grpc/grpc/blob/master/doc/statuscodes.md)
    - [Gmail API Scopes - *Google Dev*](https://developers.google.com/gmail/api/auth/scopes)
    - [Python QuickStart - *Google Dev*](https://developers.google.com/gmail/api/quickstart/python)
    - [Gmail API returns unspecified error at random moments - *StackOverFlow*](https://stackoverflow.com/questions/31109540/gmail-api-returns-unspeficied-error-at-random-moments)

## TESTS

1. Total emails found: `60`; Total execution time: `2186.6479198932648` [before putting sender's email as an initial filter]
2. Total emails found: `54`; Total execution time: `35.785658836364746` [after putting sender's email as an initial filter]
3. Email data (latest format, old format remains) successfully inserted (143 emails inserted) on 2024-12-12 16:49
4. Email Insertion with Automation Successfully implemented 
  a. Successfully programmed Automation Script
  b. Setup Python Script to Win Task Scheduler 
  c. First Successful Automation Run on 2025-01-31 6:00 PM
