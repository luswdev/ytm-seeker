#!/bin/bash -e

VENV_PATH=.venv

function gen_py_env () {
  echo "generating python virtual environment..."
  python3 -m venv $VENV_PATH

  echo "installing pip requirements..."
  . ./${VENV_PATH}/bin/activate
  pip install -qr ./requirements.txt
  deactivate
}

# if no argument input, default build ytm api
# otherwise, skip to generate frontend files
if [ -z "$1" ]; then
  echo "checking python virtual environment..."
  if [ ! -d "${VENV_PATH}" ]; then
    gen_py_env
  fi

  echo "start ytm api seeking..."
  . ./${VENV_PATH}/bin/activate
  ./ytm-api.py
  deactivate
fi

DIST_PATH=public

echo "generating output \"${DIST_PATH}\" directory..."
mkdir -p $DIST_PATH

echo "[css] frontend/styles/main.css -> $DIST_PATH/styles/main.min.css with tailwind minifying..."
tailwindcss-cli -i ./frontend/styles/main.css -o ./${DIST_PATH}/styles/main.min.css --minify --silent

for file in frontend/scripts/*.js; do
    [ -f "$file" ] || continue

    filename=$(basename "$file" .js)

    echo "[javascript] $file -> $DIST_PATH/scripts/$filename.min.js minifying..."
    terser "$file" \
        --compress \
        --mangle \
        --output "${DIST_PATH}/scripts/${filename}.min.js"
done

echo "[resource] copy assets..."
cp -varf frontend/assets public

version=$(date +%s)

echo "[html] update version tag -> $version"
sed "s/VER_TAG/$version/g" ./frontend/index.html > ./${DIST_PATH}/index.html

echo "build done."
