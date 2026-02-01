# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an e-paper dashboard application for Raspberry Pi, built for Python ≥3.12. The project uses SVG templates with token replacement to render content, which is then converted and sent to a Waveshare 7.5inch e-Paper display (V2). Designed for Raspberry Pi OS Trixie (Python 3.13).

## Running the Application

```bash
# Install dependencies (first time only)
pip install -e .

# Initialize git submodules (first time only)
git submodule update --init --recursive

# Run the complete pipeline (loads data, renders template, sends to display)
./run.sh

# Run individual modules
python3 -m dashboard.getweather    # Load weather data
python3 -m dashboard.getalert      # Load alert data
python3 -m dashboard.getsun        # Load sunrise/sunset times
python3 -m dashboard.getdatetime   # Load current date/time
python3 -m dashboard.replacesvg    # Replace SVG template tokens
python3 -m dashboard.sendtodisplay # Send to e-paper display
```

The `run.sh` script orchestrates the complete pipeline sequentially.

## Project Structure

- `dashboard/` - Main application source code (NOT `src/`)
  - `dashboard/provider/` - Data provider plugins (weather, alert, sun, datetime)
  - `dashboard/utils/` - Shared utilities (logging, HTTP, file I/O)
  - `dashboard/get*.py` - Entry point modules that load data from providers
  - `dashboard/replacesvg.py` - Token replacement in SVG templates
  - `dashboard/sendtodisplay.py` - SVG to bitmap conversion and display output
- `lib/e-Paper/` - Waveshare e-Paper library (git submodule)
  - Display driver: `lib/e-Paper/RaspberryPi_JetsonNano/python/lib/waveshare_epd/epd7in5_V2.py`
- `templates/` - SVG templates with token placeholders
- `assets/icons/` - SVG icon resources
- `data/` - Generated output directory (gitignored)
  - `data/*.json` - Cached data from providers
  - `data/image.svg` - Final rendered SVG before display conversion
- `.env` - Environment configuration (copy from `.env.example`)

## Architecture

### Data Pipeline Flow

The application follows a strict sequential pipeline:

1. **Data Loading** - Each provider loads data and saves to `data/*.json`
   - Weather → `data/weather.json`
   - Alerts → `data/alert.json`
   - Sun times → `data/sun.json`
   - DateTime → `data/datetime.json`

2. **Template Rendering** - `replacesvg.py` merges all JSON data and performs token replacement
   - Loads template from `templates/$TEMPLATE`
   - Reads all JSON files and merges their `to_dict()` outputs
   - Replaces uppercase tokens (e.g., `TEMP_MIN`, `SUNRISE_TIME`) with values
   - Writes final SVG to `data/image.svg`

3. **Display Output** - `sendtodisplay.py` converts and sends to e-paper
   - SVG → PNG (in-memory using CairoSVG)
   - PNG → 1-bit bitmap (using Pillow with Floyd-Steinberg dithering)
   - Sends to epd7in5_V2 display (800x480 pixels)

### Provider Plugin System

All data providers inherit from `BaseDataProvider` which provides location and timezone configuration from environment variables. Each provider type has its own base class:

- **BaseWeatherProvider** - Weather data providers (currently: Brightsky)
- **BaseAlertProvider** - Weather alert providers (currently: Brightsky)
- **DateTimeProvider** - System datetime (no external API)
- **SunProvider** - Sunrise/sunset calculations using Astral library

To add a new provider:
1. Create a class inheriting from the appropriate base provider in `dashboard/provider/<type>/`
2. Implement the `load()` method returning the corresponding data model
3. Add provider selection logic in the relevant `dashboard/get*.py` module

### Data Models

All data models are dataclasses with a `to_dict()` method that returns token→value mappings:

- **WeatherData** - `temp_min`, `temp_max`, `icon` (WeatherIcon enum)
- **AlertData** - `headline`, `description`, `instruction`
- **SunData** - `sunrise_time`, `sunset_time` (formatted strings)
- **DateTimeData** - Various date/time fields in localized format

The `to_dict()` method converts field names to uppercase tokens (e.g., `temp_min` → `TEMP_MIN`) and formats values as strings suitable for SVG token replacement.

### Configuration

Environment variables in `.env`:
- `DISPLAY_WIDTH=800`, `DISPLAY_HEIGHT=480` - Display resolution
- `LOCATION_LAT`, `LOCATION_LON` - Geographic coordinates
- `TIMEZONE` - Timezone for datetime/sun calculations (e.g., `Europe/Berlin`)
- `LOCALE` - Locale for formatting (e.g., `de_DE.UTF-8`)
- `WEATHER_PROVIDER` - Provider name (currently only `brightsky`)
- `ALERT_PROVIDER` - Provider name (currently only `brightsky`)
- `TEMPLATE` - SVG template filename (e.g., `template-01.svg`)

### File Utilities (`dashboard/utils/files.py`)

Key functions:
- `write_json(obj, filename)` - Serialize dataclass to JSON in `data/` directory
- `read_json(filename, cls)` - Deserialize JSON to dataclass with enum support
- `read_template()` - Load SVG from `templates/$TEMPLATE`
- `write_template(content)` - Write final SVG to `data/image.svg`
- `read_icon_path(filename)` - Extract SVG content from icon files

All file I/O uses pathlib.Path and handles dataclass/enum serialization automatically.

## Hardware Requirements

- **Raspberry Pi Zero W** (or any Raspberry Pi model)
- **Waveshare 7.5inch e-Paper display V2** (800x480 resolution)
- **Raspberry Pi OS Trixie (Debian 13)** with Python 3.13

Note: This project requires Python ≥3.12. Raspberry Pi OS Bookworm (Debian 12) ships with Python 3.11 and is not compatible. Trixie ships with Python 3.13 and has full piwheels support for all dependencies including Pillow.

## Development Environment

- Python 3.12+ on development machine (macOS/Linux/Windows)
- Python 3.13 on Raspberry Pi (via Trixie)
- Dependencies managed via `pyproject.toml`:
  - `requests` - HTTP requests for API calls
  - `python-dotenv` - Environment configuration
  - `astral` - Sunrise/sunset calculations
  - `cairosvg` - SVG to PNG conversion
  - `pillow` - Image manipulation and bitmap conversion
- Git submodule for Waveshare e-Paper library
- Logging configured via `configure_logging()` from `dashboard/utils/utils.py`

The `sendtodisplay.py` module gracefully handles running on development machines by catching ImportError/OSError when the Waveshare library isn't available, allowing SVG conversion to be tested without hardware.

## Adding New Data Providers

Example: Adding a new weather provider called "openweather"

1. Create `dashboard/provider/weather/openweatherprovider.py`:
```python
from dashboard.provider.weather.baseweatherprovider import BaseWeatherProvider
from dashboard.provider.weather.weatherdata import WeatherData
from dashboard.utils.utils import fetch_json

class OpenWeatherProvider(BaseWeatherProvider):
    def load(self) -> WeatherData:
        # Fetch data using self.location_lat, self.location_lon, self.timezone
        # Map response to WeatherData with WeatherIcon enum
        pass
```

2. Update `dashboard/getweather.py`:
```python
match weather_provider_name:
    case "brightsky":
        weather_provider = BrightskyWeatherProvider()
    case "openweather":
        weather_provider = OpenWeatherProvider()
    case _: raise Exception(f"Weather provider {weather_provider_name} not supported")
```

3. Add to `.env.example`:
```
# possible values: brightsky, openweather
WEATHER_PROVIDER=brightsky
```
