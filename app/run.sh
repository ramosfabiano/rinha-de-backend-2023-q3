#/bin/bash

uvicorn main:app --reload --port $APP_PORT
