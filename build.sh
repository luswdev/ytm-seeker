#!/bin/bash -e

if [ -z "$1" ]; then
  . ./.venv/bin/activate
  ./ytm-api.py
  deactivate
fi

rm -rvf public
cp -avf frontend public

tailwindcss-cli -i ./frontend/styles/main.css -o ./public/styles/main.css

version=$(date +%s)

sed "s/VER_TAG/$version/g" ./frontend/index.html > ./public/index.html
