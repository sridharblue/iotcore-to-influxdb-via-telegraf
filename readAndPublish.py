import RPi.GPIO as GPIO
import dht11
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
 
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
 
# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("123afhlss456")
myMQTTClient.configureEndpoint("XXXXXX-ats.iot.ap-south-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/demo/demo-cert/aws-root-cert.pem", "/home/pi/demo/demo-cert/private-key.pem.key", "/home/pi/demo/demo-cert/iot-cert.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
 
#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("demotopic/demo", "connected", 0)
 
#loop and publish sensor reading
while 1:
    now = datetime.utcnow()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
    instance = dht11.DHT11(pin = 4) #BCM GPIO04
    result = instance.read()
    if result.is_valid():
        payload = '{ "timestamp": "' + now_str + '","temperature": ' + str(result.temperature) + ',"humidity": '+ str(result.humidity) + ' }'
        print payload
        myMQTTClient.publish("demotopic/demo", payload, 0)
        sleep(10)
    else:
        print (".")
        sleep(1)
