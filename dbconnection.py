from mysql.connector import connect, Error, pooling

# Create Database connection
def db_connect(log_file):
    
    try:
        with connect( 
            connection_timeout = 60, #25
            user = "root", 
            password = "************", 
            host = "127.0.0.1", 
            database = "nlarchive") as connection:
                if connection.is_connected():
                    return connection
    except Error as e:
        log_file.write(f"Error: {e} \n")
        return None
    

# Insert an email   
def insert_friday_email(connection, msg_id, email_date, subject, log_file):
    cursor = None
    try:
        insert_friday_email_query = """
            INSERT INTO tff_5bullet_emails (email_message_id, email_date, email_title)
            VALUES (%s, %s, %s)
        """
        insert_friday_email_data = (msg_id, email_date, subject)

        if not connection.is_connected():
            log_file.write(f"||| Reconnecting to database... ||| Email Insertion \n")
            connection.reconnect()

        with connection.cursor() as cursor:
            cursor.execute(insert_friday_email_query, insert_friday_email_data)
            connection.commit()
            return cursor.lastrowid
    except Error as e:
        log_file.write(f"Error: {e} \n")
        if connection and connection.is_connected():
            connection.rollback()
            log_file.write("Transaction has been rollbacked \n\n")
        return None
    finally:
        if cursor:
            cursor.close()
    
def insert_email_bullets(connection, bullet_content, log_file):
    cursor = None    
    try:
        insert_friday_bullets_query = """
            INSERT INTO tff_bullets (tff_email_id, bullet_heading, bullet_content, searchable_bullet_content)
            VALUES (%s, %s, %s, %s)
        """

        if not connection.is_connected():
            log_file.write(f"||| Reconnecting to database... ||| Email Bullets Insertion \n")
            connection.reconnect()

        with connection.cursor() as cursor:
            cursor.executemany(insert_friday_bullets_query, bullet_content)
            connection.commit()
            return cursor.rowcount
    except Error as e:
        log_file.write(f"Error: {e} \n")
        if connection and connection.is_connected():
            connection.rollback()
            log_file.write("Transaction has been rollbacked \n\n")
        return None
    finally:
        if cursor:
            cursor.close()

def fetch_latest_friday_email(connection, log_file):
    cursor = None
    last_friday_email = []
    try:
        fetch_latest_friday_email_query = """
            SELECT email_message_id, email_date, email_title
            FROM tff_5bullet_emails 
            WHERE email_date = (
	            SELECT MAX(email_date) 
                FROM tff_5bullet_emails
            );
        """

        if not connection.is_connected():
            log_file.write(f"||| Reconnecting to database... ||| Latest Email Fetch \n")
            connection.reconnect()
        
        with connection.cursor() as cursor:
            cursor.execute(fetch_latest_friday_email_query)
            last_friday_email = cursor.fetchall()
            return last_friday_email
    except Error as e:
        log_file.write(f"Error while fetching Last Friday Email: {e} \n")
        return None
    finally:
        if cursor:
            cursor.close()

def fetch_email_bullets(email_id):
    pass

