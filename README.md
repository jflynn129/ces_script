# Python CES Demo

## Program Startup
```
usage: ces_demo.py [-h] [-d] [-c CONSTRING] [-p FIFOPIPE] [-b CONSTRING]

CES race track demo script

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           enable output of debug messages
  -c CONSTRING, --constring CONSTRING
                        connection string for Azure IoT Hub
  -p FIFOPIPE, --fifopipe FIFOPIPE
                        Named PIPE to use for reading data to be sent
  -b, --blobconstr      Connect string for blob storage
```

This script opens a user specified named pipe to receive data then sends that data to the Azure IoT Hub specified in the user supplied connection. Example: 
```
python ces_demo.py -c "HostName=PythonDemo.azure-devices.net;DeviceId=MyPythonDevice;SharedAccessKey=KRgEJfu3xcYc0g7vZrX5pUUQ7ssS80Lt3uSH7/LHEIU=" -p jim
```
To send picture data, you will add the Azure Storage connection string with the '-b' flag. When an input record signals, the file will be uploaded to Azure storage.


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

## Example run results with setting a speed threshold
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

## Picture upload

To upload a picture file to Blob storage you must specify the connection string for blob storage as well as the picture file name.  The connection string can be found using the az CLI, for example:

```
az storage account show-connection-string --name pythoniotstorage --resource-group PythonJMF --subscription Pay-As-You-go
{
  "connectionString": "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=pythoniotstorage;AccountKey=QEkzFfv6RoyOc6AhATMvIaOGi7SK5D9g39R8CzZ3vVj9KB0Rn6Qldb/zbdouD5EAjMKV+d3sxwdKjLssiHDTfw=="
}
```

Then using this connection string plus all the other configuration flags, start the script:

```
python ces_demo.py -b "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=pythoniotstorage;AccountKey=QEkzFfv6RoyOc6AhATMvIaOGi7SK5D9g39R8CzZ3vVj9KB0Rn6Qldb/zbdouD5EAjMKV+d3sxwdKjLssiHDTfw==" -c "HostName=PythonDemo.azure-devices.net;DeviceId=MyPythonDevice;SharedAccessKey=KRgEJfu3xcYc0g7vZrX5pUUQ7ssS80Lt3uSH7/LHEIU=" -p jim -d
               
     ****      
    **  **     CES Python demo, press Ctrl-C to exit
   **    **    
  ** ==== **   

              Debug: True
  Connection string: [ HostName=PythonDemo.azure-devices.net;DeviceId=MyPythonDevice;SharedAccessKey=KRgEJfu3xcYc0g7vZrX5pUUQ7ssS80Lt3uSH7/LHEIU= ]
   Using named pipe: jim
    Speed Threshold: 5
```

From a second terminal window, enter:
```
echo {pict:localpict.png} > jim
echo {EOF:EOF} > jim
```

Assuming a file 'localpict.png' is present, you will then see the python script respond as:

```
Read: "{pict:localpict.png}"

--Blob Initialize:
     picture name: localpict.png
   container name: localpictf20eeb9f-81b7-4c4f-85af-8516d49d3cc5
connection string: [DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=pythoniotstorage;AccountKey=QEkzFfv6RoyOc6AhATMvIaOGi7SK5D9g39R8CzZ3vVj9KB0Rn6Qldb/zbdouD5EAjMKV+d3sxwdKjLssiHDTfw== ]

Upload localpict.png to localpictf20eeb9f-81b7-4c4f-85af-8516d49d3cc5
sending: {"pict":"localpictf20eeb9f-81b7-4c4f-85af-8516d49d3cc5"}
Sending message: {"pict": localpictf20eeb9f-81b7-4c4f-85af-8516d49d3cc5}
Message sent
No more data in pipe
Open jim pipe
 Opened
Read: "{EOF:EOF}"
close named pipe.
```

You can login to your azure portal and not that the picture file has been stored within Azure.

