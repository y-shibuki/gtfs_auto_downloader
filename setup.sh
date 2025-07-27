#!/bin/bash

# GTFS RT Crawler Systemd Timer Setup Script
# Usage: ./setup.sh [crawler|downloader]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
SERVICE_USER="$USER"

log() {
    local level="$1"
    local message="$2"
    echo "[$level] $message"
}

usage() {
    log "INFO" "Usage: $0 [crawler|downloader]"
    log "INFO" "Commands:"
    log "INFO" "  crawler     Setup crawler services and timers"
    log "INFO" "  downloader  Setup downloader service and timer"
    exit 1
}

create_service_file() {
    local service_name="$1"
    local description="$2"
    local exec_command="$3"
    
    local service_file="/etc/systemd/system/${service_name}.service"

    log "INFO" "Creating service file: $service_file"

    sudo tee "$service_file" <<EOF > /dev/null
[Unit]
Description=$description

[Service]
Type=simple
User=$SERVICE_USER
ExecStart=$exec_command

[Install]
WantedBy=multi-user.target
EOF
    
    log "INFO" "Service file created: $service_file"
}

create_timer_file() {
    local timer_name="$1"
    local description="$2"
    local on_calendar="$3"
    
    local timer_file="/etc/systemd/system/${timer_name}.timer"

    log "INFO" "Creating timer file: $timer_file"

    sudo tee "$timer_file" <<EOF > /dev/null
[Unit]
Description=$description
Requires=${timer_name}.service

[Timer]
OnCalendar=$on_calendar

[Install]
WantedBy=timers.target
EOF
    
    log "INFO" "Timer file created: $timer_file"
}

setup_crawler_services() {
    log "INFO" "Setting up crawler services..."
    
    # Create services for different intervals
    create_service_file "gtfs-crawler-20s" \
        "GTFS RT Crawler (20 second interval)" \
        "task -d $PROJECT_DIR crawler:20s"
    create_timer_file "gtfs-crawler-20s" \
        "GTFS RT Crawler Timer (20 second interval)" \
        "*:*:0/20"
    
    create_service_file "gtfs-crawler-60s" \
        "GTFS RT Crawler (60 second interval)" \
        "task -d $PROJECT_DIR crawler:60s"
    create_timer_file "gtfs-crawler-60s" \
        "GTFS RT Crawler Timer (60 second interval)" \
        "*:*:0/60"
    
    create_service_file "gtfs-crawler-120s" \
        "GTFS RT Crawler (120 second interval)" \
        "task -d $PROJECT_DIR crawler:120s"
    create_timer_file "gtfs-crawler-120s" \
        "GTFS RT Crawler Timer (120 second interval)" \
        "*:*:0/120"
    
    create_service_file "gtfs-crawler-1day" \
        "GTFS RT Crawler (1 day interval)" \
        "task -d $PROJECT_DIR crawler:1day"
    create_timer_file "gtfs-crawler-1day" \
        "GTFS RT Crawler Timer (1 day interval)" \
        "daily"
    
    # Create compress service
    create_service_file "gtfs-compress" \
        "GTFS Data Compression" \
        "task -d $PROJECT_DIR compress"
    create_timer_file "gtfs-compress" \
        "GTFS Data Compression Timer" \
        "daily"
    
    log "INFO" "Crawler services and timers created successfully."
    log "INFO" "Services and timers created:
  - gtfs-crawler-20s.service / gtfs-crawler-20s.timer
  - gtfs-crawler-60s.service / gtfs-crawler-60s.timer
  - gtfs-crawler-120s.service / gtfs-crawler-120s.timer
  - gtfs-crawler-1day.service / gtfs-crawler-1day.timer
  - gtfs-compress.service / gtfs-compress.timer"
}

setup_downloader_service() {
    log "INFO" "Setting up downloader service..."
    
    create_service_file "gtfs-downloader" \
        "GTFS Data Downloader" \
        "task -d $PROJECT_DIR download"
    create_timer_file "gtfs-downloader" \
        "GTFS Data Downloader Timer" \
        "daily"
    
    log "INFO" "Downloader service and timer created successfully."
    log "INFO" "Service and timer created:
  - gtfs-downloader.service / gtfs-downloader.timer"
}


if [ $# -ne 1 ]; then
    log "ERROR" "Invalid number of arguments."
    usage
fi

case "$1" in
    "crawler")
        setup_crawler_services
        sudo systemctl daemon-reload
        log "INFO" "Crawler setup completed successfully."
        log "INFO" "To enable and start timers, run:
  sudo systemctl enable --now gtfs-crawler-20s.timer
  sudo systemctl enable --now gtfs-crawler-60s.timer
  sudo systemctl enable --now gtfs-crawler-120s.timer
  sudo systemctl enable --now gtfs-crawler-1day.timer
  sudo systemctl enable --now gtfs-compress.timer"
        log "INFO" "Or use: task systemd:enable:all"
        ;;
    "downloader")
        setup_downloader_service
        sudo systemctl daemon-reload
        log "INFO" "Downloader setup completed successfully."
        log "INFO" "To enable and start timer, run:
  sudo systemctl enable --now gtfs-downloader.timer"
        ;;
    *)
        log "ERROR" "Invalid argument: $1"
        usage
        ;;
esac