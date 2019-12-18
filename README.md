# Python CES Demo

## Program Startup
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

## Speed Threshold
A speed threshold can be set using the az CLI, e.g.
```
   az iot hub invoke-device-method -n PythonDemo -d MyPythonDevice --mn SetSpeedThreshold --mp 20
```

This command sets the speed threshold to 20 mph.

## Monitor IoT Hub events
Lately, you can monitor IoT Hub events being sent to Azure using the az CLI command:
```
   az iot hub monitor-events --hub-name PythonDemo --device-id MyPythonDevice
```

## Example run results
Start **ces_demo** script then enter:
1. **echo "{jim:bob}" > jim** in seperate terminal session. 
2. **az iot hub invoke-device-method -n PythonDemo -d MyPythonDevice --mn SetSpeedThreshold --mp 20** in seperate terminal session
3. **echo "{EOF:EOF}" > jim**

Program output is:
```
               
     ****      
    **  **     CES Python demo, press Ctrl-C to exit
   **    **    
  ** ==== **   

              Debug: True
  Connection string: [ HostName=PythonDemo.azure-devices.net;DeviceId=MyPythonDevice;SharedAccessKey=KRgEJfu3xcYc0g7vZrX5pUUQ7ssS80Lt3uSH7/LHEIU= ]
   Using named pipe: jim
Picture File set to: pic.jpg
    Speed Threshold: 5
Open jim pipe
 Opened
Read: "{jim:bob}"
sending: {"jim":"bob"}
Sending message: {"jim": bob}
Message sent
No more data in pipe
Open jim pipe

User requested SetSpeedThreshold as: 20

Set (20)
 Opened
Read: "{EOF:EOF}"
close named pipe.
```

# IoT Hub events monitor output
```
Starting event monitor, filtering on device: MyPythonDevice, use ctrl-c to stop...
{
    "event": {
        "origin": "MyPythonDevice",
        "payload": "{\"jim\": bob}"
    }
}
```


