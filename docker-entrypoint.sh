#!/bin/sh
set -eu

# Create default user/group
APP_USER="${APP_USER:-tvguide}"
APP_GROUP="${APP_GROUP:-tvguide}"
# Set default user/group ID's
PUID="${PUID:-1000}"
PGID="${PGID:-1000}"
# Set default cron variables
CRON_SCHEDULE="${CRON_SCHEDULE:-0 1 * * *}"
CRON_PATH="${CRON_PATH:-/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin}"

# create user and group if they don't exist
if ! getent group "$APP_GROUP" >/dev/null 2>&1; then
	addgroup --gid "$PGID" "$APP_GROUP"
fi

if ! getent passwd "$APP_USER" >/dev/null 2>&1; then
	adduser --disabled-password --gecos "" --uid "$PUID" --ingroup "$APP_GROUP" \
		--home /home/"$APP_USER" --shell /bin/sh "$APP_USER"
fi

# Set ownership of /app directory to user/group
chown -R "$APP_USER":"$APP_GROUP" /app

# Print environment variables to file and set permissions
printenv > /app/environment
chmod 0644 /app/environment

# Create cron job to run the script every day at 1am UTC
# Source the environment file so cron and thus the script can access the environment variables
cat <<EOF >/etc/cron.d/tvguide-cron
SHELL=/bin/sh
PATH=$CRON_PATH

$CRON_SCHEDULE $APP_USER set -a; . /app/environment; set +a; /app/run_tvguide.sh
EOF
chmod 0644 /etc/cron.d/tvguide-cron
crontab -r >/dev/null 2>&1 || true

# Start cron in foreground mode
exec cron -f
