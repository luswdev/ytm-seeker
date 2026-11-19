#!/bin/bash -e

VENV_PATH=.venv
DIST_PATH=public

function usage () {
  cat <<EOF
usage: $0 <step>

    step:
        y,ytm         fetch ytm api data
        c,css         generate tailwind css file(s)
        j,js          generate minify javascript file(s)
        r,resource    copy all resource file(s) to public folder
        h,html        generate html file(s) with version tag
        f,frontend    generate all frontend file(s)
        a,all         generate all frontend file(s) and fetch ytm api data
EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

function _check_dist_folder () {
  echo "generating output \"${DIST_PATH}\" directory..."
  mkdir -vp $DIST_PATH
  mkdir -vp $DIST_PATH/assets/data
}

function _check_py_env () {
  echo "checking python virtual environment..."
  if [ ! -d "${VENV_PATH}" ]; then
    echo "generating python virtual environment..."
    python3 -m venv $VENV_PATH

    echo "installing pip requirements..."
    . ./${VENV_PATH}/bin/activate
    pip install -qr ./requirements.txt
    deactivate
  else
    echo "python virtual environment is existed."
  fi
}

function _step_ytm_api () {
  _check_py_env

  echo "start ytm api seeking..."
  . ./${VENV_PATH}/bin/activate
  ./ytm-api.py "$DIST_PATH/assets/data"
  deactivate
}

function _step_css () {
  echo "[css] frontend/styles/main.css -> $DIST_PATH/styles/main.min.css with tailwind minifying..."
  tailwindcss-cli -i ./frontend/styles/main.css -o ./${DIST_PATH}/styles/main.min.css --minify --silent
}

function _step_js () {
  for file in frontend/scripts/*.js; do
      [ -f "$file" ] || continue

      filename=$(basename "$file" .js)

      echo "[javascript] $file -> $DIST_PATH/scripts/$filename.min.js minifying..."
      terser "$file" \
          --compress \
          --mangle \
          --output "${DIST_PATH}/scripts/${filename}.min.js"
  done
}

function _step_resource () {
  echo "[resource] copy assets..."
  cp -varf frontend/assets public

  echo "[resource] copy seo files..."
  cp -varf frontend/robots.txt frontend/sitemap.xml $DIST_PATH
}

function _step_html () {
  version=$(date +%s)
  echo "[html] update version tag -> $version"
  sed "s/VER_TAG/$version/g" ./frontend/index.html > ./${DIST_PATH}/index.html
}

STEP="${1:-}"

case "$STEP" in
  y|ytm)          _check_dist_folder;_step_ytm_api;;
  c|css)          _check_dist_folder;_step_css;;
  j|js)           _check_dist_folder;_step_js;;
  r|resource)     _check_dist_folder;_step_resource;;
  h|html)         _check_dist_folder;_step_html;;
  f|frontend)     _check_dist_folder;_step_css; _step_js; _step_html;;
  a|all)          _check_dist_folder;_step_ytm_api; _step_css; _step_js; _step_html;;
  *)
    echo "unknown step: $STEP"
    usage
    exit 1
    ;;
esac

echo "build done."
