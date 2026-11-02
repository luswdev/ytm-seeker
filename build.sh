#!/bin/bash

. ./.venv/bin/activate
./ytm-api.py
deactivate

rm -rvf public
cp -avf frontend public

version=$(date +%s)

sed "s/VER_TAG/$version/g" ./frontend/index.html > ./public/index.html
