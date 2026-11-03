#!/bin/bash -e

if [ -z "$1" ]; then
  . ./.venv/bin/activate
  ./ytm-api.py
  deactivate
fi

mkdir -p public

echo "[css] frontend/styles/main.css -> public/styles/main.min.css with tailwind minifying..."
tailwindcss-cli -i ./frontend/styles/main.css -o ./public/styles/main.min.css --minify --silent

for file in frontend/scripts/*.js; do
    [ -f "$file" ] || continue

    filename=$(basename "$file" .js)

    echo "[javascript] $file -> public/scripts/$filename.min.js minifying..."
    terser "$file" \
        --compress \
        --mangle \
        --output "public/scripts/${filename}.min.js"
done

echo "[resource] copy assets..."
cp -varf frontend/assets public

version=$(date +%s)

echo "[html] update version tag -> $version"
sed "s/VER_TAG/$version/g" ./frontend/index.html > ./public/index.html
