set port=8000
set ip=192.168.1.223

@echo Started at %_time
@rem gates
curl -X PUT %ip%:%port%/lever/14/N

@echo.
@echo Selecting Passenger
curl -X PUT %ip%:%port%/lever/15/R
curl -X PUT %ip%:%port%/lever/16/N

curl -X GET %ip%:%port%/

@echo.
@echo Down passenger at %_time
curl -X PUT %ip%:%port%/lever/1/R
curl -X PUT %ip%:%port%/lever/1/N
delay 10

@echo.
@echo Up passenger at %_time
@rem signal
curl -X PUT %ip%:%port%/lever/12/R
curl -X PUT %ip%:%port%/lever/13/R
curl -X PUT %ip%:%port%/lever/13/N
curl -X PUT %ip%:%port%/lever/12/N
delay 10

@echo.
@echo Selecting Mineral
curl -X PUT %ip%:%port%/lever/15/N
curl -X PUT %ip%:%port%/lever/16/R

curl -X GET %ip%:%port%/

@echo.
@echo Up mineral at %_time
@rem Up train
curl -X PUT %ip%:%port%/lever/13/R
curl -X PUT %ip%:%port%/lever/13/N
delay 10

@echo.
@echo Down mineral at %_time
curl -X PUT %ip%:%port%/lever/1/R
curl -X PUT %ip%:%port%/lever/1/N

@rem gates
curl -X PUT %ip%:%port%/lever/14/R

@echo.
@echo Finished at %_time
