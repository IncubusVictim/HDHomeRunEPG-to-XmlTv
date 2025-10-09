FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/* \
	&& pip install --no-cache-dir argparse requests

COPY HDHomeRunEPG_To_XmlTv.py ./
COPY run_tvguide.sh ./

ENV HOST=localhost
ENV FILENAME=output.xml
# Add crontab entry to run the script every day at 1am
RUN chmod +x /app/run_tvguide.sh

RUN echo "0 1 * * * /app/run_tvguide.sh" > /etc/cron.d/tvguide-cron
RUN chmod 0644 /etc/cron.d/tvguide-cron && crontab /etc/cron.d/tvguide-cron

CMD ["cron", "-f"]
