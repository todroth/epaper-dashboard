#!/usr/bin/env bash

echo "Loading weather data..."
if ! python3 -m dashboard.getweather; then
  echo "⚠️ Error loading weather data"
fi

echo
echo "Loading alert data..."

echo
echo "Loading calendar data..."

echo
echo "Loading sun data..."

echo
echo "Loading time data..."

echo
echo "Replacing placeholders in SVG file..."
if ! python3 -m dashboard.replacesvg; then
  echo "⚠️ Error creating svg file"
fi

echo
echo "Sending image to display..."