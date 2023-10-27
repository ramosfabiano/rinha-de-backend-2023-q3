#/bin/bash

uvicorn main:app --workers 1 --port $APP_PORT --backlog 8192  --timeout-keep-alive 1 --no-access-log  #--log-level warning
