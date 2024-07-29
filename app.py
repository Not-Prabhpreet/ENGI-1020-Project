import streamlit as st
import pyttsx3
import speech_recognition as sr
import time
from engi1020.arduino.api import *
import serial
import threading

# Initialize TTS engine and recognizer
tts_engine = pyttsx3.init()  # Initialize the text-to-speech engine
recognizer = sr.Recognizer()  # Initialize the speech recognizer

# Define pins for Arduino components
BUTTON_PIN = 6
LED_PIN = 4

# Initialize the OLED screen
oled_clear()
oled_print("Initializing...")  # Display initialization message

def speak(text):
    """Function to convert text to speech and display it on Streamlit."""
    tts_engine.say(text)  # Convert text to speech
    tts_engine.runAndWait()  # Wait for the speech to complete
    st.write(f"Alice: {text}")  # Display text in Streamlit app
    print(f"Spoken: {text}")  # Print text to console

def recognize_speech():
    """Function to recognize speech using the microphone."""
    with sr.Microphone() as source:  # Use the microphone as the source
        st.write("Listening...")  # Display listening status
        audio = recognizer.listen(source)  # Listen for audio input
        try:
            command = recognizer.recognize_google(audio)  # Use Google's speech recognition
            st.write(f"You: {command}")  # Display recognized speech
            return command.lower()  # Return the command in lowercase
        except sr.UnknownValueError:
            st.write("Sorry, I did not understand that.")  # Handle unrecognized speech
            return None
        except sr.RequestError:
            st.write("Could not request results; check your network connection.")  # Handle network errors
            speak("Could not request results; check your network connection.")
            return None

def get_weather_data():
    """Function to get weather data from Arduino sensors."""
    try:
        temperature = pressure_get_temp()  # Get temperature
    except serial.SerialException as e:
        st.write("Error reading temperature from Arduino:", str(e))
        temperature = None

    try:
        humidity = (analog_read(3) / 1023.0) * 100  # Get humidity
    except serial.SerialException as e:
        st.write("Error reading humidity from Arduino:", str(e))
        humidity = None

    try:
        pressure = pressure_get_pressure()  # Get atmospheric pressure
    except serial.SerialException as e:
        st.write("Error reading pressure from Arduino:", str(e))
        pressure = None

    try:
        altitude = pressure_get_altitude()  # Get altitude
    except serial.SerialException as e:
        st.write("Error reading altitude from Arduino:", str(e))
        altitude = None

    try:
        light_level = analog_read(6)  # Get light level
    except serial.SerialException as e:
        st.write("Error reading light level from Arduino:", str(e))
        light_level = None

    try:
        sound_level = analog_read(2)  # Get sound level
    except serial.SerialException as e:
        st.write("Error reading sound level from Arduino:", str(e))
        sound_level = None

    return {
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "altitude": altitude,
        "light_level": light_level,
        "sound_level": sound_level
    }

def display_weather_data(data):
    """Function to display weather data on Streamlit."""
    st.write("### Weather Data")
    st.write("Temperature:", data["temperature"], "°C")
    st.write("Humidity:", data["humidity"], "%")
    st.write("Pressure:", data["pressure"], "Pa")
    st.write("Altitude:", data["altitude"], "m")
    st.write("Light Level:", data["light_level"])
    st.write("Sound Level:", data["sound_level"])

def system_on():
    """Function to turn the system on and handle voice commands."""
    global system_active
    system_active = True
    digital_write(LED_PIN, True)  # Turn on the LED
    speak("System initialized and ready.")
    oled_print("System Ready")
    time.sleep(1)
    oled_clear()
    speak("Hey, I am Alice, your weather assistant. How can I help you today?")
    oled_print("I am Alice, your weather assistant")
    time.sleep(2)
    oled_clear()

    while system_active:
        command = recognize_speech()
        if command:
            if "temperature" in command:
                weather_data = get_weather_data()
                temperature = weather_data["temperature"]
                if temperature is not None:
                    speak(f"The temperature is {temperature:.1f} degrees Celsius.")
                    st.write(f"Temperature: {temperature:.1f}°C")
            elif "humidity" in command:
                humidity = weather_data["humidity"]
                if humidity is not None:
                    speak(f"The humidity is {humidity:.1f} percent.")
                    st.write(f"Humidity: {humidity:.1f}%")
            elif "pressure" in command:
                pressure = weather_data["pressure"]
                if pressure is not None:
                    speak(f"The atmospheric pressure is {pressure:.1f} Pascals.")
                    st.write(f"Pressure: {pressure:.1f} Pa")
            elif "altitude" in command:
                altitude = weather_data["altitude"]
                if altitude is not None:
                    speak(f"The altitude is approximately {altitude:.1f} meters.")
                    st.write(f"Altitude: {altitude:.1f} m")
            elif "light" in command:
                light_level = weather_data["light_level"]
                if light_level is not None:
                    speak(f"The light level is {light_level}")
                    st.write(f"Light Level: {light_level}")
            elif "sound" in command:
                sound_level = weather_data["sound_level"]
                if sound_level is not None:
                    speak(f"The sound level is {sound_level}")
                    st.write(f"Sound Level: {sound_level}")
            elif "clear screen" in command:
                oled_clear()
                speak("Screen cleared.")
                st.write("Screen cleared.")
            elif "status" in command:
                data = get_weather_data()
                status = (
                    f"Temp: {data['temperature']:.1f}C, "
                    f"Humidity: {data['humidity']:.1f}%, "
                    f"Pressure: {data['pressure']:.1f} Pa, "
                    f"Altitude: {data['altitude']:.1f} m, "
                    f"Light: {data['light_level']}, "
                    f"Sound: {data['sound_level']}"
                )
                speak(status)
                st.write(status)
            elif "turn off" in command or "bye" in command or "goodnight" in command or "good night" in command:
                system_off()

def system_off():
    """Function to turn the system off."""
    global system_active
    system_active = False
    digital_write(LED_PIN, False)  # Turn off the LED
    speak("Goodbye. System turning off.")
    oled_print("Goodbye")
    time.sleep(1)
    oled_clear()

def main():
    """Main function to start the Streamlit app and handle button press."""
    global system_active

    st.title("Alice: Your Weather Assistant")
    st.write("Press the button on the Arduino to run the application")

    while True:
        button_state = digital_read(BUTTON_PIN)  # Check the button state
        if button_state == 1:
            system_on()
            break

if __name__ == "__main__":
    main()
