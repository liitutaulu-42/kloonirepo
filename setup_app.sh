#!/bin/bash

echo "Setup app"

FILE=.env
if [ ! -f "$FILE" ]; then
	echo "$FILE tiedosto puuttuu, luodaan"
	echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres\n" >$FILE
	echo "TEST_ENV=true" >$FILE
	echo "SECRET_KEY='sekret'" >$FILE
fi

poetry run python3 src/db_helper.py

echo "DB setup done"

poetry run python3 src/index.py
status=$?
echo "started flask server"

BROWSER=firefox

if [ -n "$BROWSER" ]; then
	$BROWSER 'http://127.0.0.1:5001/'
fi

kill $(lsof -t -i:5001)

exit $status
