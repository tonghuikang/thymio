#10.009 The Digital World 1D Project
#17F04 Group 2

''' ADJ_LIST SUBSCRIPTION '''
'''
This script subscribes to the adj_list topic
on Google Cloud. The received input is written
to a text file, which is then read by cam_lights
script to perform the LED operations. The data
is also sent to Firebase to retain the settings
when the Kivy app is reopened.
'''
#directory of text file receiving adj_list data
txt = '/home/pi/thymio/cam_dw_1D/adj_list.txt'

#import statements
import paho.mqtt.client as mqttClient #import the client for Google cloud
from time import sleep
from firebase import firebase #for permanent storage of adj_list

#set up Firebase
url = "https://dw2018-1d-project.firebaseio.com/"
secret = "mwS8gxOh624P4fJ0FR1BUOTPEqFjIMkvnnOni9RL"
fire = firebase.FirebaseApplication(url, secret)

#write received data in a text file
def write_to_txt(file, message):
    f = open(file, 'w')
    f.write('{}\n'.format(message))
    f.close()
    print('Message written to text file')

#call write_to_txt() & send to Firebase upon receiving message from Google Cloud
def on_message(client, userdata, message):
    received_data = str(message.payload.decode("utf-8"))
    print("Message received:", received_data)
    write_to_txt(txt, received_data)
    received_data_list_raw = received_data.strip('[]').split(',')
    received_data_list = [float(item) for item in received_data_list_raw]
    fire.put('/', 'adj_list', received_data_list)
    print("Message sent to Firebase")

#setting up connection to Google Cloud
broker_address="35.197.131.13"
port = 8883
print("Creating new instance")
dw1d = mqttClient.Client("DW1Dadjsub")
dw1d.username_pw_set("sammy","password")  #set usernames and passwords
dw1d.on_message = on_message              #attach functions to callback
print("Connecting to broker")
dw1d.connect(broker_address, port=port)   #connect to broker

#actual loop for receiving info
dw1d.loop_start()
print("Subscribed, waiting for message")
dw1d.subscribe("adj_list")
sleep(100000)
dw1d.loop_stop()
