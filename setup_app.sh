#!/bin/bash

echo "Setup app"
cd "$(dirname "$0")" || return
FILE=.env
if [ -f "$FILE" ]; then
	echo "tiedosto olemassa"
else
	touch $FILE
	echo "$FILE tiedosto puuttuu, luodaan"
	echo -e "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres\n" >>$FILE
	echo -e "TEST_ENV=true\n" >>$FILE
	echo "SECRET_KEY='sekret'" >>$FILE
fi

poetry run python3 src/db_helper.py

echo "DB setup done"

poetry run python3 src/index.py
status=$?
echo "started flask server"

BROWSER=firefox
BROWSER1=google-chrome

if [ -n "$BROWSER" ]; then
	$BROWSER 'http://127.0.0.1:5001/'
elif [ -n "$BROWSER1" ]; then
	$BROWSER1 'http://127.0.0.1:5001/'

fi

kill $(lsof -t -i:5001)

exit $status
