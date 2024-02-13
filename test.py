import os
import time
from twilio.rest import Client
import adafruit_dht
import board

# Twilio credentials
account_sid = "ACb240c4eb917728e7bffd575f791091e7"
auth_token = "8c609363de9b1c8331afaad221db693b"
client = Client(account_sid, auth_token)

# DHT sensor setup
dht_device = adafruit_dht.DHT11(board.D4)

# Initialize previous temperature and humidity
prev_temperature_c = None
prev_humidity = None

def send_sms(message):
    """Function to send SMS using Twilio."""
    try:
        message = client.messages.create(
            body=message,
            from_='+16596992336',
            to='+919072049254'
        )
        print("SMS sent successfully!")
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")

while True:
    try:
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity

        # Check if there is a change in temperature or humidity
        if (prev_temperature_c is None or prev_temperature_c != temperature_c) or \
           (prev_humidity is None or prev_humidity != humidity):
            message = f"Temperature: {temperature_c}°C, Humidity: {humidity}%"
            send_sms(message)
            prev_temperature_c = temperature_c
            prev_humidity = humidity
            print("Message sent due to change in temperature or humidity")

        # Print sensor readings
        print(f"Temp: {temperature_c}°C   Humidity: {humidity}%")

    except RuntimeError as err:
        print(err.args[0])

    time.sleep(2.0)
