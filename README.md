Python CES Demo

Program Startup
```
usage: ces_demo.py [-h] [-d] [-c CONSTRING] [-p FIFOPIPE] [-j JPEG]

CES race track demo script

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           enable output of debug messages
  -c CONSTRING, --constring CONSTRING
                        connection string for Azure IoT Hub
  -p FIFOPIPE, --fifopipe FIFOPIPE
                        Named PIPE to use for reading data to be sent
  -j JPEG, --jpeg JPEG  Picture Data File to be uploaded to Azure blob storage
```

This script opens a user specified named pipe to receive data then sends that data to the Azure IoT Hub specified in the user supplied connection. Example: 
```
python ces_demo.py -c "HostName=PythonDemo.azure-devices.net;DeviceId=MyPythonDevice;SharedAccessKey=KRgEJfu3xcYc0g7vZrX5pUUQ7ssS80Lt3uSH7/LHEIU=" -d -p jim
```

A speed threshold can be set using the az CLI, e.g.
```
   az iot hub invoke-device-method -n PythonDemo -d MyPythonDevice --mn SetSpeedThreshold --mp 20
```

This command sets the speed threshold to 20 mph.

Lately, you can monitor IoT Hub events being sent to Azure using the az CLI command:
```
   az iot hub monitor-events --hub-name PythonDemo --device-id MyPythonDevice
```

