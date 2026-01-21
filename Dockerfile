FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/* \
	&& pip install --no-cache-dir -r requirements.txt

COPY HDHomeRunEPG_To_XmlTv.py ./
COPY run_tvguide.sh ./
COPY docker-entrypoint.sh ./

RUN chmod +x /app/run_tvguide.sh /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]
