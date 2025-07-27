#!/bin/bash

# GTFS RT Crawler Systemd Timer Setup Script
# Usage: ./setup.sh [crawler|downloader]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
SERVICE_USER="$USER"

# 色付きの出力用
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

usage() {
    echo "Usage: $0 [crawler|downloader]"
    echo ""
    echo "Arguments:"
    echo "  crawler     Setup systemd timers for data crawling (20s, 60s, 120s, 1day intervals)"
    echo "  downloader  Setup systemd timer for downloading data from server"
    echo ""
    echo "Example:"
    echo "  $0 crawler     # Setup crawler timers"
    echo "  $0 downloader  # Setup downloader timer"
    exit 1
}

check_requirements() {
    print_info "Checking requirements..."
    
    # Check if systemctl is available
    if ! command -v systemctl &> /dev/null; then
        print_error "systemctl is not available. This script requires systemd."
        exit 1
    fi
    
    # Check if uv is installed
    if ! command -v uv &> /dev/null; then
        print_error "uv is not installed. Please install uv first."
        exit 1
    fi
    
    # Check if task is installed
    if ! command -v task &> /dev/null; then
        print_error "Task is not installed. Please install Task first."
        print_info "Installation: brew install go-task"
        print_info "Or see: https://taskfile.dev/installation/"
        exit 1
    fi
    
    # Get task executable path
    TASK_PATH=$(which task)
    if [ -z "$TASK_PATH" ]; then
        print_error "Task executable not found in PATH."
        exit 1
    fi
    
    # Check if project directory exists
    if [ ! -d "$PROJECT_DIR/app" ]; then
        print_error "Project directory structure is invalid. Expected app/ directory not found."
        exit 1
    fi
    
    # Check if Taskfile.yml exists
    if [ ! -f "$PROJECT_DIR/Taskfile.yml" ]; then
        print_error "Taskfile.yml not found in project directory."
        exit 1
    fi
    
    print_info "Requirements check passed."
}

create_service_file() {
    local service_name="$1"
    local description="$2"
    local exec_command="$3"
    
    local service_file="/etc/systemd/system/${service_name}.service"
    
    print_info "Creating service file: $service_file"
    
    sudo tee "$service_file" > /dev/null <<EOF
[Unit]
Description=$description
After=network.target

[Service]
Type=oneshot
User=$SERVICE_USER
WorkingDirectory=$PROJECT_DIR/app
Environment=PATH=/home/$SERVICE_USER/.local/bin:\$PATH
ExecStart=$exec_command
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    
    print_info "Service file created: $service_file"
}

setup_crawler_services() {
    print_info "Setting up crawler services..."
    
    # Create services for different intervals
    create_service_file "gtfs-crawler-20s" \
        "GTFS RT Crawler (20 second interval)" \
        "$TASK_PATH -d $PROJECT_DIR crawler:20s"
    
    create_service_file "gtfs-crawler-60s" \
        "GTFS RT Crawler (60 second interval)" \
        "$TASK_PATH -d $PROJECT_DIR crawler:60s"
    
    create_service_file "gtfs-crawler-120s" \
        "GTFS RT Crawler (120 second interval)" \
        "$TASK_PATH -d $PROJECT_DIR crawler:120s"
    
    create_service_file "gtfs-crawler-1day" \
        "GTFS RT Crawler (1 day interval)" \
        "$TASK_PATH -d $PROJECT_DIR crawler:1day"
    
    # Create compress service
    create_service_file "gtfs-compress" \
        "GTFS Data Compression" \
        "$TASK_PATH -d $PROJECT_DIR compress"
    
    print_info "Crawler services created successfully."
    print_warning "Timer files (.timer) need to be created separately."
    print_info "Services created:"
    echo "  - gtfs-crawler-20s.service"
    echo "  - gtfs-crawler-60s.service" 
    echo "  - gtfs-crawler-120s.service"
    echo "  - gtfs-crawler-1day.service"
    echo "  - gtfs-compress.service"
}

setup_downloader_service() {
    print_info "Setting up downloader service..."
    
    create_service_file "gtfs-downloader" \
        "GTFS Data Downloader" \
        "$TASK_PATH -d $PROJECT_DIR download"
    
    print_info "Downloader service created successfully."
    print_warning "Timer file (.timer) needs to be created separately."
    print_info "Service created:"
    echo "  - gtfs-downloader.service"
}

reload_systemd() {
    print_info "Reloading systemd daemon..."
    sudo systemctl daemon-reload
    print_info "Systemd daemon reloaded."
}

main() {
    if [ $# -ne 1 ]; then
        print_error "Invalid number of arguments."
        usage
    fi
    
    case "$1" in
        "crawler")
            check_requirements
            setup_crawler_services
            reload_systemd
            print_info "Crawler setup completed successfully."
            ;;
        "downloader")
            check_requirements
            setup_downloader_service
            reload_systemd
            print_info "Downloader setup completed successfully."
            ;;
        *)
            print_error "Invalid argument: $1"
            usage
            ;;
    esac
}

main "$@"
