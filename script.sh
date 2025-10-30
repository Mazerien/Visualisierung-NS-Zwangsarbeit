#!/bin/sh
export FLASK_APP=app.main
export FLASK_ENV=dev # turn this off in prod!
sleep 5
waitress-serve --port 5000 app.main:app

tail -f /dev/null