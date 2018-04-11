#!/usr/bin/env bash
curl -i http://127.0.0.1:12480/image/v1/dectect \
-F "image=@../darknet/data/dog.jpg" \
-F "api_key=f4ba472f161f052914bdbfcf2122a833" \
-F "api_secret=0172f5c5ede9e251dd44659eab3c0165"

curl -i http://127.0.0.1:12480/image/v1/mean \
-F "image=@../darknet/data/dog.jpg" \
-F "api_key=f4ba472f161f052914bdbfcf2122a833" \
-F "api_secret=0172f5c5ede9e251dd44659eab3c0165"
