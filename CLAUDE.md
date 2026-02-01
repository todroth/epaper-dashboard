# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an e-paper dashboard application built for Python 3.12. The project uses SVG templates with token replacement to render content for display on e-paper devices.

## Running the Application

```bash
# Run the main data loading pipeline
./run.sh

# Run individual modules directly
python3 -m src.weather.getweather
```

The `run.sh` script orchestrates loading data from multiple sources (weather, alerts, calendar, sun, time). Currently only weather is implemented.

## Project Structure

- `src/` - Main application source code
  - `src/weather/` - Weather data loading and providers
  - `src/utils.py` - Shared utilities (logging, HTTP requests)
- `lib/e-Paper/` - Waveshare e-Paper library (git submodule)
  - Python drivers: `lib/e-Paper/RaspberryPi_JetsonNano/python/lib/`
  - Examples: `lib/e-Paper/RaspberryPi_JetsonNano/python/examples/`
- `templates/` - SVG templates with token placeholders for dynamic content
- `assets/icons/` - Icon resources
- `.env` - Environment configuration (copy from `.env.example`)

## Architecture

### Weather Provider Plugin System

The weather module uses a provider pattern (`src/weather/provider/`) to support multiple weather APIs:

- **BaseProvider** (`baseprovider.py`) - Abstract base class that all providers must inherit from. Defines the `load() -> WeatherData` contract and handles location configuration from environment variables.
- **Provider implementations** (e.g., `brightsky.py`) - Concrete providers that fetch from specific weather APIs and map their response formats to the common `WeatherData` dataclass.
- **Configuration** - Provider selection is done via `WEATHER_PROVIDER` environment variable (currently supports `brightsky`).

To add a new weather provider:
1. Create a new class inheriting from `BaseProvider` in `src/weather/provider/`
2. Implement the `load()` method to return `WeatherData`
3. Map the provider's icon format to `WeatherIcon` enum values
4. Add the provider name to the match statement in `getweather.py:load_weather()`

### Data Models

- **WeatherData** (`weatherdata.py`) - Common dataclass for weather information (temp_min, temp_max, icon)
- **WeatherIcon** (`weathericon.py`) - Enum representing normalized weather conditions across providers

### Configuration

Environment variables in `.env`:
- `DISPLAY_WIDTH`, `DISPLAY_HEIGHT` - Display resolution (default 800x480)
- `LOCATION_LAT`, `LOCATION_LON` - Geographic coordinates for weather
- `WEATHER_PROVIDER` - Which weather API to use (currently only "brightsky")

## Template System

The dashboard uses SVG templates with token-based placeholders. See `templates/example.svg` for the pattern:

- Tokens are uppercase placeholder strings (e.g., `TIME_NOW`, `TEMP_NOW`, `WEATHER_DESCRIPTION`)
- Templates define the layout at 800x480 resolution (common e-paper display size)
- Token replacement happens before rendering to the e-paper display

When implementing template rendering, the pattern is:
1. Load SVG template
2. Replace tokens with actual data
3. Render to bitmap format for e-paper

## Output Files

The `.gitignore` specifies these output patterns that are generated but not committed:
- `screen-output.*` - Main display output files
- `output.png`, `output.bmp` - Rendered images
- `cache_*.json`, `cache_*.pickle` - Cached data from APIs
- `token.pickle`, `outlooktoken.bin` - OAuth tokens

## E-Paper Hardware Library

The project uses the official Waveshare e-Paper library (added as git submodule):
- Repository: https://github.com/waveshareteam/e-Paper
- Location: `lib/e-Paper/`
- To initialize after cloning: `git submodule update --init --recursive`

The Python drivers support various Waveshare e-paper display models. Import drivers from the submodule path when implementing display functionality.

## Development Environment

- Python 3.12+ required
- Uses virtual environment (venv)
- Dependencies managed via `pyproject.toml`
- Git submodules must be initialized after cloning
- Logging is configured via `configure_logging()` from `src/utils.py`