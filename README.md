# E-Paper Dashboard v2

Modern E-Paper dashboard for Raspberry Pi Zero W with weather, calendar, and custom data.

## Requirements

- Raspberry Pi Zero W
- Raspberry Pi OS Trixie (32-bit) or later
- Python 3.12+
- Waveshare 7.5" E-Paper Display

## Quick Start

```bash
# Clone repository with submodules
git clone --recursive [your-repo-url]
cd epaper-dashboard-v2

# Or add submodule manually:
git submodule add https://github.com/waveshare/e-Paper lib/e-Paper
git submodule update --init --recursive

# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
nano .env  # Edit with your settings

# Run
python src/main.py
```

## Project Structure

```
epaper-dashboard-v2/
├── src/              # Your Python code goes here
├── templates/        # SVG templates with tokens
├── assets/
│   └── icons/        # Weather icons
├── lib/
│   └── e-Paper/      # Waveshare library (git submodule)
├── .env              # Your configuration (not in git)
└── pyproject.toml    # Project metadata
```

## Development

Built for Python 3.12+ with modern dependencies and clean architecture.

Inspired by [waveshare-epaper-display](https://github.com/mendhak/waveshare-epaper-display).

## License

MIT
