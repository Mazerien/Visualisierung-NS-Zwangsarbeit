#!/bin/sh
sleep 5
flask --app app/main.py run

tail -f /dev/null       # Heartbeat