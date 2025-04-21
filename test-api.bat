set port=8000
curl -X GET localhost:%port/lever/1/R
delay 10
curl -X GET localhost:%port/lever/1/N
delay 1

curl -X GET localhost:%port/lever/13/R
delay 10
curl -X GET localhost:%port/lever/13/N
delay 1


curl -X GET localhost:%port/lever/14/R
delay 10
curl -X GET localhost:%port/lever/14/N
delay 1
