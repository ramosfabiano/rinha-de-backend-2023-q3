#/bin/bash

uvicorn main:app --workers 2 --port $APP_PORT
