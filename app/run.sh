#/bin/bash

LOG_STRING='--no-access-log  --log-level warning'
#LOG_STRING='--log-level debug'

uvicorn main:app --workers 1 --port $APP_PORT --backlog 8192  --timeout-keep-alive 1  $LOG_STRING
