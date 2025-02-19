#!/bin/bash

echo "one worker"
time python Dispatch_1.py 

python cat_db.py

rm combined_results.db worker_0.db worker_1.db

echo "two worker" 
time python Dispatch.py 
