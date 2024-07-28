# Alice: Your Weather Assistant(ENGI 1020 PROJECT)

Alice is an interactive weather assistant that utilizes a Streamlit web interface, speech recognition, and text-to-speech capabilities to provide real-time weather information from Arduino sensors. Alice can respond to various voice commands related to weather data, including temperature, humidity, pressure, altitude, light level, and sound level.

## Features

- **Voice Interaction**: Uses speech_recognition library to understand voice commands.
- **Real-time Weather Data**: Retrieves data from Arduino sensors for temperature, humidity, pressure, altitude, light level, and sound level.
- **Text-to-Speech**: Provides spoken responses using `pyttsx3`.
- **OLED Display**: Displays information and status messages on an OLED screen connected to the Arduino.
- **LED Indicator**: Turns on an LED indicator when the system is active.

## Requirements

- Python 3.8+
- Grove Beginner Kit For Arduino
- OLED display
- Microphone for speech recognition
- `requirements.txt` includes all necessary Python libraries.

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/ENGI-1020-Project.git
   cd ENGI-1020-Project

2. **Install the required Python Packages:**

  <pre><code>pip install -r requirements.txt</code></pre>

3. **Connect your Grove Beginner Kit to your machine**


# Running the Application on your Local Machine:

1. **Navigate to the project directory:**

   <pre><code>cd ENGI-1020-Project</code></pre>

   
2. **Run the Streamlit app:**
   <pre><code>streamlit run app.py</code></pre>

3. **Press the button(D6) on the Grove Beginner Kit to activate the system.**

# Usage
Once the system is activated, you can interact with Alice by speaking commands. Alice will respond with the requested weather data. Here are some example commands:

<pre>
-"What's the temperature?"
-"What's the humidity?"
-"What's the pressure?"
-"What's the altitude?"
-"What's the light level?"
-"What's the sound level?"
-"Clear screen"
-"Status"
-"Turn off" / "Bye" / "Goodnight" / "Good night"</pre>

# Project Structure
<pre>
-app.py: Main Streamlit application file.
-requirements.txt: List of Python dependencies.</pre>

# Acknowledgements
<pre>
-pyttsx3 for text-to-speech.
-speech_recogniton
-Streamlit for the web interface.
-engi1020 for Arduino integration.
</pre>

# License
This project is licensed under the MIT License.

