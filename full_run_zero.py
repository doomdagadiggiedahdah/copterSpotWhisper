import re
from pathlib import Path
import whisper
import shutil
import sqlite3
from datetime import datetime

audio_path = Path("./audio/2022/10/zero")

def init_database():
    conn = sqlite3.connect('atc_transcriptions_2022_10_0.db')
    c = conn.cursor()
    
    # Create tables if they don't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS transcriptions (
            file_path TEXT PRIMARY KEY,
            transcription TEXT,
            keywords TEXT,
            processed_date TIMESTAMP,
            copied_to_output BOOLEAN
        )
    ''')
    
    conn.commit()
    return conn

def is_file_processed(conn, file_path):
    c = conn.cursor()
    c.execute('SELECT 1 FROM transcriptions WHERE file_path = ?', (str(file_path),))
    return c.fetchone() is not None

def save_to_database(conn, file_path, transcription, keywords, copied_to_output):
    c = conn.cursor()
    c.execute('''
        INSERT INTO transcriptions 
        (file_path, transcription, keywords, processed_date, copied_to_output)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        str(file_path),
        transcription,
        ','.join(keywords) if keywords else '',
        datetime.now(),
        copied_to_output
    ))
    conn.commit()

def check_keywords(text):
    # List of multi-word phrases and keywords (ensure commas are correct)
    phrases = [
        "close call", "near miss", "go around",
        "going around", "ra", "resolution advisory",
        "ta", "traffic alert", "immediately",
        "traffic advisory", "clear of conflict",
        "cc", "descend"
    ]
    
    # Single-word abbreviations that need exact matching
    exact_words = {"ac", "ra", "ta", "cc"}
    
    # Convert text to lowercase for case-insensitive comparison
    text_lower = text.lower()
    
    found_keywords = []

    # Use regex to ensure whole-word matching for all phrases
    for phrase in phrases:
        # re.escape makes sure any special characters in the phrase are handled correctly.
        pattern = r'\b' + re.escape(phrase) + r'\b'
        if re.search(pattern, text_lower):
            found_keywords.append(phrase)
    
    # If you still need to check exact_words separately (though many are already in phrases),
    # you can do so with a similar approach:
    for word in exact_words:
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, text_lower) and word not in found_keywords:
            found_keywords.append(word)
    
    return found_keywords

def main():
    # Setup paths
    input_dir = audio_path
    output_dir = Path("./close_calls")
    output_dir.mkdir(exist_ok=True)
    
    # Initialize database connection
    conn = init_database()
    
    # Load model once
    print("Loading model...")
    model = whisper.load_model("large")
    
    # Process all MP3 files
    total_files = 0
    processed_files = 0
    
    for audio_file in input_dir.rglob("*.mp3"):
        total_files += 1
        print(f"\nProcessing: {audio_file}")
        
        # Check if file has already been processed
        if is_file_processed(conn, audio_file):
            print(f"Skipping {audio_file} - already processed")
            skipped_files += 1
            continue
        
        try:
            # Transcribe
            prompt = """El Monte tower with runways 1 and 19 on frequency 121.2. Traffic Alert, Cessna Three-Four Juliett, 12'o clock, 1 mile advise you turn left and climb immediately. """
            prompt += """ROOK01 climb and maintain flight level two zero zero. Report (advise) when formation join-up is complete"""
            prompt += """BAMA21 have BAMA23 squawk 5544, descend and maintain flight level one-niner-zero and change to my frequency"""
            prompt += """DMHS23 Radar contact (position if required). Cleared to SSC via direct. Descend and maintain flight level one-niner-zero."""
            prompt += """N5871S requesting flight break-up with N731K. N731K is changing destination to PHL."""

            result = model.transcribe(str(audio_file), language="en", prompt=prompt)
            
            # Check for keywords
            found_keywords = check_keywords(result["text"])
            
            # Flag for whether file was copied to output
            copied_to_output = False
            
            if found_keywords:
                print(f"Found keywords: {found_keywords}")
                print(f"Text: {result['text']}")
                
                # Copy file to output directory
                shutil.copy2(audio_file, output_dir / audio_file.name)
                copied_to_output = True
            
            # Save to database
            save_to_database(conn, audio_file, result["text"], found_keywords, copied_to_output)
            processed_files += 1
            
        except Exception as e:
            print(f"Error processing {audio_file}: {str(e)}")
        
    print(f"\nFinished processing {total_files} total files")
    print(f"Successfully processed: {processed_files}")
    
    conn.close()

if __name__ == "__main__":
    main()

# ls audio/2022/10/ | head -n $(($(ls audio/2022/10/ | wc -l) / 2)) | xargs -I{} mv ./audio/2022/10/{} ./audio/2022/10/zero/
# mkdir -p audio/2022/10/zero audio/2022/10/one