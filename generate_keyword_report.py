import sqlite3
import os

files_to_find = os.listdir('./close_calls/')

def full(db_name):
    # Map text input to database filenames
    try:
        conn = sqlite3.connect(db_name)  # Connect to the correct database
        c = conn.cursor()

        # Count total rows in 'transcriptions' table
        c.execute('SELECT COUNT(*) FROM transcriptions')
        total = c.fetchone()[0]
        print(f"Total rows in {db_name}: {total}")

        # Count rows where 'keywords' column is not empty
        c.execute('SELECT COUNT(*) FROM transcriptions WHERE keywords != ""')
        with_keywords = c.fetchone()[0]
        print(f"Rows with keywords in {db_name}: {with_keywords}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()  # Ensure connection is closed

def query_database(db_file, filename):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    c.execute('''
        SELECT file_path, transcription, keywords, processed_date 
        FROM transcriptions 
        WHERE file_path LIKE ?
    ''', (f'%{filename}%',))
    
    result = c.fetchone()
    conn.close()
    return result

full('zero')

# Check both databases for each file
for filename in files_to_find:
    print(f"\nLooking for: {filename}")
    found = False
    
    # Check first database
    result = query_database('atc_transcriptions_2022_10_0.db', filename)
    if result:
        print(f"Keywords: {result[2]}")
        print(f"Text: {result[1][:200]}...")  # First 200 chars
        found = True
        
    # Check second database
    result = query_database('atc_transcriptions_2022_10_1.db', filename)
    if result:
        print(f"Keywords: {result[2]}")
        print(f"Text: {result[1][:200]}...")  # First 200 chars
        found = True
        
    if not found:
        print("File not found in either database")
