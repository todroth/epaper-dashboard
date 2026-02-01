#!/usr/bin/env bash

echo "Loading weather data..."

if ! python3 -m dashboard.weather; then
  echo "⚠️ Error loading weather data"
  exit 1
fi

echo
echo "Loading alert data..."

echo
echo "Loading calendar data..."

echo
echo "Loading sun data..."

echo
echo "Loading time data..."