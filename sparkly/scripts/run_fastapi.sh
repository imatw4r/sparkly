#!/bin/bash

if [ "$RELOAD_APP" == true ]; then
  exec uvicorn main:app --app-dir sparkly/app/entrypoints/http/fastapi \
                        --host 0.0.0.0 \
                        --port 8000 \
                        --reload;
else
  exec uvicorn main:app --app-dir sparkly/app/entrypoints/http/fastapi \
                        --host 0.0.0.0 \
                        --port 8000 \
                        --header server:HIDDEN;
fi
