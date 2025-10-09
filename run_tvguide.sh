#!/bin/sh
python /app/HD_to_xmlTV.py --host "$HOST" --filename "$FILENAME" >> /app/output/cron.log 2>&1
echo "TV guide updated at $(date)" >> /app/output/cron.log