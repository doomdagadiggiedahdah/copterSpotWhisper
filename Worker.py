import re
from pathlib import Path
import whisper
import shutil
import sqlite3
from datetime import datetime
from typing import List, Dict, Tuple, Optional

class Worker:
    def __init__(self, 
                 db_path: str,
                 input_dir: Path,
                 output_dir: Path,
                 model_name: str = "large"):
        """
        Initialize the worker with necessary configurations.
        
        Args:
            db_path: Path to SQLite database
            input_dir: Directory containing input audio files
            output_dir: Directory for copied files matching criteria
            model_name: Whisper model to use
        """
        self.db_path = db_path
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.model_name = model_name
        self.model = None
        self.conn = None
        
        self.output_dir.mkdir(exist_ok=True)
        
        self.phrases = [
            "close call", "near miss", "go around",
            "going around", "ra", "resolution advisory",
            "ta", "traffic alert", "immediately",
            "traffic advisory", "clear of conflict",
            "cc", "descend"
        ]
        self.exact_words = {"ac", "ra", "ta", "cc"}

    def initialize_model(self) -> None:
        print("Loading Whisper model...")
        self.model = whisper.load_model(self.model_name)

    def initialize_db(self) -> None:
        """Initialize the database connection and load the Whisper model."""
        self.conn = self._init_database()

    def shutdown(self) -> None:
        """Clean up resources."""
        if self.conn:
            self.conn.close()

    def process_file(self, audio_file: Path) -> Tuple[bool, Optional[str]]:
        try:
            if self._is_file_processed(audio_file):
                return True, "Already processed"

            result = self._transcribe_audio(audio_file)
            found_keywords = self._check_keywords(result["text"])
            copied_to_output = False

            if found_keywords:
                print(f"Found keywords in {audio_file}: {found_keywords}")
                shutil.copy2(audio_file, self.output_dir / audio_file.name)
                copied_to_output = True
            
            self._save_to_database(audio_file, result["text"], found_keywords, copied_to_output)
            return True, None

        except Exception as e:
            return False, str(e)

    def _init_database(self) -> sqlite3.Connection:
        """Initialize SQLite database and create tables if needed."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
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

    def _is_file_processed(self, file_path: Path) -> bool:
        """Check if a file has already been processed."""
        c = self.conn.cursor()
        c.execute('SELECT 1 FROM transcriptions WHERE file_path = ?', (str(file_path),))
        return c.fetchone() is not None

    def _save_to_database(self, 
                         file_path: Path, 
                         transcription: str, 
                         keywords: List[str], 
                         copied_to_output: bool) -> None:
        """Save processing results to database."""
        c = self.conn.cursor()
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
        self.conn.commit()

    def _check_keywords(self, text: str) -> List[str]:
        """Check for presence of keywords and phrases in text."""
        text_lower = text.lower()
        found_keywords = []

        for phrase in self.phrases:
            pattern = r'\b' + re.escape(phrase) + r'\b'
            if re.search(pattern, text_lower):
                found_keywords.append(phrase)
        
        for word in self.exact_words:
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, text_lower) and word not in found_keywords:
                found_keywords.append(word)
        
        return found_keywords

    def _transcribe_audio(self, audio_file: Path) -> Dict:
        """Transcribe audio file using Whisper model."""
        prompt = """El Monte tower with runways 1 and 19 on frequency 121.2. Traffic Alert, Cessna Three-Four Juliett, 12'o clock, 1 mile advise you turn left and climb immediately. """
        prompt += """ROOK01 climb and maintain flight level two zero zero. Report (advise) when formation join-up is complete"""
        prompt += """BAMA21 have BAMA23 squawk 5544, descend and maintain flight level one-niner-zero and change to my frequency"""
        prompt += """DMHS23 Radar contact (position if required). Cleared to SSC via direct. Descend and maintain flight level one-niner-zero."""
        prompt += """N5871S requesting flight break-up with N731K. N731K is changing destination to PHL."""

        return self.model.transcribe(str(audio_file), language="en", prompt=prompt)