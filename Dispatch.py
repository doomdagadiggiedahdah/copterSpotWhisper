from pathlib import Path
from Worker import Worker
import sqlite3
from typing import List
import time
import math
import torch.multiprocessing as mp
from multiprocessing import Process

class Dispatcher:
    def __init__(self, 
                 num_workers: int,
                 audio_input_dir: Path,
                 audio_keyword_dir: Path):
        self.num_workers = num_workers
        self.audio_input_dir = audio_input_dir
        self.audio_keyword_dir = audio_keyword_dir
        self.workers: List[Worker] = []

    def initialize_workers(self):
        self.workers = [
            (i, self.audio_input_dir, self.audio_keyword_dir / f'worker_{i}')
            for i in range(self.num_workers)
        ]

    def distribute_work(self):
        """Distribute audio files among workers."""
        audio_files = list(self.audio_input_dir.rglob("*.mp3"))
        files_per_worker = math.ceil(len(audio_files) / self.num_workers)
        return audio_files, files_per_worker

    def combine_databases(self, final_db_path: str = 'combined_results.db'):
        with sqlite3.connect(final_db_path) as final_db:
            # Get schema from first worker's database
            first_worker_db = f'worker_0.db'
            with sqlite3.connect(first_worker_db) as worker_db:
                cursor = worker_db.cursor()
                cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
                schemas = cursor.fetchall()
                
                for schema in schemas:
                    if schema[0] is not None:
                        final_db.execute(schema[0])
            
            # Combine data from all workers
            for i in range(self.num_workers):
                worker_db_path = f'worker_{i}.db'
                with sqlite3.connect(worker_db_path) as worker_db:
                    cursor = worker_db.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    
                    for table in tables:
                        table_name = table[0]
                        if table_name.startswith('sqlite_'):
                            continue
                        cursor.execute(f"SELECT * FROM {table_name}")
                        rows = cursor.fetchall()
                        if rows:
                            cursor.execute(f"PRAGMA table_info({table_name})")
                            col_count = len(cursor.fetchall())
                            placeholders = ','.join(['?' for _ in range(col_count)])
                            final_db.executemany(
                                f"INSERT INTO {table_name} VALUES ({placeholders})",
                                rows
                            )
                    worker_db.commit()
            final_db.commit()
    
def worker_process(worker_params, files):
    worker_id, input_dir, output_dir = worker_params
    
    # Create and initialize worker
    worker = Worker(
        db_path=f'worker_{worker_id}.db',
        input_dir=input_dir,
        output_dir=output_dir
    )
    worker.initialize_db()
    worker.initialize_model()  # Model initialization happens here, inside the process
    
    # Process files
    for file in files:
        worker.process_file(file)
    worker.shutdown()

def main():
    dispatcher = Dispatcher(
        num_workers=2,
        audio_input_dir=Path("./test_worker_audio/audio_files"),
        audio_keyword_dir=Path("./test_worker_audio/test_close_calls")
    )

    print(f"Starting initialization at {time.strftime('%H:%M:%S')}")
    dispatcher.initialize_workers()
    
    # print(f"Distributing audio files at {time.strftime('%H:%M:%S')}")
    audio_files, files_per_worker = dispatcher.distribute_work()
    print(files_per_worker)
    
    processes = []
    try:
        # print(f"Starting processing at {time.strftime('%H:%M:%S')}")
        for i, worker_params in enumerate(dispatcher.workers):
            start_idx = i * files_per_worker
            end_idx = min((i + 1) * files_per_worker, len(audio_files))
            worker_files = audio_files[start_idx:end_idx]
            
            p = Process(target=worker_process, args=(worker_params, worker_files))
            processes.append(p)
            p.start()
  
    finally:
    #    print(f"Combining results at {time.strftime('%H:%M:%S')}")
       dispatcher.combine_databases()

if __name__ == "__main__":
    mp.set_start_method('spawn')
    main()

# rm worker_* combined_results.db