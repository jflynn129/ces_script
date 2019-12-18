import argparse, os, errno
import sys, time
import threading

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

# Login to Azure using the CLI:
# az login -u <username> -p <password>
#
# Set the active subscription (if necessary) with the CLI:
# az account set --subscription "My Demos"
#
# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table

MSG_TXT = '{{"{0}": {1}}}'
THRESHOLD = 5

parser = argparse.ArgumentParser(
	description='CES race track demo script', 
	)
parser.add_argument('-d', '--debug', action='store_true',
	help='enable output of debug messages',
	default=False
        )
parser.add_argument('-c', '--constring',
        help='connection string for Azure IoT Hub',
        default=' '
        )
parser.add_argument('-p', '--fifopipe',
        help='Named PIPE to use for reading data to be sent',
        default=''
        )
parser.add_argument('-j', '--jpeg',
        help='Picture Data File to be uploaded to Azure blob storage',
        default='pic.jpg'
        )

#====================================================================================================================

def do_debug(doit, msg):
	if doit:
		sys.stdout.write(msg)

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(args.constring)
    return client


def device_method_listener(device_client):
    global THRESHOLD
    while True:
        method_request = device_client.receive_method_request()
        method_name=method_request.name
        payload=method_request.payload
        print ("\nUser requested {0} as: {1}".format( method_name,payload))
        if method_request.name == "SetSpeedThreshold":
            try:
                THRESHOLD = int(method_request.payload)
            except ValueError:
                response_payload = {"Response": "Invalid speed threshold specified"}
                response_status = 400
            else:
                response_payload = {"Response": "{0} set to {1} (mph)".format(method_request.name, THRESHOLD)}
                response_status = 200
        else:
            response_payload = {"Response": "Direct method {} not defined".format(method_request.name)}
            response_status = 404

        method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
        device_client.send_method_response(method_response)
        print("\nSet (" + str(THRESHOLD) + ")")



#====================================================================================================================

if __name__ == '__main__':

    args = parser.parse_args()

    if len(args.fifopipe) == 0:
        fifopipe = 'CESDemo'
    else:
        fifopipe = args.fifopipe

    try:
        os.mkfifo(fifopipe)

    except OSError as oe:
	if os.errno != errno.EEXIST:
            raise

    print("               ")
    print("     ****      ")
    print("    **  **     CES Python demo, press Ctrl-C to exit")
    print("   **    **    ")
    print("  ** ==== **   \n")
    print("              Debug: " + str(args.debug))
    print("  Connection string: [ " + args.constring + " ]")
    print("   Using named pipe: " + args.fifopipe)
    print("Picture File set to: " + args.jpeg)
    print("    Speed Threshold: " + str(THRESHOLD))

    client = iothub_client_init()

    # Start a thread to listen 
    device_method_thread = threading.Thread(target=device_method_listener, args=(client,))
    device_method_thread.daemon = True
    device_method_thread.start()

    try:
        run = True
        while run:
            do_debug(args.debug, "Open "+fifopipe+" pipe\n")
    	    with open(fifopipe) as fifo:
    	        do_debug(args.debug, ' Opened\n')
    	        while True:
    		    data = fifo.read()
    		    if len(data) == 0:
    		        do_debug(args.debug, 'No more data in pipe\n')
    		        break
    		    else:
    		        do_debug(args.debug, 'Read: "{}"\n'.format(data[:-1]))
    		        indata = data.split(':')
                        key = indata[0][1:]
    		        value = indata[1][:-2]
         	        if key == 'EOF':
    			    do_debug(args.debug, 'close named pipe.\n')
     			    run = False
    			    break
    		        if key == 'speed_kmph':
    			    do_debug(args.debug, 'speed (in kmph) is {}\n'.format(value))
    		        elif key == 'speed_mph':
    			    do_debug(args.debug, 'speed (in mph) is {}\n'.format(value))
    		        elif key == 'location_latitude':
    			    do_debug(args.debug, 'latitude is {}\n'.format(value))
        		elif key == 'location_longitude':
        		    do_debug(args.debug, 'longitude is {}\n'.format(value))
    		        else:
    			    do_debug(args.debug, 'sending: {"'+key+'":"'+value+'"}\n')
                        msg = MSG_TXT.format(key, value)
    		        message = Message(msg)
    		        # Send the message.
            	        do_debug(args.debug, 'Sending message: {}\n'.format(message) )
    		        client.send_message(message)
    		        do_debug(args.debug, 'Message sent\n' )
    
        fifo.close()

    except KeyboardInterrupt:
        os.unlink(fifopipe)
        print('Exit programm.')



