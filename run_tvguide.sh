#!/bin/sh
/usr/local/bin/python /app/HDHomeRunEPG_To_XmlTv.py --host "$HOST" --filename "$FILENAME" --days "$DAYS" >> /app/output/cron.log 2>&1
echo "TV guide updated at $(date)" >> /app/output/cron.log