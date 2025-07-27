#!/bin/bash

# Systemd Timer Examples for GTFS RT Crawler
# This file contains examples of timer configurations

echo "Timer configuration examples:"
echo ""
echo "Example timer files that should be created in /etc/systemd/system/:"
echo ""

cat << 'EOF'
# gtfs-crawler-20s.timer
[Unit]
Description=Run GTFS Crawler every 20 seconds
Requires=gtfs-crawler-20s.service

[Timer]
OnBootSec=30sec
OnUnitActiveSec=20sec
AccuracySec=1sec

[Install]
WantedBy=timers.target

# gtfs-crawler-60s.timer
[Unit]
Description=Run GTFS Crawler every 60 seconds
Requires=gtfs-crawler-60s.service

[Timer]
OnBootSec=30sec
OnUnitActiveSec=60sec
AccuracySec=1sec

[Install]
WantedBy=timers.target

# gtfs-crawler-120s.timer
[Unit]
Description=Run GTFS Crawler every 120 seconds
Requires=gtfs-crawler-120s.service

[Timer]
OnBootSec=30sec
OnUnitActiveSec=120sec
AccuracySec=1sec

[Install]
WantedBy=timers.target

# gtfs-crawler-1day.timer
[Unit]
Description=Run GTFS Crawler once per day
Requires=gtfs-crawler-1day.service

[Timer]
OnBootSec=5min
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target

# gtfs-compress.timer
[Unit]
Description=Compress GTFS data daily
Requires=gtfs-compress.service

[Timer]
OnBootSec=10min
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target

# gtfs-downloader.timer
[Unit]
Description=Download GTFS data daily
Requires=gtfs-downloader.service

[Timer]
OnBootSec=15min
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
EOF

echo ""
echo "To enable and start a timer:"
echo "sudo systemctl enable --now gtfs-crawler-20s.timer"
echo ""
echo "To check timer status:"
echo "sudo systemctl list-timers --all"
echo ""
echo "To check service logs:"
echo "sudo journalctl -u gtfs-crawler-20s.service -f"
