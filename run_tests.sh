#!/bin/sh

IMG=pocin/kbc-ex-gmail-attachments:dev
docker build -t ${IMG} .
source .env
docker run -e KBC_EX_CLIENT_ID -e KBC_EX_CLIENT_SECRET -e KBC_EX_REFRESH_TOKEN ${IMG} python3 -m 'pytest'

