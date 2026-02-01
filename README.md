# E-Paper Dashboard

A modular e-paper dashboard for Raspberry Pi that displays weather, alerts, sunrise/sunset times, and date/time information on a Waveshare 7.5" e-Paper display.

## Features

- **Modular Data Providers** - Plugin architecture for weather, alerts, sun times, and datetime
- **SVG Template System** - Customizable layouts with token-based placeholders
- **Efficient Rendering** - In-memory SVG to bitmap conversion optimized for e-paper
- **Low Power Consumption** - E-paper displays content without power after updates
- **Brightsky Integration** - Weather and alert data from DWD (Deutscher Wetterdienst)
- **Localization Support** - Configurable timezone and locale settings

## Hardware Requirements

- **Raspberry Pi Zero W** (or any Raspberry Pi model)
- **Waveshare 7.5inch e-Paper Display V2** (800×480 resolution)
- MicroSD card (8GB minimum, 16GB recommended)
- Power supply (5V, 2.5A recommended)

## Software Requirements

- Raspberry Pi OS Trixie (Debian 13) - **Required**
- Python 3.13 (comes with Trixie)
- Internet connection for weather data

**Note:** This project requires Python ≥3.12. Bookworm (Debian 12) ships with Python 3.11 and is **not compatible**.

---

## Setup Guide

### Prerequisites

Before starting, ensure you have:

- Raspberry Pi Zero W with **Raspberry Pi OS Trixie Lite (32-bit)** installed
- SSH enabled and WiFi configured
- SSH access to your Pi
- Waveshare 7.5inch e-Paper Display V2 connected to GPIO pins

**Important:** Pi Zero W requires 32-bit OS (ARMv6). This project requires Python ≥3.12, so Trixie (Python 3.13) is mandatory.

### Installation

Connect to your Raspberry Pi via SSH and follow these steps:

#### 1. Update System and Install Dependencies

```bash
sudo apt update && sudo apt full-upgrade -y

# Install system dependencies for image processing
sudo apt install -y python3 python3-pip python3-venv git \
    libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev \
    libopenjp2-7 libtiff6 libcairo2 libpango-1.0-0 \
    libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev \
    shared-mime-info

# Enable SPI interface (required for e-Paper display)
sudo raspi-config nonint do_spi 0
sudo reboot
```

#### 2. Clone Repository and Install

```bash
# Clone with submodules (Waveshare library)
git clone --recurse-submodules https://github.com/todroth/epaper-dashboard.git
cd epaper-dashboard

# Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

**Note:** Installation takes 5-10 minutes on Pi Zero W.

#### 3. Configuration

Create and edit `.env` file:

```bash
cp .env.example .env
nano .env
```

Configure your location and settings:
- `LOCATION_LAT` / `LOCATION_LON` - Your coordinates (find on Google Maps)
- `TIMEZONE` - e.g., `Europe/Berlin` (check `timedatectl list-timezones`)
- `LOCALE` - e.g., `de_DE.UTF-8` (check `locale -a`)
- `TEMPLATE` - SVG template filename from `templates/`

#### 4. Run the Dashboard

```bash
./run.sh
```

The display will update after 15-20 seconds. The script automatically activates the venv.

#### 5. Automate Updates (Optional)

Create update script:

```bash
cat > ~/update-dashboard.sh << 'EOF'
#!/bin/bash
cd /home/pi/epaper-dashboard
source venv/bin/activate
./run.sh
EOF

chmod +x ~/update-dashboard.sh
```

Schedule with cron:

```bash
crontab -e
# Add: */30 * * * * ~/update-dashboard.sh >> ~/dashboard.log 2>&1
```

---

## Troubleshooting

**Display not updating:** Check SPI enabled with `lsmod | grep spi`

**Weather data issues:** Verify coordinates in `.env` and internet connection

**Wrong Python version:** Requires Python ≥3.12 (Trixie only). Check: `python3 --version`

## Contributing

Contributions are welcome! This project is still work in progress.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Waveshare e-Paper library](https://github.com/waveshareteam/e-Paper) - Display drivers
- [Brightsky API](https://brightsky.dev/) - Weather data from DWD
- [Astral](https://github.com/sffjunkie/astral) - Sunrise/sunset calculations
- [CairoSVG](https://cairosvg.org/) - SVG rendering

---

**Enjoy your personalized e-paper dashboard! 🎨📊🌤️**
