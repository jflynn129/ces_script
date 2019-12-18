The CES demo is a Python scipt that opens a named pipe to receive data, it then takes that data and 
sends it to Azure IoT Hub using the connection string that the user has specified. An example program start
is:

   python ces_demo.py -c "HostName=PythonDemo.azure-devices.net;DeviceId=MyPythonDevice;SharedAccessKey=KRgEJfu3xcYc0g7vZrX5pUUQ7ssS80Lt3uSH7/LHEIU=" -d -p jim

you can send a speed threshold for the program using the az CLI; eg,

   az iot hub invoke-device-method -n PythonDemo -d MyPythonDevice --mn SetSpeedThreshold --mp 20

This will set the speed threshold to 20 mph

You can monitor the IoT Hub events using the az CLI command:

   az iot hub monitor-events --hub-name PythonDemo --device-id MyPythonDevice

