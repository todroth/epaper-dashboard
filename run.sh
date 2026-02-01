#!/usr/bin/env bash

# Activate virtual environment
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/venv/bin/activate"

echo "Loading weather data..."
if python3 -m dashboard.getweather; then
  echo "✅"
else
  echo "⚠️ Error loading weather data"
fi

echo
echo "Loading alert data..."
if python3 -m dashboard.getalert; then
  echo "✅"
else
  echo "⚠️ Error loading alert data"
fi

echo
echo "Loading calendar data..."
if python3 -m dashboard.getcalendar; then
  echo "✅"
else
  echo "⚠️ Error loading calendar data"
fi

echo
echo "Loading sun data..."
if python3 -m dashboard.getsun; then
  echo "✅"
else
  echo "⚠️ Error loading sun data"
fi

echo
echo "Loading date time data..."
if python3 -m dashboard.getdatetime; then
  echo "✅"
else
  echo "⚠️ Error loading date time data"
fi

echo
echo "Replacing placeholders in SVG file..."
if python3 -m dashboard.replacesvg; then
  echo "✅"
else
  echo "⚠️ Error replacing placeholders in SVG file"
fi

echo
echo "Sending image to display..."
if python3 -m dashboard.sendtodisplay; then
  echo "✅"
else
  echo "⚠️ Error sending image to display"
fi
