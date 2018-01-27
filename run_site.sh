#!/bin/sh
export FLASK_APP=server.py
export FLASK_DEBUG=1
python3 -m flask run
