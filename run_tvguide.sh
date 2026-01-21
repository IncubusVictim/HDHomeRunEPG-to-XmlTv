#!/bin/sh
python /app/HDHomeRunEPG_To_XmlTv.py >> /app/output/cron.log 2>&1
echo "TV guide updated at $(date)" >> /app/output/cron.log